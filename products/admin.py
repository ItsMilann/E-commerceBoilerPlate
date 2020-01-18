from django.contrib import admin
from .models import Product,Refund, OrderProduct, Order, BillingAddress, Payment, OrderStatus

def change_refund_request(modeladmin, request, queryset):
    queryset.update(refund_requested=False, refund_granted=True)
change_refund_request.short_description = 'Accept refund request.'
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'price',
        'discounted_price',
        'description'
    )
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'ordered',
        'reference_code',
        'ordered_date',
        'order_status',
        'billing_address',
        'payment_info'
        
    )
    
    list_display_links = [
        'order_status',
        'billing_address',
        'payment_info'
    ]
    list_filter = [
        'user',
        'ordered',
        'reference_code',
        'ordered_date',
        'billing_address',
    ]

    search_fields = [
        'user',
        'reference_code',

    ]
    actions = [change_refund_request]
class BillingAddressAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'country',
        'street_address',
        
    )
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'payment_method',
        'charge_id',
        'amount',
        'timestamp',

        
    )
class OrderStatusAdmin(admin.ModelAdmin):
    list_display = (
    'user',
    'pre_processing',
    'being_delivered',
    'delivered',
    'refund_requested',
    'refund_granted',       
    )
admin.site.register(Product, ProductAdmin )
admin.site.register(Payment, PaymentAdmin )
admin.site.register(OrderProduct)
admin.site.register(Order, OrderAdmin)
admin.site.register(BillingAddress, BillingAddressAdmin)
admin.site.register(OrderStatus, OrderStatusAdmin)
admin.site.register(Refund)
