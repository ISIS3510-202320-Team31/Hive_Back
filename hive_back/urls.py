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
from event.views import default, index_list as event_index_list, index_detail as event_index_detail, index_list_by_date as event_index_list_by_date, index_list_by_date_and_user as event_index_list_by_date_and_user,events_for_user as events_for_user, index_count_events_by_user as event_index_count_events_by_user, index_list_edit_event as index_list_edit_event, index_list_stats as stats
from user.views import index_list as user_index_list, index_one as user_index_one, index_user_register as user_index_register, index_user_login as user_index_login, index_top_partners as user_index_top_partners
from weight.views import index_list as weight_index_list, index_detail as weight_index_detail, index_user as weight_index_user, index_tag as weight_index_tag
from user.views import index_events_list as user_index_events_list, index_events_one as user_index_events_one, index_events_list_created as user_index_events_list_created, index_top_creators as user_index_top_creators

urlpatterns = [
    path('', default, name='default'),
    path('admin/', admin.site.urls),
    path('events/', event_index_list, name='event_list'),
    path('events/edit/<str:pk>/', index_list_edit_event, name='index_list_edit_event'),
    path('events/<str:pk>/', event_index_detail, name='event_detail'),
    path('events/date/<str:date>/', event_index_list_by_date, name='event_list_by_date'),
    path('events/date/<str:date>/user/<uuid:user_id>/order/<str:future>', event_index_list_by_date_and_user, name='event_list_by_date_and_user'),
    path('events/users/<uuid:user_id>/', events_for_user, name='events_for_user'),
    path('events/users/<uuid:user_id>/participation/', event_index_count_events_by_user, name='event_count_by_user'),
    path('events/users/<uuid:user_id>/createdby/', user_index_events_list_created, name='event_list_created_by_user'),
    path('users/', user_index_list, name='user_list'),
    path('users/<uuid:user_id>/', user_index_one, name='user_one'),
    path('weights/', weight_index_list, name='weight_list'),
    path('weights/<str:pk>/', weight_index_detail, name='weight_detail'),
    path('users/', user_index_list, name='user_list'),
    path('users/<uuid:user_id>/', user_index_one, name='user_detail'),
    path('users/<uuid:user_id>/events/', user_index_events_list, name='event_by_user'),
    path('users/<uuid:user_id>/events/<uuid:event_id>/', user_index_events_one, name='event_by_user_detail'),
    path('register/', user_index_register, name='user_register'),
    path('login/', user_index_login, name='user_login'),
    path('top_creators/', user_index_top_creators, name='top_creators'),
    path('users/<uuid:user_id>/partners/',user_index_top_partners, name='top_partners'),
    path('users/<uuid:user_id>/stats', stats, name='stats')
]
