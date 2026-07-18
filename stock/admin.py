from django.contrib import admin
from .models import Product, StockIn, Sale, Branch, UserProfile

@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ['name', 'location', 'is_active', 'created_at']
    list_filter = ['location', 'is_active']
    search_fields = ['name', 'location']

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'role', 'branch']
    list_filter = ['role', 'branch']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'mrp', 'dp', 'current_stock', 'stock_status']

@admin.register(StockIn)
class StockInAdmin(admin.ModelAdmin):
    list_display = ['product', 'branch', 'date', 'quantity_in', 'purchase_price', 'supplier']
    list_filter = ['branch', 'date']
    search_fields = ['product__name', 'supplier']

@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ['date', 'customer_name', 'product', 'branch', 'quantity_sold', 'discount_base', 'selling_price', 'payment_pending']
    list_filter = ['branch', 'date', 'discount_base']
    search_fields = ['customer_name', 'product__name']

from .models import CommissionSetting, MonthlyCommission

@admin.register(CommissionSetting)
class CommissionSettingAdmin(admin.ModelAdmin):
    list_display = ['branch', 'branch_type', 'commission_type', 'commission_value', 'effective_from']
    list_filter = ['branch_type', 'commission_type']

@admin.register(MonthlyCommission)
class MonthlyCommissionAdmin(admin.ModelAdmin):
    list_display = ['branch', 'month', 'year', 'total_sales', 'commission_amount', 'amount_paid', 'status']
    list_filter = ['status', 'year', 'branch']

from .models import PayoutLog

@admin.register(PayoutLog)
class PayoutLogAdmin(admin.ModelAdmin):
    list_display = ['monthly_commission', 'sent_at', 'sent_to_email', 'sent_to_mobile', 'email_status', 'sms_status', 'sent_by']
    list_filter  = ['email_status', 'sms_status']
    readonly_fields = ['sent_at']
