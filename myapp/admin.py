from django.contrib import admin
from .models import Category, Review, Comment, UserProfile

# Register your models here.

admin.site.register(Category)
admin.site.register(Review)
admin.site.register(Comment)
admin.site.register(UserProfile)