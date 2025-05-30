from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import F
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from .serializers import ProductSerializer
from .permissions import IsAdminOrManager, IsChefReadOnly
from .models import Product


# --- REST API uchun ViewSet ---
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated, IsAdminOrManager | IsChefReadOnly]
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['name']
    filterset_fields = ['category']

    @action(detail=False, methods=['get'])
    def low_stock(self, request):
        low_stock_products = Product.objects.filter(quantity_grams__lte=F('min_quantity'))
        serializer = self.get_serializer(low_stock_products, many=True)
        return Response(serializer.data)


# --- HTML View’lar (sync versiyada) ---
@login_required
def inventory_list(request):
    products = Product.objects.all()
    return render(request, 'inventory/product_list.html', {'products': products})


@login_required
def inventory_detail(request, pk):
    product = Product.objects.get(pk=pk)
    return render(request, 'inventory/product_form.html', {'product': product})


@login_required
def inventory_create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        quantity = request.POST.get('quantity_grams')
        min_quantity = request.POST.get('min_quantity')

        if not name or not quantity or not min_quantity:
            messages.error(request, "Barcha maydonlarni to‘ldiring.")
            return render(request, 'inventory/product_form.html')

        try:
            Product.objects.create(
                name=name,
                quantity_grams=float(quantity),
                min_quantity=float(min_quantity)
            )
            messages.success(request, "Mahsulot muvaffaqiyatli qo'shildi.")
            return redirect('inventory_list')
        except IntegrityError:
            messages.error(request, "Bu nomdagi mahsulot allaqachon mavjud.")
        except ValueError:
            messages.error(request, "Miqdor noto‘g‘ri formatda.")

    return render(request, 'inventory/product_form.html')


@login_required
def inventory_edit(request, pk):
    product = Product.objects.get(pk=pk)
    user_role = request.user.role

    if request.method == 'POST':
        if user_role not in ['Admin', 'Manager']:
            messages.error(request, "Sizda mahsulotni tahrirlash ruxsati yo‘q.")
            return redirect('inventory_list')

        name = request.POST.get('name')
        quantity = request.POST.get('quantity_grams')
        min_quantity = request.POST.get('min_quantity')

        if not name or not quantity or not min_quantity:
            messages.error(request, "Barcha maydonlarni to‘ldiring.")
            return render(request, 'inventory/product_form.html', {'product': product})

        try:
            product.name = name
            product.quantity_grams = float(quantity)
            product.min_quantity = float(min_quantity)
            product.save()
            messages.success(request, "Mahsulot muvaffaqiyatli tahrirlandi.")
            return redirect('inventory_list')
        except ValueError:
            messages.error(request, "Miqdor noto‘g‘ri formatda.")

    return render(request, 'inventory/product_form.html', {'product': product})


@login_required
def inventory_delete(request, pk):
    product = Product.objects.get(pk=pk)
    user_role = request.user.role

    if request.method == 'POST':
        if user_role not in ['Admin', 'Manager']:
            messages.error(request, "Sizda mahsulotni o‘chirish ruxsati yo‘q.")
            return redirect('inventory_list')

        product.delete()
        messages.success(request, "Mahsulot muvaffaqiyatli o‘chirildi.")
        return redirect('inventory_list')

    return render(request, 'inventory/product_delete.html', {'product': product})


@login_required
def low_stock_list(request):
    products = Product.objects.filter(quantity_grams__lte=F('min_quantity'))
    return render(request, 'inventory/product_list.html', {'products': products, 'low_stock': True})
