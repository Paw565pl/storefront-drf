from decimal import Decimal
from uuid import uuid4

from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from django_extensions.db import fields as extension_fields
from phonenumber_field.modelfields import PhoneNumberField

from products.models import Product


# Create your models here.
class Address(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone_number = PhoneNumberField(max_length=255, unique=True)
    apartment_number = models.CharField(max_length=50, blank=True, null=True)
    street_number = models.CharField(max_length=50)
    street = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=10)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    country = models.CharField(max_length=255)

    class Meta:
        abstract = True

    def __str__(self) -> str:
        return f"Address of {self.first_name} {self.last_name}"


class CustomerAddress(Address):
    pass


class Customer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    address = models.ForeignKey(
        CustomerAddress, on_delete=models.SET_NULL, null=True, blank=True
    )

    def __str__(self) -> str:
        return self.user.username  # noqa


class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    updated_at = extension_fields.ModificationDateTimeField()
    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(Decimal(0))],
    )

    def __str__(self) -> str:
        return f"Cart {self.id}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    total_price = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal(0))]
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["cart", "product"], name="one_product_per_cart"
            ),
        ]

    def __str__(self) -> str:
        return f"{self.product.title} - quantity {self.quantity}"


class OrderAddress(Address):
    pass


class Order(models.Model):
    STATUS_IN_PROGRESS = "P"
    STATUS_IN_DELIVERY = "D"
    STATUS_COMPLETED = "C"

    STATUS_CHOICES = [
        (STATUS_IN_PROGRESS, "In progress"),
        (STATUS_IN_DELIVERY, "Issued for delivery"),
        (STATUS_COMPLETED, "Completed"),
    ]

    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    address = models.ForeignKey(OrderAddress, on_delete=models.PROTECT)
    status = models.CharField(
        max_length=1, choices=STATUS_CHOICES, default=STATUS_IN_PROGRESS
    )
    created_at = extension_fields.CreationDateTimeField()
    updated_at = extension_fields.ModificationDateTimeField()
    total_price = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal(0))]
    )

    class Meta:
        permissions = [
            ("cancel_order", "Can cancel order"),
        ]

    def __str__(self) -> str:
        return f"Order nr {self.id}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    total_price = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal(0))]
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["order", "product"], name="one_product_per_order"
            ),
        ]

    def __str__(self) -> str:
        return f"{self.product.title} - quantity {self.quantity}"
