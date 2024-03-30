import pytest
from model_bakery import baker

from products.models import Collection, Product


@pytest.fixture
def create_product():
    collection = baker.make(Collection)
    product = baker.make(Product, collection=collection)
    return product


@pytest.fixture
def create_collection():
    collection = baker.make(Collection)
    return collection
