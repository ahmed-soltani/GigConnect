from django.db import models
from django.conf import settings
from django.db.models import Avg
from django.utils.safestring import mark_safe
import math


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(decimal_places=2, max_digits=10)
    seller = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             related_name='product_created_by',
                             related_query_name='product_created_by',
                             )

    def average_rating(self):
        return self.reviews.aggregate(avg=Avg('rating'))['avg']

    def stars(self):
        avg = self.average_rating()
        filled_stars = math.trunc(avg)
        half_star = 1 if (avg - math.trunc(avg)) >= 0.5 else 0
        empty_stars = 5 - (filled_stars + half_star)

        html = (
            '<i class="bi bi-star-fill"></i>' * filled_stars +
            '<i class="bi bi-star-half"></i>' * half_star +
            '<i class="bi bi-star"></i>' * empty_stars
        )
        return mark_safe(html)

    class Meta:
        ordering = ['name', 'price', 'seller']
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def __str__(self):
        return f"{self.name} ({self.price})"

    def __repr__(self):
        return '<Product {}'.format(self.name + ' ' + self.price) + ' by ' + self.seller.username + '>'


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='product_images',
    )
    image = models.ImageField(
        upload_to='product_images/',
        default='product_images/default_image.jpeg',
    )

    def __str__(self):
        return f"Images of {self.product.name}"