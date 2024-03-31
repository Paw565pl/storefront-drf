import pytest
from model_bakery import baker

from products.models import Collection, Product, ProductImage, Review


@pytest.fixture
def create_collection():
    collection = baker.make(Collection)
    return collection


@pytest.fixture
def create_product(create_collection):
    product = baker.make(Product, collection=create_collection)
    return product


@pytest.fixture
def create_product_image(create_product):
    image = baker.make(ProductImage, product=create_product, _create_files=True)
    return image


@pytest.fixture
def create_product_review(create_product):
    review = baker.make(Review, product=create_product)
    return review
