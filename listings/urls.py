from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.listing_list, name='listing_list'),
    path('listing/<int:pk>/', views.listing_detail, name='listing_detail'),
    path('create/', views.create_listing, name='create_listing'),
    path('listing/<int:pk>/image/', views.add_listing_image, name='add_listing_image'),
    path('listing/<int:pk>/favorite/', views.toggle_favorite, name='toggle_favorite'),
    path('favorites/', views.my_favorites, name='my_favorites'),
]