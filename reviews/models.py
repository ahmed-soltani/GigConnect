from django.core.exceptions import ValidationError
from django.db import models
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from decimal import Decimal

from products.models import Product


def validate_step(value):
    if (value * 4) % 1 != 0:
        raise ValidationError("Rating must be in 0.25 increments")

class Review(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    rating = models.DecimalField(
        decimal_places=2,
        max_digits=3,
        validators=[
            MinValueValidator(Decimal('1.00')),
            MaxValueValidator(Decimal('5.00')),
            validate_step,
        ]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    text = models.TextField(max_length=500)

    class Meta:
        ordering = ['created_at']
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'product'],
                name='one_review_per_user_per_product'
            )
        ]
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'

    def vote(self, user, choice):
        vote_exists = Vote.objects.filter(user=user, review=self).first()
        if vote_exists:
            if vote_exists.choice != choice:
                vote_exists.choice = choice
                vote_exists.save()
        else:
            vote = Vote.objects.create(
                choice=choice,
                user=user,
                review=self,
            )

    def upvotes(self):
        return self.vote_set.filter(choice=True).count()

    def downvotes(self):
        return self.vote_set.filter(choice=False).count()

    def __str__(self):
        return f"{self.user.username} - {self.product.name}: {self.rating}: {self.text}"

    def __repr__(self):
        return f"Review #{self.id}: {self.user.username} for {self.product.name}: rating {self.rating}: {self.text}"


class Vote(models.Model):
    choice = models.BooleanField()
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'review'],
                name='one_vote_per_user_review'
            )
        ]

    def __str__(self):
        return f"{self.choice} on {self.review.text} by {self.user.username}"


class ReviewReport(models.Model):
    REASON_TYPES = [
        ('S', 'Spam'),
        ('H', 'Hate speech'),
        ('OL', 'Offensive language'),
        ('FR', 'Fake review'),
        ('O', 'Other')
    ]
    reporter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE
    )
    reason = models.CharField(
        max_length=2,
        choices=REASON_TYPES,
    )
    timestamp = models.DateTimeField(auto_now_add=True)
    is_resolved = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['reporter', 'review'],
                name='one_report_per_user_review'
            )
        ]
        verbose_name = 'Review Report'
        verbose_name_plural = 'Review Reports'