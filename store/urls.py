from django.urls import path, include
from rest_framework.routers import SimpleRouter
from . import views

router = SimpleRouter()
router.register(r"products", views.ProductViewSet)
router.register(r"collections", views.CollectionViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
