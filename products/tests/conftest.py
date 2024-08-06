from shutil import rmtree

import pytest
from model_bakery import baker

from products.models import ProductImage, Review


@pytest.fixture
def product_image(product, create_image_file) -> ProductImage:
    file = create_image_file()

    image = baker.make(ProductImage, product=product, image=file)
    return image


@pytest.fixture
def product_review(product) -> Review:
    review = baker.make(Review, product=product)
    return review


@pytest.fixture(scope="session", autouse=True)
def remove_mock_images():
    yield remove_mock_images
    rmtree("media/test")
