from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter

# REST API router
router = DefaultRouter()
router.register(r'users', views.CustomUserViewSet, basename='user')

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('users/', views.user_list, name='user_list'),
    path('users/profile/', views.user_profile, name='user_profile'),
    path('users/create/', views.user_create, name='user_create'),
    path('users/edit/<int:pk>/', views.user_edit, name='user_edit'),
    path('users/delete/<int:pk>/', views.user_delete, name='user_delete'),
    path('login/', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name='user_logout'),
] + router.urls