from django.urls import path
from apps.wines.views import wineListAPI, wineDetailsAPI

urlpatterns = [
    path('wines/', wineListAPI, name='wineListAPI'),
    path('wines/<str:wine_id>/', wineDetailsAPI, name='wineDetailsAPI'),  
]