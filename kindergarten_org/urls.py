from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('meals/', include('meals.urls')),
    path('inventory/', include('inventory.urls')),
    path('reports/', include('reports.urls')),
    path('', include('users.urls')),
    path('api-auth/', include('rest_framework.urls')),
]