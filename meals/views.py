from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Meal, MealDistribution
from .serializers import MealSerializer, MealDistributionSerializer
from app.permissions import IsAdminOrManager, IsChefReadOnly, IsAdminOrChef, IsManagerReadOnly

# --- REST API ViewSet'lar ---
class MealViewSet(viewsets.ModelViewSet):
    queryset = Meal.objects.prefetch_related('ingredients')
    serializer_class = MealSerializer
    permission_classes = [IsAuthenticated, IsAdminOrManager | IsChefReadOnly]
    filter_backends = [SearchFilter]
    search_fields = ['name']


class MealDistributionViewSet(viewsets.ModelViewSet):
    queryset = MealDistribution.objects.select_related('meal', 'user')
    serializer_class = MealDistributionSerializer
    permission_classes = [IsAuthenticated, IsAdminOrChef | IsManagerReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# --- HTML View'lar ---
@login_required
def meal_list(request):
    meals = Meal.objects.prefetch_related('ingredients').all()
    return render(request, 'meals/meal_list.html', {'meals': meals})


@login_required
def meal_detail(request, pk):
    meal = Meal.objects.prefetch_related('ingredients').get(pk=pk)
    return render(request, 'meals/meal_form.html', {'meal': meal})


@login_required
def meal_create(request):
    user_role = request.user.role
    if user_role not in ['Admin', 'Manager']:
        messages.error(request, "Sizda ovqat yaratish ruxsati yo‘q.")
        return redirect('meal_list')

    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            Meal.objects.create(name=name)
            messages.success(request, "Ovqat muvaffaqiyatli yaratildi.")
            return redirect('meal_list')
        else:
            messages.error(request, "Ovqat nomi bo‘sh bo‘lishi mumkin emas.")

    return render(request, 'meals/meal_form.html')


@login_required
def meal_edit(request, pk):
    meal = Meal.objects.get(pk=pk)
    user_role = request.user.role
    if user_role not in ['Admin', 'Manager']:
        messages.error(request, "Sizda ovqatni tahrirlash ruxsati yo‘q.")
        return redirect('meal_list')

    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            meal.name = name
            meal.save()
            messages.success(request, "Ovqat muvaffaqiyatli tahrirlandi.")
            return redirect('meal_list')
        else:
            messages.error(request, "Ovqat nomi bo‘sh bo‘lishi mumkin emas.")
    return render(request, 'meals/meal_form.html', {'meal': meal})


@login_required
def meal_delete(request, pk):
    meal = Meal.objects.get(pk=pk)
    user_role = request.user.role
    if user_role not in ['Admin', 'Manager']:
        messages.error(request, "Sizda ovqatni o‘chirish ruxsati yo‘q.")
        return redirect('meal_list')

    if request.method == 'POST':
        meal.delete()
        messages.success(request, "Ovqat muvaffaqiyatli o‘chirildi.")
        return redirect('meal_list')
    return render(request, 'meals/meal_delete.html', {'meal': meal})


@login_required
def distribution_create(request):
    user_role = request.user.role
    if user_role not in ['Admin', 'Chef']:
        messages.error(request, "Sizda ovqat tarqatish ruxsati yo‘q.")
        return redirect('meal_list')

    if request.method == 'POST':
        meal_id = request.POST.get('meal')
        quantity = request.POST.get('quantity')
        if meal_id and quantity:
            try:
                meal = Meal.objects.get(pk=meal_id)
                MealDistribution.objects.create(
                    meal=meal, user=request.user, quantity=float(quantity)
                )
                messages.success(request, "Ovqat tarqatish muvaffaqiyatli amalga oshirildi.")
                return redirect('meal_list')
            except Exception as e:
                messages.error(request, f"Xato yuz berdi: {e}")
        else:
            messages.error(request, "Barcha maydonlarni to‘ldiring.")

    meals = Meal.objects.all()
    return render(request, 'meals/distribution_form.html', {'meals': meals})
