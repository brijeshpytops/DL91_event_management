from django.urls import path

from apps.dashboard.views import AuthViews, DashboardViews

urlpatterns = [
    path('register/', AuthViews.register, name='register'),
    path('email-verification/', AuthViews.verify_email, name='verify_email'),
    path('login/', AuthViews.login, name='login'),
    path('logout/', AuthViews.logout, name='logout'),
    path('', DashboardViews.dashboard, name='dashboard'),

    # path('events/', DashboardViews.events, name='events'),
    # path('artists/', DashboardViews.artists, name='artists'),
]