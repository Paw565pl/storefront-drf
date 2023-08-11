from django.urls import path, include
from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()
router.register(r"products", views.ProductViewSet, basename="products")
router.register(r"collections", views.CollectionViewSet)
router.register(r"carts", views.CartViewSet)
router.register(r"customers", views.CustomerViewSet)

product_reviews_router = routers.NestedDefaultRouter(
    router, r"products", lookup="product"
)
product_reviews_router.register(
    r"reviews", views.ReviewViewSet, basename="product-reviews"
)

cart_items_router = routers.NestedDefaultRouter(router, r"carts", lookup="cart")
cart_items_router.register(r"items", views.CartItemViewSet, basename="cart-items")

urlpatterns = [
    path("", include(router.urls)),
    path("", include(product_reviews_router.urls)),
    path("", include(cart_items_router.urls)),
]
