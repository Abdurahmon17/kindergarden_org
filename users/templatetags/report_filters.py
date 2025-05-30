from django import template

register = template.Library()

# Example filter (optional)
@register.filter
def format_date(value):
    return value.strftime('%Y-%m') if hasattr(value, 'strftime') else value