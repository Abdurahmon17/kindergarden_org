from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import CustomUser
from .serializers import CustomUserSerializer
from reports.models import MonthlyReport

class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

# Dashboard view
@login_required
def dashboard(request):
    reports = MonthlyReport.objects.all().order_by('-id')
    if not reports:
        return render(request, 'users/dashboard.html', {
            'pie_chart_data': {'labels': [], 'data': []},
            'column_chart_data': {'labels': [], 'difference_percent': []},
            'no_data': True
        })

    # report_date dan yil-oy formatini olish
    labels = [report.report_date.strftime('%Y-%m') for report in reports]
    pie_data = [report.prepared_portions for report in reports]
    possible_data = [report.possible_portions for report in reports]

    pie_chart_data = {
        'labels': ['Prepared', 'Possible'],
        'data': [sum(pie_data), sum(possible_data)]
    }

    column_chart_data = {
        'labels': labels,
        'difference_percent': [
            (p - po) / po * 100 if po else 0 for p, po in zip(pie_data, possible_data)
        ]
    }

    return render(request, 'users/dashboard.html', {
        'pie_chart_data': pie_chart_data,
        'column_chart_data': column_chart_data,
        'no_data': False
    })

# Foydalanuvchilar ro‘yxati
@login_required
def user_list(request):
    users = CustomUser.objects.all()
    return render(request, 'users/user_list.html', {'users': users})

# Profil
@login_required
def user_profile(request):
    return render(request, 'users/user_form.html', {'user': request.user})

# Yaratish
@login_required
def user_create(request):
    if request.method == 'POST':
        user_role = request.user.role
        if user_role != 'Admin':
            messages.error(request, "Sizda foydalanuvchi yaratish ruxsati yo‘q.")
            return redirect('user_list')

        username = request.POST.get('username')
        email = request.POST.get('email')
        role = request.POST.get('role')
        password = request.POST.get('password')

        if username and email and role and password:
            CustomUser.objects.create_user(
                username=username, email=email, role=role, password=password
            )
            messages.success(request, "Foydalanuvchi muvaffaqiyatli yaratildi.")
            return redirect('user_list')

    return render(request, 'users/user_form.html')

# Tahrirlash
@login_required
def user_edit(request, pk):
    user = CustomUser.objects.get(pk=pk)
    current_role = request.user.role

    if request.method == 'POST':
        if current_role != 'Admin':
            messages.error(request, "Sizda foydalanuvchini tahrirlash ruxsati yo‘q.")
            return redirect('user_list')

        user.username = request.POST.get('username')
        user.email = request.POST.get('email')
        user.role = request.POST.get('role')
        password = request.POST.get('password')

        if password:
            user.set_password(password)

        user.save()
        messages.success(request, "Foydalanuvchi muvaffaqiyatli tahrirlandi.")
        return redirect('user_list')

    return render(request, 'users/user_form.html', {'user': user})

# O‘chirish
@login_required
def user_delete(request, pk):
    user = CustomUser.objects.get(pk=pk)
    current_user = request.user
    current_role = current_user.role

    if request.method == 'POST':
        if current_role != 'Admin':
            messages.error(request, "Sizda foydalanuvchini o‘chirish ruxsati yo‘q.")
            return redirect('user_list')

        if user == current_user:
            messages.error(request, "O‘zingizni o‘chira olmaysiz.")
            return redirect('user_list')

        user.delete()
        messages.success(request, "Foydalanuvchi muvaffaqiyatli o‘chirildi.")
        return redirect('user_list')

    return render(request, 'users/user_delete.html', {'user': user})

# Login (sync qoladi)
def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(request.GET.get('next', 'dashboard'))

        messages.error(request, 'Noto‘g‘ri foydalanuvchi nomi yoki parol.')
    else:
        form = AuthenticationForm()

    return render(request, 'users/login.html', {'form': form})

# Logout (sync qoladi)
def user_logout(request):
    logout(request)
    return redirect('user_login')
