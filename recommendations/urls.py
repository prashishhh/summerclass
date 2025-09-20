from django.urls import path
from . import views

app_name = 'recommendations'

urlpatterns = [
    path('recently-viewed/<int:user_id>/', views.recently_viewed, name='recently_viewed'),
    path('also-bought/<int:product_id>/', views.also_bought, name='also_bought'),
    path('trending/', views.trending, name='trending'),
]
