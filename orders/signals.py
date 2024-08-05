from django.conf import settings
from django.db.models import Sum
from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver

from orders.models import Customer, CartItem, OrderItem, Order, Cart


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_customer_for_new_user(sender, instance, created: bool, **kwargs):
    if created:
        Customer.objects.create(user=instance)


@receiver([pre_save], sender=CartItem)
@receiver([pre_save], sender=OrderItem)
def calculate_item_total_price(sender, instance: CartItem | OrderItem, **kwargs):
    instance.total_price = instance.quantity * instance.product.unit_price


@receiver([post_save, post_delete], sender=CartItem)
def update_cart_total_price(sender, instance: CartItem, **kwargs):
    origin = kwargs.get("origin")

    # update total price if model is saved or directly deleted
    model_save = origin is None
    direct_model_delete = isinstance(origin, OrderItem)
    if model_save or direct_model_delete:
        cart_id = instance.cart_id
        new_total_price = (
            CartItem.objects.filter(cart_id=cart_id)
            .aggregate(Sum("total_price"))
            .get("total_price__sum")
            or 0
        )
        Cart.objects.filter(id=cart_id).update(total_price=new_total_price)


@receiver([post_save, post_delete], sender=OrderItem)
def update_order_total_price(sender, instance: OrderItem, **kwargs):
    origin = kwargs.get("origin")
    created = kwargs.get("created")

    # update total price if model is updated or directly deleted
    model_update = origin is None and not created
    direct_model_delete = isinstance(origin, OrderItem)
    if model_update or direct_model_delete:
        order_id = instance.order_id
        new_total_price = (
            OrderItem.objects.filter(order_id=order_id)
            .aggregate(Sum("total_price"))
            .get("total_price__sum")
            or 0
        )
        Order.objects.filter(id=order_id).update(total_price=new_total_price)
