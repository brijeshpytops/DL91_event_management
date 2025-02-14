from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from apps.wines.models import Wine
from apps.wines.serializers import WineSerializer

@api_view(['GET', 'POST'])
def wineListAPI(request):
    if request.method == 'GET':
        querySet = Wine.objects.all()
        serializer = WineSerializer(querySet, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    
    if request.method == 'POST':
        serializer = WineSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def wineDetailsAPI(request, wine_id):
    try:
        wine = Wine.objects.get(pk=wine_id)
    except:
        return Response({'Message': "Wine not found"}, status=status.HTTP_404_NOT_FOUND)


    if request.method == 'GET':
        serializer = WineSerializer(wine)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    if request.method == 'PUT':
        serializer = WineSerializer(wine, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'PATCH':
        serializer = WineSerializer(wine, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    
    if request.method == 'DELETE':
        wine.delete()
        return Response({'Message': 'Wine deleted'}, status=status.HTTP_204_NO_CONTENT)