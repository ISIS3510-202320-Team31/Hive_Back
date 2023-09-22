"""hive_back URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path
from event.views import index_list as event_index_list, index_detail as event_index_detail
from user.views import index_list as user_index_list#, index_detail as event_index_detail

urlpatterns = [
    path('admin/', admin.site.urls),
    path('events/', event_index_list, name='event_list'),
    path('events/<str:pk>/', event_index_detail, name='event_detail'),
    path('users/', user_index_list, name='user_list'),
]
