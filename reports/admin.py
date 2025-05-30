from django.contrib import admin
from .models import MonthlyReport

@admin.register(MonthlyReport)
class MonthlyReportAdmin(admin.ModelAdmin):
    list_display = ('report_date', 'prepared_portions', 'possible_portions', 'difference_percent', 'warning')
    list_filter = ('report_date', 'warning')
    ordering = ('-report_date',)  # Yoki boshqa mos maydon
    search_fields = ('report_date',)

    # Qo'shimcha sozlamalar
    date_hierarchy = 'report_date'