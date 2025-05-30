from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'reports'

router = DefaultRouter()
router.register(r'reports', views.MonthlyReportViewSet, basename='report')

urlpatterns = [
    path('dashboard/', views.report_dashboard, name='report_dashboard'),
    path('report/<int:pk>/', views.report_detail, name='report_detail'),
    path('create/', views.report_create, name='report_create'),
    path('check-status/<str:task_id>/', views.check_report_status, name='check_report_status'),
    path('edit/<int:pk>/', views.report_edit, name='report_edit'),
    path('delete/<int:pk>/', views.report_delete, name='report_delete'),
    path('api/', include(router.urls)),
]