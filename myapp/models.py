from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# This model is for categories, like TV Show, Food, or Theme Park.
# Each category just has a name, and we can use it to group reviews.
class Category(models.Model):
    name = models.CharField(max_length=100)  # The name of the category (e.g.TV show).

    def __str__(self):
        return self.name  # This makes it show the category name in the admin panel or when printed.

# This model is for reviews. Each review is tied to a category and an author.
# It has a title, content, rating, and the date it was created.
class Review(models.Model):
    title = models.CharField(max_length=200)  # The title of the review (e.g. Archer).
    content = models.TextField()  # The main text of the review.
    rating = models.IntegerField()  # The rating.
    category = models.ForeignKey(Category, on_delete=models.CASCADE)  # Links the review to a category.
    author = models.ForeignKey(User, on_delete=models.CASCADE)  # Links the review to the user who wrote it. And the delete part means if user is deleted then delete their reviews
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically sets the date when the review is created.

    def __str__(self):
        return self.title  # This makes it show the review title in the admin panel or when printed.

# This model is for comments on reviews. Each comment is tied to a review and a user.
# It has the text of the comment and the date it was created.
class Comment(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE)  # Links the comment to a specific review.
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Links the comment to the user who wrote it.
    text = models.TextField()  # The actual comment text.
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically sets the date when the comment is created.

# This model is for user profiles. It extends the default User model with extra fields.
# Each profile is tied to a user and can have a bio and a favorite category.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Links the profile to a specific user.
    bio = models.TextField(blank=True)  # A short bio about the user.
    favorite_category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)  # The user's favorite category.

    def __str__(self):
        return self.user.username  # This makes it show the username in the admin panel or when printed.
