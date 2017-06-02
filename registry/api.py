import models
import serializers
from rest_framework import viewsets, permissions


class RegistryViewSet(viewsets.ModelViewSet):
    """ViewSet for the Registry class"""

    queryset = models.Registry.objects.all()
    serializer_class = serializers.RegistrySerializer
    permission_classes = [permissions.IsAuthenticated]


class ItemViewSet(viewsets.ModelViewSet):
    """ViewSet for the Item class"""

    queryset = models.Item.objects.all()
    serializer_class = serializers.ItemSerializer
    permission_classes = [permissions.IsAuthenticated]


class RegistryItemViewSet(viewsets.ModelViewSet):
    """ViewSet for the RegistryItem class"""

    queryset = models.RegistryItem.objects.all()
    serializer_class = serializers.RegistryItemSerializer
    permission_classes = [permissions.IsAuthenticated]


