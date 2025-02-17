from django.urls import path
from apps.wines.views import wineListAPI, wineDetailsAPI, wine_list_by_manager

urlpatterns = [
    path('wines/', wineListAPI, name='wineListAPI'),
    path('mangerWines/', wine_list_by_manager, name='wine-list-by-manager'),
    path('wines/<str:wine_id>/', wineDetailsAPI, name='wineDetailsAPI'),  
]