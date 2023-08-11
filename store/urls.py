from django.urls import path, include
from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()
router.register(r"products", views.ProductViewSet)
router.register(r"collections", views.CollectionViewSet)

products_router = routers.NestedDefaultRouter(router, r"products", lookup="product")
products_router.register(r"reviews", views.ReviewViewSet, basename="product-reviews")

urlpatterns = [path("", include(router.urls)), path("", include(products_router.urls))]
