# serializers.py

from rest_framework import serializers
from .models import Vehicle

class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = ['id', 'owner', 'license_plate', 'vehicle_type', 'latitude', 'longitude']
