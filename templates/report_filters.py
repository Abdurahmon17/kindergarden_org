# Create templatetags/report_filters.py
from django import template

register = template.Library()

@register.filter
def format_report_date(year, month):
    return f"{year}-{month:02d}"