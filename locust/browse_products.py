from random import randint
from locust import FastHttpUser, task, between


class WebsiteUser(FastHttpUser):
    wait_time = between(1, 10)

    @task(5)
    def view_products(self):
        collection_id = randint(2, 10)
        self.client.get(
            f"/store/products/?collection_id={collection_id}/", name="/store/products/"
        )

    @task(4)
    def view_product(self):
        product_id = randint(1, 1000)
        self.client.get(f"/store/products/{product_id}/", name="/store/products/:id/")

    @task(2)
    def add_to_cart(self):
        product_id = randint(1, 100)

        self.client.post(
            f"/store/carts/{self.cart_id}/items/",
            name="store/carts/:cart_id/items/",
            json={"product_id": product_id, "quantity": product_id // randint(1, 5)},
        )

    @task(3)
    def main_endpoint(self):
        self.client.get("", name="/")

    @task(1)
    def slow_endpoint(self):
        self.client.get("/playground/slow/", name="/playground/slow/")

    def on_start(self):
        response = self.client.post("/store/carts/")
        result = response.json()
        self.cart_id = result["id"]
