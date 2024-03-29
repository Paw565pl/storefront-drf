from rest_framework.routers import SimpleRouter

from products.views import ProductViewSet

router = SimpleRouter()
router.register(r"products", ProductViewSet, basename="products")

urlpatterns = router.urls
