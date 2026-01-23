from datetime import date, datetime
from django.contrib.auth.models import AbstractUser
from django.db import models

from shoppingcart.models import ShoppingCart


def get_date_20_years_ago():
    now = datetime.now()
    year = now.year
    month = now.month
    day = now.day
    return date(year - 20, month, day)

class MyUser(AbstractUser):
    date_of_birth = models.DateField(default=get_date_20_years_ago())
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    is_cs = models.BooleanField(default=False) # Is normal user or Customer_Service

    def count_shopping_cart_items(self):
        count = 0
        if self.is_authenticated:
            shopping_carts = ShoppingCart.objects.filter(myuser=self)
            if shopping_carts:
                shopping_cart = shopping_carts.first()
                count = shopping_cart.get_number_of_items()

        return count

    def execute_after_login(self):

        self.save()

    def has_birthday_today(self):
        now = datetime.now()
        today_month = now.month
        today_day = now.day

        user_month = self.date_of_birth.month
        user_day = self.date_of_birth.day

        return today_month == user_month and today_day == user_day

    def __str__(self):
        return self.username + ': ' + self.first_name + ' ' + self.last_name + ' (' + str(self.date_of_birth) + ')'
