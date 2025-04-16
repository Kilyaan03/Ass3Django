from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='index'),
    path('archer/', views.archer, name='archer'),
    path('monk/', views.monk, name='monk'),
    path('asip/', views.asip, name='asip'),
    path('tayto/', views.tayto, name='tayto'),
    path('futuroscope/', views.futuroscope, name='futuroscope'),
    path('Parc_Asterix/', views.Parc_Asterix, name='Parc_Asterix'),
    path('PastaReview/', views.PastaReview, name='PastaReview'),
    path('PizzaReview/', views.PizzaReview, name='PizzaReview'),
    path('CroqMonsieur/', views.CroqMonsieur, name='CroqMonsieur'),
    path('review/create/', views.create_review, name='create_review'),
    path('review/<int:review_id>/edit/', views.update_review, name='update_review'),
    path('review/<int:review_id>/delete/', views.delete_review, name='delete_review'),
    path('review/<int:review_id>/', views.review_detail, name='review_detail'),
    path('review/<int:review_id>/comments/json/', views.review_comments_json, name='review_comments_json'),
    path('review/<int:review_id>/comments/add/', views.add_comment_ajax, name='add_comment_ajax'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='myapp/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='index'), name='logout'),
    path('base/', views.base, name='base'),
    path('review_list', views.review_list, name='review_list'),
    path('index', views.index, name='index'),
]
