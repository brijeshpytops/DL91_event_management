from django.urls import path

from apps.dashboard.views import AuthViews, DashboardViews

urlpatterns = [
    path('register/', AuthViews.register, name='register'),
    path('', DashboardViews.dashboard, name='dashboard'),
    # path('events/', DashboardViews.events, name='events'),
    # path('artists/', DashboardViews.artists, name='artists'),
]