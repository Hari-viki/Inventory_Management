from django.shortcuts import render,get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import Inventory_Management
from .serializer import Inventory_Management_Serializer
from django.core.cache import cache
from rest_framework import status,generics
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
import logging
# Create your views here.
logger = logging.getLogger(__name__)

class CreateItemView(generics.CreateAPIView):
    queryset = Inventory_Management.objects.all()
    serializer_class = Inventory_Management_Serializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if Inventory_Management.objects.filter(name=request.data.get('name')).exists():
            return Response({"error": "Item already exists"}, status=status.HTTP_400_BAD_REQUEST)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ReadItemView(generics.RetrieveAPIView):
    queryset = Inventory_Management.objects.all()
    serializer_class = Inventory_Management_Serializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        item_id = kwargs.get('pk')
        item = cache.get(f'item_{item_id}')

        if not item:
            try:
                item = self.get_object()
                cache.set(f'item_{item_id}', item, timeout=60*15)  # Cache for 15 mins
            except Inventory_Management.DoesNotExist:
                return Response({"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(item)
        return Response(serializer.data)


class UpdateItemView(generics.UpdateAPIView):
    queryset = Inventory_Management.objects.all()
    serializer_class = Inventory_Management_Serializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)  
        item = self.get_object() 

        serializer = self.get_serializer(item, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True) 

        self.perform_update(serializer)  

        item_id = kwargs.get('pk')
        cache.set(f'item_{item_id}', item, timeout=60*15)  

        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()

class DeleteItemView(generics.DestroyAPIView):
    queryset = Inventory_Management.objects.all()
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        item_id = kwargs.get('pk')
        try:
            item = self.get_object()
        except Inventory_Management.DoesNotExist:
            return Response({"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND)

        self.perform_destroy(item)
        cache.delete(f'item_{item_id}')  # Remove from cache
        return Response({"message": "Item deleted"}, status=status.HTTP_204_NO_CONTENT)