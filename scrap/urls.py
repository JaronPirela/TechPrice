from django.urls import path
from . import views

urlpatterns = [
    path('main/', views.main, name = 'main'),
    # path('product_detail/', views.product_detail, name='product detail'),
]
