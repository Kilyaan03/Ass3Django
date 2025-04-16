from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.review_list, name='review_list'),
    path('review/create/', views.create_review, name='create_review'),
    path('review/<int:review_id>/edit/', views.update_review, name='update_review'),
    path('review/<int:review_id>/delete/', views.delete_review, name='delete_review'),
    path('review/<int:review_id>/', views.review_detail, name='review_detail'),
    path('review/<int:review_id>/comments/json/', views.review_comments_json, name='review_comments_json'),
    path('review/<int:review_id>/comments/add/', views.add_comment_ajax, name='add_comment_ajax'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
]
