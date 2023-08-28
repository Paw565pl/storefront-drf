from django.urls import path, include
from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()
router.register(r"products", views.ProductViewSet, basename="products")
router.register(r"collections", views.CollectionViewSet)
router.register(r"carts", views.CartViewSet)
router.register(r"customers", views.CustomerViewSet)
router.register(r"orders", views.OrderViewSet, basename="orders")

product_router = routers.NestedDefaultRouter(router, r"products", lookup="product")
product_router.register(r"reviews", views.ReviewViewSet, basename="product-reviews")
product_router.register(r"images", views.ProductImageViewSet, basename="product-images")

cart_router = routers.NestedDefaultRouter(router, r"carts", lookup="cart")
cart_router.register(r"items", views.CartItemViewSet, basename="cart-items")

urlpatterns = [
    path(
        "customers/me",
        views.CustomerProfileViewSet.as_view(),
        name="customer-profile",
    ),
    path("", include(router.urls)),
    path("", include(product_router.urls)),
    path("", include(cart_router.urls)),
]
