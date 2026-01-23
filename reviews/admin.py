from django.contrib import admin
from .models import Review, Vote, ReviewReport

# Register your models here.
admin.register(Review)
admin.register(Vote)
admin.register(ReviewReport)