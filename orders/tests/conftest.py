import pytest
from model_bakery import baker

from orders.models import CustomerAddress, Customer, Cart, CartItem, Order, OrderAddress
from orders.serializers import CustomerAddressSerializer


@pytest.fixture
def create_customer_address():
    def do_create_customer_address(customer: Customer) -> CustomerAddress:
        customer_address = baker.make(CustomerAddress, phone_number="+44123456789")
        customer.address = customer_address
        customer.save()

        return customer_address

    return do_create_customer_address


@pytest.fixture
def cart() -> Cart:
    cart = baker.make(Cart)
    return cart


@pytest.fixture
def create_cart_item():
    def do_create_cart_item(cart: Cart, item_quantity: int = 1) -> CartItem:
        cart_item = baker.make(CartItem, cart=cart, quantity=item_quantity)
        return cart_item

    return do_create_cart_item


@pytest.fixture
def create_order(create_customer_address):
    def do_create_order(customer: Customer) -> Order:
        customer_address = create_customer_address(customer)
        serialized_customer_address = CustomerAddressSerializer(customer_address).data
        order_address = OrderAddress.objects.create(**serialized_customer_address)
        order = baker.make(Order, customer=customer, address=order_address)
        return order

    return do_create_order
