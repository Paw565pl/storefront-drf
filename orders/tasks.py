from datetime import timedelta

from celery import shared_task
from django.utils import timezone

from orders.models import Cart


@shared_task
def remove_unused_carts():
    one_month_ago = timezone.now() - timedelta(days=30)
    Cart.objects.filter(updated_at__lt=one_month_ago).delete()
