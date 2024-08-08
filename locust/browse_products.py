from random import randint
from uuid import uuid4

from locust import FastHttpUser, task, between


class WebsiteUser(FastHttpUser):
    cart_id: uuid4
    wait_time = between(1, 5)

    @task(5)
    def view_products(self):
        collection_id = randint(2, 10)
        self.client.get(
            f"/api/products/?collection_id={collection_id}/", name="/api/products/"
        )

    @task(4)
    def view_product(self):
        product_id = randint(1, 800)
        self.client.get(f"/api/products/{product_id}/", name="/api/products/:id/")

    @task(3)
    def view_product_reviews(self):
        product_id = randint(1, 800)
        self.client.get(
            f"/api/products/{product_id}/reviews/", name="/api/products/:id/reviews/"
        )

    @task(2)
    def view_collections(self):
        self.client.get("/api/collections/", name="/api/collections/")

    @task(1)
    def view_collection(self):
        collection_id = randint(2, 10)
        self.client.get(
            f"/api/collections/{collection_id}/", name="/api/collections/:id/"
        )

    @task(1)
    def view_cart(self):
        self.client.get(f"/api/carts/{self.cart_id}/", name="/api/carts/:id/")

    @task(3)
    def add_product_to_cart(self):
        product_id = randint(1, 100)

        self.client.post(
            f"/api/carts/{self.cart_id}/items/",
            name="api/carts/:cart_id/items/",
            json={"product_id": product_id, "quantity": 1},
        )

    def on_start(self):
        response = self.client.post("/api/carts/")
        result = response.json()
        self.cart_id = result["id"]
