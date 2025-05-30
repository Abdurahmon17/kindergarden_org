from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'products', views.ProductViewSet, basename='product')

urlpatterns = [
    path('', views.inventory_list, name='inventory_list'),
    path('item/<int:pk>/', views.inventory_detail, name='inventory_detail'),
    path('create/', views.inventory_create, name='inventory_create'),
    path('edit/<int:pk>/', views.inventory_edit, name='inventory_edit'),
    path('delete/<int:pk>/', views.inventory_delete, name='inventory_delete'),
    path('low-stock/', views.low_stock_list, name='low_stock_list'),
    path('api/', include(router.urls)),
]