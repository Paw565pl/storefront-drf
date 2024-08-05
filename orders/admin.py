from django.contrib import admin
from django_admin_inline_paginator.admin import TabularInlinePaginated

from orders.models import (
    Customer,
    CustomerAddress,
    Cart,
    CartItem,
    OrderAddress,
    Order,
    OrderItem,
)

# Register your models here.
admin.site.register(CustomerAddress)
admin.site.register(OrderAddress)


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_select_related = ["user"]
    readonly_fields = ["user", "address"]

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("user", "address")


class CartItemInline(TabularInlinePaginated):
    model = CartItem
    readonly_fields = ["product", "quantity", "total_price"]
    per_page = 10

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("product")

    def has_add_permission(self, *args, **kwargs):
        return False


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    inlines = [CartItemInline]
    readonly_fields = ["updated_at", "total_price"]
    list_display = ["id", "total_price"]
    list_filter = ["updated_at"]


class OrderItemInline(TabularInlinePaginated):
    model = OrderItem
    readonly_fields = ["product", "quantity", "total_price"]
    per_page = 10

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("product")

    def has_add_permission(self, *args, **kwargs):
        return False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]
    readonly_fields = ["customer", "address", "created_at", "updated_at", "total_price"]
    list_display = ["id", "customer", "status", "total_price"]
    list_filter = ["status", "created_at", "updated_at"]
    search_fields = ["customer__user__username__istartswith"]
    search_help_text = "Search orders by customer's username"

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("customer__user", "address")
