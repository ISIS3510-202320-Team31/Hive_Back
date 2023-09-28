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
from event.views import index_list as event_index_list, index_detail as event_index_detail, index_participants as event_index_participants, index_list_by_date as event_index_list_by_date
from user.views import index_list as user_index_list, index_one as user_index_one, index_user_register as user_index_register
from weight.views import index_list as weight_index_list, index_detail as weight_index_detail, index_user as weight_index_user, index_tag as weight_index_tag
from event.views import index_list as event_index_list, index_detail as event_index_detail, index_participants as event_index_participants
from user.views import index_list as user_index_list, index_one as user_index_one, index_events_list as user_index_events_list, index_events_one as user_index_events_one

urlpatterns = [
    path('admin/', admin.site.urls),
    path('events/', event_index_list, name='event_list'),
    path('events/<str:pk>/', event_index_detail, name='event_detail'),
    path('events/<str:pk>/participants/', event_index_participants, name='event_participants'),
    path('events/date/<str:date>/', event_index_list_by_date, name='event_list_by_date'),
    path('users/', user_index_list, name='user_list'),
    path('users/<uuid:user_id>/', user_index_one, name='user_one'),
    path('weights/', weight_index_list, name='weight_list'),
    path('weights/<str:pk>/', weight_index_detail, name='weight_detail'),
    path('users/', user_index_list, name='user_list'),
    path('users/<uuid:user_id>/', user_index_one, name='user_detail'),
    path('users/<uuid:user_id>/events/', user_index_events_list, name='event_by_user'),
    path('users/<uuid:user_id>/events/<uuid:event_id>/', user_index_events_one, name='event_by_user_detail'),
    path('register/', user_index_register, name='user_register')
]
