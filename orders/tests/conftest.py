import pytest
from model_bakery import baker

from orders.models import CustomerAddress, Customer, Cart, CartItem


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
    def do_create_cart_item(cart: Cart, item_quantity: int) -> CartItem:
        cart_item = baker.make(CartItem, cart=cart, quantity=item_quantity)
        return cart_item

    return do_create_cart_item
