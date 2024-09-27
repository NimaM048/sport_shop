from django.contrib import admin

from . import models
from cart.models import DiscountCode, OrderItem, Order, UserDiscountCode


class OrderItemInline(admin.TabularInline):
    model = OrderItem


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_paid', 'total_price')
    inlines = (OrderItemInline,)
    list_filter = ('is_paid',)
    search_fields = ('user__username',)


@admin.register(DiscountCode)
class DiscountCodeAdmin(admin.ModelAdmin):
    list_display = ('name', 'quantity', 'percentage')
    search_fields = ('name',)
    list_filter = ('quantity',)

class UserDiscountCodeAdmin(admin.ModelAdmin):
    list_display = ('user', 'discount_code')
    list_filter = ('user', 'discount_code')

admin.site.register(UserDiscountCode, UserDiscountCodeAdmin)








