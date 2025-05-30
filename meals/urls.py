from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'meals', views.MealViewSet, basename='meal')
router.register(r'distributions', views.MealDistributionViewSet, basename='distribution')

urlpatterns = [
    path('', views.meal_list, name='meal_list'),
    path('meal/<int:pk>/', views.meal_detail, name='meal_detail'),
    path('meal/create/', views.meal_create, name='meal_create'),
    path('meal/edit/<int:pk>/', views.meal_edit, name='meal_edit'),
    path('meal/delete/<int:pk>/', views.meal_delete, name='meal_delete'),
    path('distribution/create/', views.distribution_create, name='distribution_create'),
    path('api/', include(router.urls)),
]