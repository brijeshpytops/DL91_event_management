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
     path('generate_event_tickets/<str:event_id>/', DashboardViews.generate_event_tickets, name='generate_event_tickets'),
    path('artists/', DashboardViews.artists, name='artists'),
    path('view_artist/<str:artist_id>', DashboardViews.view_artist, name='view_artist'),
    path('delete_artist/<str:artist_id>', DashboardViews.delete_artist, name='delete_artist'),
    path('edit_artist/<str:artist_id>', DashboardViews.edit_artist, name='edit_artist'),
    path('venues_view/', DashboardViews.venues_view, name='venues_view'),
    path('things_view/', DashboardViews.things_view, name='things_view'),
    path('profile/', DashboardViews.profile, name='profile')

    # path('events/', DashboardViews.events, name='events'),
    # path('artists/', DashboardViews.artists, name='artists'),
]