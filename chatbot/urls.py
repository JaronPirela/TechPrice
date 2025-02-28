from django.urls import path
from . import views

urlpatterns = [
    path('chatbot/', views.chatbot_view, name = 'chatbot'),
    # path('product_detail/', views.product_detail, name='product detail'),
]
