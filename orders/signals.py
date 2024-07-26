from django.conf import settings
from django.db.models import Sum
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from orders.models import Customer, CartItem, Cart


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_customer_for_new_user(sender, instance, created: bool, **kwargs):
    if created:
        Customer.objects.create(user=instance)


@receiver([post_save, post_delete], sender=CartItem)
def update_cart_total_price(sender, instance: CartItem, **kwargs):
    cart_id = instance.cart_id
    new_total_price = (
        CartItem.objects.filter(cart_id=cart_id)
        .aggregate(Sum("total_price"))
        .get("total_price__sum")
        or 0
    )
    Cart.objects.filter(id=cart_id).update(total_price=new_total_price)
