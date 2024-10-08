from django.conf import settings
from django.db.models import Sum
from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver

from orders.models import Customer, CartItem, OrderItem, Order, Cart
from orders.tasks import send_order_confirmation_email


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_customer_for_new_user(sender, instance, created: bool, **kwargs):
    if created:
        Customer.objects.create(user=instance)


@receiver([pre_save], sender=CartItem)
def calculate_cart_item_total_price(sender, instance: CartItem, **kwargs):
    instance.total_price = instance.quantity * instance.product.unit_price


@receiver([pre_save], sender=OrderItem)
def calculate_order_item_total_price(sender, instance: OrderItem, **kwargs):
    old_order_item: OrderItem | None = OrderItem.objects.filter(id=instance.id).first()
    old_quantity = old_order_item.quantity if old_order_item is not None else 0
    product = instance.product

    quantity_change = instance.quantity - old_quantity
    product.inventory -= quantity_change
    product.save()

    instance.total_price = instance.quantity * product.unit_price


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


@receiver(post_save, sender=Order)
def send_email_to_customer_with_order_confirmation(
    sender, instance: Order, created: bool, **kwargs
):
    if created:
        order_id, username, user_email = (
            instance.id,
            instance.customer.user.username,
            instance.customer.user.email,
        )
        send_order_confirmation_email.delay(order_id, username, user_email)
