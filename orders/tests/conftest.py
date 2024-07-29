import pytest
from model_bakery import baker

from orders.models import CustomerAddress, Customer


@pytest.fixture
def create_customer_address():
    def go(customer: Customer) -> CustomerAddress:
        customer_address = baker.make(CustomerAddress, phone_number="+44123456789")
        customer.address = customer_address
        customer.save()
        return customer_address

    return go
