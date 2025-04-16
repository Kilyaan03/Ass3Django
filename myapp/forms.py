from django import forms
from .models import Review, Comment, UserProfile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['title', 'content', 'rating', 'category']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio', 'favorite_category']
