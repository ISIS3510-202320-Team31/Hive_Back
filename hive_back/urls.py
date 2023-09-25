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
from event.views import index_list as event_index_list, index_detail as event_index_detail, index_participants as event_index_participants
from user.views import index_list as user_index_list#, index_detail as event_index_detail
from weight.views import index_list as weight_index_list, index_detail as weight_index_detail, index_user as weight_index_user, index_tag as weight_index_tag

urlpatterns = [
    path('admin/', admin.site.urls),
    path('events/', event_index_list, name='event_list'),
    path('events/<str:pk>/', event_index_detail, name='event_detail'),
    path('events/<str:pk>/participants/', event_index_participants, name='event_participants'),
    path('users/', user_index_list, name='user_list'),
    path('weights/', weight_index_list, name='weight_list'),
    path('weights/<str:pk>/', weight_index_detail, name='weight_detail'),
    path('weights/users/<str:pk>/', weight_index_user, name='weight_user'),
    path('weights/tags/<str:pk>/', weight_index_tag, name='weight_tag'),
]
