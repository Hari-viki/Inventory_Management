from django.urls import path
from .views import CreateItemView, ReadItemView, UpdateItemView, DeleteItemView

urlpatterns = [
    path('items/', CreateItemView.as_view(), name='create-item'),
    path('items/<int:pk>/', ReadItemView.as_view(), name='read-item'),
    path('items/<int:pk>/update/', UpdateItemView.as_view(), name='update-item'),
    path('items/<int:pk>/delete/', DeleteItemView.as_view(), name='delete-item'),
]
