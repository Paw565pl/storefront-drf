from django.db.models import Count, Q
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet

from core.exceptions import Conflict
from likes.models import LikeDislike
from likes.views import LikeDislikeView
from products.filters import ProductFilter, ReviewFilter
from products.mixins import MultipleFieldLookupMixin
from products.models import Product, ProductImage, Review, Collection
from products.permissions import IsAdminOrReadOnly, IsAuthorOrReadOnly
from products.serializers import (
    ProductSerializer,
    ProductImageSerializer,
    ReviewSerializer,
    CollectionSerializer,
)
from products.utils import get_product_or_404


# Create your views here.
class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.prefetch_related("product_set").all()
    serializer_class = CollectionSerializer
    permission_classes = [IsAdminOrReadOnly]
    ordering_fields = ["title"]

    @method_decorator([cache_page(60 * 5), vary_on_cookie])
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        collection = self.get_object()
        if Product.objects.filter(collection=collection).exists():
            raise Conflict(
                "Collection can not be deleted because it is associated with one or more products."
            )
        return super().destroy(request, *args, **kwargs)


class ProductViewSet(MultipleFieldLookupMixin, ModelViewSet):
    queryset = (
        Product.objects.select_related("collection")
        .prefetch_related("promotions")
        .prefetch_related("productimage_set")
        .prefetch_related("likes_dislikes")
        .annotate(
            likes_count=Count(
                "likes_dislikes", filter=Q(likes_dislikes__vote=LikeDislike.LIKE)
            ),
            dislikes_count=Count(
                "likes_dislikes", filter=Q(likes_dislikes__vote=LikeDislike.DISLIKE)
            ),
        )
        .all()
    )
    serializer_class = ProductSerializer
    permission_classes = [IsAdminOrReadOnly]
    filterset_class = ProductFilter
    lookup_fields = ["id", "slug"]
    ordering_fields = [
        "title",
        "unit_price",
        "inventory",
        "last_update",
        "likes_count",
        "dislikes_count",
    ]


class ProductImageViewSet(ModelViewSet):
    serializer_class = ProductImageSerializer
    permission_classes = [IsAdminOrReadOnly]
    ordering_fields = []

    def get_queryset(self):
        product_identifier = self.kwargs["product_pk"]
        product = get_product_or_404(product_identifier)
        return ProductImage.objects.filter(product=product).order_by("id")

    def create(self, request, *args, **kwargs):
        product_identifier = self.kwargs["product_pk"]
        get_product_or_404(product_identifier)
        return super().create(request, *args, **kwargs)


class ProductReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    filterset_class = ReviewFilter
    ordering_fields = [
        "rating",
        "created_at",
        "likes_count",
        "dislikes_count",
    ]

    def get_queryset(self):
        product_identifier = self.kwargs["product_pk"]
        product = get_product_or_404(product_identifier)

        return (
            Review.objects.filter(product=product)
            .prefetch_related("likes_dislikes")
            .annotate(
                likes_count=Count(
                    "likes_dislikes", filter=Q(likes_dislikes__vote=LikeDislike.LIKE)
                ),
                dislikes_count=Count(
                    "likes_dislikes", filter=Q(likes_dislikes__vote=LikeDislike.DISLIKE)
                ),
            )
            .order_by("-created_at")
            .all()
        )

    def create(self, request, *args, **kwargs):
        product_identifier = self.kwargs["product_pk"]
        get_product_or_404(product_identifier)
        return super().create(request, *args, **kwargs)


class ProductLikeDislikeView(LikeDislikeView):
    content_object_queryset = Product.objects.all()
    integrity_error_message = "You have already liked or disliked this product."

    def get_content_object_id(self, *args, **kwargs):
        product_identifier = self.kwargs["product_pk"]
        product = get_product_or_404(product_identifier)
        return product.id


class ProductReviewLikeDislikeView(LikeDislikeView):
    content_object_queryset = Review.objects.all()
    integrity_error_message = "You have already liked or disliked this review."
