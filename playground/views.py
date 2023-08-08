from django.shortcuts import render
from django.db.models import (
    Count,
    Max,
    Min,
    F,
    Q,
    Value,
    Func,
    ExpressionWrapper,
    DecimalField,
)
from django.db.models.functions import Concat
from django.db import transaction, connection
from django.contrib.contenttypes.models import ContentType
from tags.models import TaggedItem
from store.models import Product, OrderItem, Order, Customer, Collection


# Create your views here.
# @transaction.atomic()
def index(request):
    # queryset = (
    #     OrderItem.objects.select_related("product")
    #     .select_related("order__customer")
    #     .order_by("-order__placed_at")[:5]
    # )

    # queryset = (
    #     Order.objects.select_related("customer")
    #     .prefetch_related("orderitem_set__product")
    #     .order_by("-placed_at")[:5]
    # )
    # __ relative value

    # queryset = Product.objects.aggregate(max=Max("unit_price"))

    # queryset = Customer.objects.annotate(
    #     full_name=Concat("first_name", Value(" "), "last_name")
    # )

    # queryset = Customer.objects.annotate(orders_count=Count("order"))
    # group data

    # discounted_price = ExpressionWrapper(
    #     F("unit_price") * 0.8,
    #     output_field=DecimalField(max_digits=10, decimal_places=2),
    # )
    # queryset = Product.objects.annotate(discounted_price=discounted_price)

    # queryset = TaggedItem.objects.get_tags_for(Product, "1")
    # generic query

    # collection = Collection()
    # collection.title = "Video Games"
    # collection.featured_product = Product(pk=1)
    # collection.save()
    # add data

    # collection = Collection.objects.get(pk=1)
    # collection.title = "Games"
    # collection.featured_product = None
    # collection.save()
    # update data

    # collection = Collection(pk=1)
    # collection.delete()
    # delete data

    # with transaction.atomic():
    #     order = Order()
    #     order.customer_id = 15
    #     order.save()

    #     item = OrderItem()
    #     item.order = order
    #     item.product_id = 1
    #     item.quantity = 1
    #     item.unit_price = 10
    #     item.save()
    # transaction

    # queryset = Product.objects.raw("SELECT * FROM store_product")
    # raw query

    # with connection.cursor() as cursor:
    #     queryset = cursor.execute("SELECT * FROM store_product")

    return render(request, "hello.html", {"name": "user"})
