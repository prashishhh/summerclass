from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('login/', views.user_login, name='user_login'),
    path('register/', views.user_register, name='user_register'),
    path('logout/', views.user_logout, name='user_logout'),
    
    path('activate/<uidb64>/<token>/', views.account_activate, name="account_activate"),
    
    path('dashboard/', views.user_dashboard, name='user_dashboard'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path("my-products/", views.my_products, name="my_products"),
    path("product/<int:product_id>/edit/", views.edit_product, name="edit_product"),
    path("product/<int:product_id>/delete/", views.delete_product, name="delete_product"),
    path("add-product/", views.add_product, name="add_product"),
    path('my-orders/', views.my_orders, name='my_orders'),
    path("order-detail/<int:order_id>/", views.order_detail, name="order_detail"),
    path("my-sales/", views.my_sales, name="my_sales"),
    path('my-sales/<int:order_product_id>/status/', views.update_delivery_status, name='seller_update_delivery_status'),
    path('change-password/', views.change_password, name='change_password'),
    
    # Password Reset URLs
    path('password-reset/', views.CustomPasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='accounts/password_reset_done.html'
    ), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', views.CustomPasswordResetConfirmView.as_view(), 
         name='password_reset_confirm'),
    path('password-reset/complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='accounts/password_reset_complete.html'
    ), name='password_reset_complete'),
]
