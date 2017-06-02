import models

from rest_framework import serializers


class RegistrySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Registry
        fields = (
            'slug', 
            'name', 
            'created', 
            'last_updated', 
            'id', 
        )


class ItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Item
        fields = (
            'slug', 
            'name', 
            'created', 
            'last_updated', 
            'url', 
            'img_url', 
            'id', 
            'description', 
        )


class RegistryItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.RegistryItem
        fields = (
            'slug', 
            'name', 
            'created', 
            'last_updated', 
            'bought_by', 
            'message', 
            'bought', 
            'price_from_vendor', 
            'price_display', 
            'vendor', 
        )


