from django.urls import path

from apps.dashboard.views import DashboardViews

urlpatterns = [
    path('', DashboardViews.dashboard, name='dashboard'),
    path('events/', DashboardViews.events, name='events'),
    path('artists/', DashboardViews.artists, name='artists'),
]