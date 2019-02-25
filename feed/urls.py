from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('sources/', views.rest_sources, name='rest-sources'),
    re_path(r'^sources/(?P<pk>[0-9]+)/$', views.rest_sources_detail, name='rest-sources-detail'),
    path('items/', views.rest_items, name='rest-items')
]