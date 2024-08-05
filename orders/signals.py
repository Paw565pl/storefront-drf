from django.conf import settings
from django.db.models import Sum
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from orders.models import Customer, CartItem, Cart, OrderItem, Order


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_customer_for_new_user(sender, instance, created: bool, **kwargs):
    if created:
        Customer.objects.create(user=instance)


@receiver([post_save, post_delete], sender=CartItem)
def update_cart_total_price(sender, instance: CartItem, **kwargs):
    def do_update_cart_total_price():
        cart_id = instance.cart_id
        new_total_price = (
            CartItem.objects.filter(cart_id=cart_id)
            .aggregate(Sum("total_price"))
            .get("total_price__sum")
            or 0
        )
        Cart.objects.filter(id=cart_id).update(total_price=new_total_price)

    origin = kwargs.get("origin")
    if origin is None:  # update total price if signal is post_save
        do_update_cart_total_price()
    elif isinstance(
        origin, CartItem
    ):  # update total price if delete origin is CartItem
        do_update_cart_total_price()


@receiver([post_save, post_delete], sender=OrderItem)
def update_order_total_price(sender, instance: OrderItem, **kwargs):
    def do_update_order_total_price():
        order_id = instance.order_id
        new_item_total_price = instance.quantity * instance.product.unit_price
        OrderItem.objects.filter(id=instance.id).update(
            total_price=new_item_total_price
        )

        new_total_price = (
            OrderItem.objects.filter(order_id=order_id)
            .aggregate(Sum("total_price"))
            .get("total_price__sum")
            or 0
        )
        Order.objects.filter(id=order_id).update(total_price=new_total_price)

    origin = kwargs.get("origin")
    created = kwargs.get("created")

    # update total price only if model is updated or directly deleted
    model_update = origin is None and not created
    direct_model_delete = isinstance(origin, OrderItem)
    if model_update or direct_model_delete:
        do_update_order_total_price()
