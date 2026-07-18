from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('switch-branch/<int:pk>/', views.switch_branch, name='switch_branch'),

    path('stock-in/', views.stock_in_list, name='stockin_list'),
    path('stock-in/add/', views.stock_in_add, name='stockin_add'),
    path('stock-in/edit/<int:pk>/', views.stock_in_edit, name='stockin_edit'),
    path('stock-in/delete/<int:pk>/', views.stock_in_delete, name='stockin_delete'),

    path('sales/', views.sale_list, name='sale_list'),
    path('sales/add/', views.sale_add, name='sale_add'),
    path('sales/edit/<int:pk>/', views.sale_edit, name='sale_edit'),
    path('sales/delete/<int:pk>/', views.sale_delete, name='sale_delete'),
    path('sales/invoice/<int:pk>/', views.sale_invoice, name='sale_invoice'),
    path('sales/invoice/bulk/', views.sale_invoice_bulk, name='sale_invoice_bulk'),

    path('alerts/', views.stock_alert, name='stock_alert'),

    path('products/', views.product_list, name='product_list'),
    path('products/add/', views.product_add, name='product_add'),
    path('products/edit/<int:pk>/', views.product_edit, name='product_edit'),

    path('branches/', views.branch_list, name='branch_list'),
    path('branches/add/', views.branch_add, name='branch_add'),
    path('branches/edit/<int:pk>/', views.branch_edit, name='branch_edit'),
    path('branches/delete/<int:pk>/', views.branch_delete, name='branch_delete'),
    path('branches/<int:pk>/assign/', views.branch_assign_user, name='branch_assign_user'),
    path('branches/<int:branch_pk>/remove-user/<int:user_pk>/', views.branch_remove_user, name='branch_remove_user'),

    path('commission/', views.commission_dashboard, name='commission_dashboard'),
    path('commission/my/', views.commission_my_view, name='commission_my_view'),
    path('commission/generate-all/', views.commission_generate_all, name='commission_generate_all'),
    path('commission/export/', views.commission_export_excel, name='commission_export_excel'),
    path('commission/payout/all/', views.commission_payout_all, name='commission_payout_all'),
    path('commission/payout/<int:pk>/', views.commission_payout_single, name='commission_payout_single'),
    path('commission/payout-logs/', views.payout_log_list, name='payout_log_list'),
    path('commission/branch/<int:branch_pk>/', views.commission_branch_detail, name='commission_branch_detail'),
    path('commission/branch/<int:branch_pk>/setting/', views.commission_setting, name='commission_setting'),
    path('commission/branch/<int:branch_pk>/generate/', views.commission_generate, name='commission_generate'),
    path('commission/pay/<int:pk>/', views.commission_pay, name='commission_pay'),
    path('branches/<int:pk>/bank/', views.branch_bank_details, name='branch_bank_details'),
    path('my-branch-details/', views.branch_my_details, name='branch_my_details'),
]
