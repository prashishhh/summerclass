"""
URL configuration for marketplace project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf.urls.static import static 
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'), # Home Page

    # User Pages
    path('register/', views.user_register, name='register'),
    path('login/', views.user_login, name='login'), # Login Page
    path('dashboard/', views.user_dashboard, name='dashboard'), # Dashboard Page
    path('change-password/', views.change_password, name='change_password'), # Change Password page
    path('edit-profile/', views.edit_profile, name='edit-profile'),

    # Cart
    path('cart/', views.cart, name='cart'),

    # Orders
    path('my-orders/', views.my_orders, name='my_orders'),
    path('checkout/', views.checkout, name='checkout'),
    path('place-order/', views.place_order, name='place_order'),
    path('order-complete/', views.order_complete, name='order_complete'),


    path('store/', include('products.urls')), # Products
    path('blog/', include('blog.urls')), # Blog 
    path('pages/', include('pages.urls')), # Pages
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)