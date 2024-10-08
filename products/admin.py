from django.contrib import admin, messages
from django.db.models import QuerySet, Count, Q
from django.urls import reverse
from django.utils.html import format_html
from django.utils.http import urlencode
from django_admin_inline_paginator.admin import TabularInlinePaginated

from products.models import Product, ProductImage, Collection, Review, Promotion
from votes.models import Vote


# Register your models here.
class InventoryFilter(admin.SimpleListFilter):
    title = "Inventory"
    parameter_name = "inventory"

    def lookups(self, request, model_admin):
        return ("<10", "Low"), (">=10", "Ok")

    def queryset(self, request, queryset: QuerySet):
        if self.value() == "<10":
            return queryset.filter(inventory__lt=10)
        elif self.value() == ">=10":
            return queryset.filter(inventory__gte=10)


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    readonly_fields = ["products_count"]
    search_fields = ["title__icontains"]
    list_display = ["title", "products_count"]
    list_per_page = 20

    @admin.display(ordering="products_count")
    def products_count(self, collection: Collection):
        url = (
            reverse("admin:products_product_changelist")
            + "?"
            + urlencode({"collection_id": str(collection.id)})
        )
        return format_html("<a href='{}'>{}</a>", url, collection.products_count)  # noqa

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(products_count=Count("product"))


class ProductImageInline(TabularInlinePaginated):
    model = ProductImage
    readonly_fields = ["thumbnail"]

    per_page = 3
    extra = 1

    @staticmethod
    def thumbnail(instance: ProductImage):
        if instance.image.name != "":
            return format_html(f"<img src='{instance.image.url}' width='50px'/>")
        return ""


class ProductReviewInline(TabularInlinePaginated):
    model = Review
    readonly_fields = ["author", "created_at"]

    per_page = 3
    extra = 1


class PromotionFilter(admin.SimpleListFilter):
    title = "Promotion discount"
    parameter_name = "discount"

    def lookups(self, request, model_admin):
        return (
            ("0-19", "0-19 %"),
            ("20-39", "20-39 %"),
            ("40-59", "40-59 %"),
            ("60-79", "60-79 %"),
            ("80-100", "80-100 %"),
        )

    def queryset(self, request, queryset: QuerySet):
        if self.value() == "0-19":
            return queryset.filter(discount__lte=19)
        elif self.value() == "20-39":
            return queryset.filter(discount__range=(20, 39))
        elif self.value() == "40-59":
            return queryset.filter(discount__range=(40, 59))
        elif self.value() == "60-79":
            return queryset.filter(discount__range=(60, 79))
        elif self.value() == "80-100":
            return queryset.filter(discount__range=(80, 100))


@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    readonly_fields = ["products_count"]
    search_fields = ["name__icontains"]
    list_per_page = 20
    list_display = ["name", "discount", "products_count"]
    list_filter = [PromotionFilter]

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(products_count=Count("product"))

    @admin.display(ordering="products_count")
    def products_count(self, promotion):
        return promotion.products_count


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    readonly_fields = ["slug", "last_update", "likes_count", "dislikes_count"]
    inlines = [ProductImageInline, ProductReviewInline]
    search_fields = ["title__icontains"]
    autocomplete_fields = ["collection", "promotions"]
    actions = ["clear_inventory"]
    list_per_page = 20
    list_display = ["title", "unit_price", "inventory_status", "collection_title"]
    list_filter = ["collection", "last_update", InventoryFilter, PromotionFilter]
    list_select_related = ["collection"]

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .prefetch_related("promotions", "productimage_set")
            .annotate(
                likes_count=Count("votes", filter=Q(votes__value=Vote.LIKE)),
                dislikes_count=Count("votes", filter=Q(votes__value=Vote.DISLIKE)),
            )
        )

    @admin.display(ordering="inventory")
    def inventory_status(self, product):
        if product.inventory < 10:
            return "Low"
        return "Ok"

    @staticmethod
    def collection_title(product):
        return product.collection.title

    @staticmethod
    def likes_count(product):
        return product.likes_count

    @staticmethod
    def dislikes_count(product):
        return product.dislikes_count

    @admin.action(description="Clear inventory")
    def clear_inventory(self, request, queryset: QuerySet):
        updated_count = queryset.update(inventory=0)
        self.message_user(
            request,
            f"{updated_count} products were successfully updated",
            messages.SUCCESS,
        )


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    readonly_fields = ["author", "product", "likes_count", "dislikes_count"]
    search_fields = ["author__username__icontains"]
    list_per_page = 20
    list_display = ["author", "product", "rating", "created_at"]
    list_filter = ["created_at"]
    list_select_related = ["product", "author"]

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .annotate(
                likes_count=Count("votes", filter=Q(votes__value=Vote.LIKE)),
                dislikes_count=Count("votes", filter=Q(votes__value=Vote.DISLIKE)),
            )
        )

    @staticmethod
    def likes_count(review):
        return review.likes_count

    @staticmethod
    def dislikes_count(review):
        return review.dislikes_count
