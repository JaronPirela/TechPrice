"""
URL configuration for djangoauth project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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

from django.urls import path, include
from admin_panel import views
from django.contrib import admin


urlpatterns = [
    
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.signout, name='logout'),
    path('admin/', views.admin_dashboard, name='admin_dashboard'),
    path('admin_django/', admin.site.urls),
    path('user_list/', views.user_list, name='user_list'),
    path('user_detail/<int:user_id>/', views.user_detail, name='user_detail'),
    path('delete_user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('login/', views.login_admin, name='login'),
    path('login_view/', views.login_view, name='login_view'),
    path('login_admin/', views.login_admin, name='login_admin'),
    path('welcome/', views.welcome, name='welcome'),
    path('edit_user/<int:user_id>/', views.edit_user, name='edit_user'),
    path('', include('scrap.urls')),
    path('', include('chatbot.urls'))
]
