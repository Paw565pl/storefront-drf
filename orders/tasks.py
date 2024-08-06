from datetime import timedelta

from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone

from orders.models import Cart


@shared_task
def remove_unused_carts():
    one_month_ago = timezone.now() - timedelta(days=30)
    Cart.objects.filter(updated_at__lt=one_month_ago).delete()


@shared_task
def send_order_confirmation_email(order_id, username, user_email):
    subject = f"Order nr. {order_id} - confirmation"
    from_email = "info@storefront.com"

    context = {"order_id": order_id, "username": username}
    text_content = render_to_string("orders/order_confirmation.txt", context)
    html_content = render_to_string("orders/order_confirmation.html", context)

    email_message = EmailMultiAlternatives(
        subject=subject, body=text_content, from_email=from_email, to=[user_email]
    )
    email_message.attach_alternative(html_content, "text/html")
    email_message.send(fail_silently=False)
