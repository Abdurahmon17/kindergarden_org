from django.db.models.signals import post_save
from django.dispatch import receiver
from reports.models import MonthlyReport
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

@receiver(post_save, sender=MonthlyReport)
def notify_report_warning(sender, instance, **kwargs):
    if instance.warning:
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'stock_updates',
            {
                'type': 'report_warning',
                'message': {
                    'month': instance.month.strftime('%Y-%m'),
                    'difference_percent': instance.difference_percent,
                    'alert': f"Oylik farq {instance.difference_percent}% ga yetdi, 15% dan oshdi!"
                }
            }
        )