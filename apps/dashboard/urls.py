from django.urls import path

from apps.dashboard.views import AuthViews, DashboardViews

urlpatterns = [
    path('register/', AuthViews.register, name='register'),
    path('email-verification/', AuthViews.verify_email, name='verify_email'),
    path('', AuthViews.login, name='login'),
    path('forgot-password/', AuthViews.forgot_password, name='forgot_password'),
    path('reset-password/<str:manager_id>', AuthViews.reset_password, name='reset_password'),
    path('logout/', AuthViews.logout, name='logout'),
    path('dashboard/', DashboardViews.dashboard, name='dashboard'),
    path('events/', DashboardViews.events, name='events'),
    path('artists/', DashboardViews.artists, name='artists'),
    path('profile/', DashboardViews.profile, name='profile')

    # path('events/', DashboardViews.events, name='events'),
    # path('artists/', DashboardViews.artists, name='artists'),
]