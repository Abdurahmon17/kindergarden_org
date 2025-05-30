from django.utils import timezone
from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from .models import MonthlyReport
from .serializers import MonthlyReportSerializer
from .forms import MonthlyReportForm
from .tasks import generate_monthly_report
from django_filters.rest_framework import DjangoFilterBackend
from app.permissions import IsAdminOrManager
import logging

logger = logging.getLogger(__name__)


class MonthlyReportViewSet(viewsets.ModelViewSet):
    queryset = MonthlyReport.objects.all()
    serializer_class = MonthlyReportSerializer
    permission_classes = [IsAuthenticated, IsAdminOrManager]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['month', 'warning']


@login_required
def report_dashboard(request):
    reports = MonthlyReport.objects.all()
    return render(request, 'reports/report_dashboard.html', {'reports': reports})


@login_required
def report_detail(request, pk):
    report = get_object_or_404(MonthlyReport, pk=pk)
    return render(request, 'reports/monthly_report.html', {'report': report})


@login_required
def check_report_status(request, task_id):
    from celery.result import AsyncResult
    try:
        task = AsyncResult(task_id)
        response = {
            'ready': task.ready(),
            'successful': task.successful(),
            'result': task.result if task.ready() else None
        }
        return JsonResponse(response)
    except Exception as e:
        logger.error(f"Error checking task status {task_id}: {e}")
        return JsonResponse({'error': str(e)}, status=500)


@login_required
def report_create(request):
    current_date = timezone.now()
    year_choices = range(current_date.year - 5, current_date.year + 1)
    month_choices = [
        (1, 'Yanvar'), (2, 'Fevral'), (3, 'Mart'),
        (4, 'Aprel'), (5, 'May'), (6, 'Iyun'),
        (7, 'Iyul'), (8, 'Avgust'), (9, 'Sentabr'),
        (10, 'Oktabr'), (11, 'Noyabr'), (12, 'Dekabr')
    ]

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        form = MonthlyReportForm(request.POST)
        if form.is_valid():
            try:
                year = form.cleaned_data['report_date'].year
                month = form.cleaned_data['report_date'].month
                prepared = form.cleaned_data['prepared_portions']
                possible = form.cleaned_data['possible_portions']
                percent = form.cleaned_data['difference_percent']
                warning = form.cleaned_data['warning']

                task = generate_monthly_report.delay(year, month, prepared, possible, percent, warning)
                request.session['report_task_id'] = task.id
                logger.info(f"Task {task.id} started for {year}-{month:02d}")
                return JsonResponse({'task_id': task.id}, status=200)
            except Exception as e:
                logger.error(f"Error starting task: {e}")
                return JsonResponse({'error': str(e)}, status=500)
        else:
            logger.error(f"Form validation failed: {form.errors.as_text()}")
            return JsonResponse({'error': form.errors.as_json()}, status=400)
    else:
        if request.method == 'POST':
            form = MonthlyReportForm(request.POST)
            if form.is_valid():
                try:
                    year = form.cleaned_data['report_date'].year
                    month = form.cleaned_data['report_date'].month
                    prepared = form.cleaned_data['prepared_portions']
                    possible = form.cleaned_data['possible_portions']
                    percent = form.cleaned_data['difference_percent']
                    warning = form.cleaned_data['warning']

                    task = generate_monthly_report.delay(year, month, prepared, possible, percent, warning)
                    request.session['report_task_id'] = task.id
                    logger.info(f"Task {task.id} started for {year}-{month:02d}")
                    messages.info(request, f"Hisobot {year}-{month:02d} uchun yaratilmoqda...")
                    return redirect('reports:report_dashboard')
                except Exception as e:
                    logger.error(f"Error starting task: {e}")
                    messages.error(request, f"Xato: {str(e)}")
            else:
                logger.error(f"Form validation failed: {form.errors.as_text()}")
                messages.error(request, f"Forma xatolari: {form.errors.as_text()}")
        else:
            form = MonthlyReportForm(initial={'report_date': current_date})

    return render(request, 'reports/monthly_report_form.html', {
        'form': form,
        'current_date': current_date,
        'year_choices': year_choices,
        'month_choices': month_choices
    })


@login_required
def report_edit(request, pk):
    report = get_object_or_404(MonthlyReport, pk=pk)
    if request.user.role not in ['Admin', 'Manager']:
        messages.error(request, "Sizda hisobotni tahrirlash ruxsati yo‘q.")
        return redirect('reports:report_dashboard')
    if request.method == 'POST':
        form = MonthlyReportForm(request.POST, instance=report)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Hisobot muvaffaqiyatli tahrirlandi.")
                return redirect('reports:report_dashboard')
            except IntegrityError:
                messages.error(request, "Bu sana uchun hisobot allaqachon mavjud.")
            except Exception as e:
                messages.error(request, f"Xato: {str(e)}")
        else:
            messages.error(request, f"Forma xatolari: {form.errors.as_text()}")
    else:
        form = MonthlyReportForm(instance=report)
    return render(request, 'reports/monthly_report_edit.html', {'form': form, 'report': report})


@login_required
def report_delete(request, pk):
    report = get_object_or_404(MonthlyReport, pk=pk)
    if request.user.role not in ['Admin', 'Manager']:
        messages.error(request, "Sizda hisobotni o‘chirish ruxsati yo‘q.")
        return redirect('reports:report_dashboard')
    if request.method == 'POST':
        report.delete()
        messages.success(request, "Hisobot muvaffaqiyatli o‘chirildi.")
        return redirect('reports:report_dashboard')
    return render(request, 'reports/monthly_report_delete.html', {'report': report})


