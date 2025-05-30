import pytest
from reports.models import MonthlyReport
from datetime import date

@pytest.mark.django_db
def test_monthly_report_str_and_properties():
    # 2025-yil, may oyi uchun report yaratamiz
    report = MonthlyReport.objects.create(
        report_date=date(2025, 5, 1),
        prepared_portions=100,
        possible_portions=120,
        difference_percent=16.7,
        warning=True
    )
    # __str__ metodi
    assert str(report) == "2025-05 Report"
    # formatted_date property
    assert report.formatted_date == "2025-05"
    # month property
    assert report.month == "May"
    # year property
    assert report.year == 2025

@pytest.mark.django_db
def test_monthly_report_default_values():
    report = MonthlyReport.objects.create()
    # created_at va updated_at avtomatik to'ldiriladi, report_date ham default now bo'ladi
    assert isinstance(report.report_date, date)
    assert report.prepared_portions == 0
    assert report.possible_portions == 0
    assert report.difference_percent == 0.0
    assert report.warning is False