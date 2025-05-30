from django.db.models.signals import post_save
from django.dispatch import receiver
from meals.models import MealDistribution
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


@receiver(post_save, sender=MealDistribution)
def notify_distribution_update(sender, instance, **kwargs):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        'stock_updates',
        {
            'type': 'stock_update',
            'message': {
                'meal': instance.meal.name,
                'quantity': instance.quantity,
                'user': instance.user.username,
                'date_time': instance.date_time.isoformat(),
            }
        }
    )