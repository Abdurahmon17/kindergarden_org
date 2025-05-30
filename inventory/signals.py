# inventory/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Product

# Misol signal
@receiver(post_save, sender=Product)  # YourModel ni o‘z modelingiz bilan almashtiring
def send_notification(sender, instance, created, **kwargs):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        'inventory_group',  # Guruh nomi
        {
            'type': 'inventory_update',
            'message': f'New item created: {instance.name}'
        }
    )