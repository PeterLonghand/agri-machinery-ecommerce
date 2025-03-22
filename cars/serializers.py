from rest_framework import serializers
from .models import (
    Machinery, Tractor, Harvester, SelfPropelledSprayer,
    Plow, Seeder, Harrow, TrailedSprayer, Mower, Baler
)

class MachinerySerializer(serializers.ModelSerializer):
    machinery_type_display = serializers.CharField(source='get_machinery_type_display')
    condition_display = serializers.CharField(source='get_condition_display')
    
    class Meta:
        model = Machinery
        fields = [
            'id', 'manufacturer', 'model_name', 'machinery_type', 
            'machinery_type_display', 'year', 'price', 'condition',
            'condition_display', 'description', 'photo', 'photo_1',
            'photo_2', 'photo_3', 'photo_4', 'created_date'
        ]

class TractorSerializer(MachinerySerializer):
    drive_type_display = serializers.CharField(source='get_drive_type_display')
    transmission_type_display = serializers.CharField(source='get_transmission_type_display')
    tow_class_display = serializers.CharField(source='get_tow_class_display')
    
    class Meta(MachinerySerializer.Meta):
        model = Tractor
        fields = MachinerySerializer.Meta.fields + [
            'drive_type', 'drive_type_display', 'power',
            'engine_volume', 'transmission_type', 'transmission_type_display',
            'tow_class', 'tow_class_display'
        ]

class HarvesterSerializer(MachinerySerializer):
    threshing_type_display = serializers.CharField(source='get_threshing_type_display')
    
    class Meta(MachinerySerializer.Meta):
        model = Harvester
        fields = MachinerySerializer.Meta.fields + [
            'power', 'engine_volume', 'bunker_volume',
            'threshing_type', 'threshing_type_display'
        ]

class SelfPropelledSprayerSerializer(MachinerySerializer):
    class Meta(MachinerySerializer.Meta):
        model = SelfPropelledSprayer
        fields = MachinerySerializer.Meta.fields + [
            'power', 'engine_volume', 'width', 'tank_capacity'
        ]

class PlowSerializer(MachinerySerializer):
    class Meta(MachinerySerializer.Meta):
        model = Plow
        fields = MachinerySerializer.Meta.fields + [
            'width', 'bodies', 'reversible', 'weight', 'min_power'
        ]

class SeederSerializer(MachinerySerializer):
    seed_type_display = serializers.CharField(source='get_seed_type_display')
    class Meta(MachinerySerializer.Meta):
        model = Seeder
        fields = MachinerySerializer.Meta.fields + [
            'width', 'seed_tank_capacity', 'fert_tank_capacity', 'seed_type',
            'seed_type_display'
        ]

class HarrowSerializer(MachinerySerializer):
    harrow_type_display = serializers.CharField(source='get_harrow_type_display')
    
    class Meta(MachinerySerializer.Meta):
        model = Harrow
        fields = MachinerySerializer.Meta.fields + [
            'width', 'harrow_type', 'harrow_type_display'
        ]

class TrailedSprayerSerializer(MachinerySerializer):
    class Meta(MachinerySerializer.Meta):
        model = TrailedSprayer
        fields = MachinerySerializer.Meta.fields + [
            'width', 'tank_capacity'
        ]

class MowerSerializer(MachinerySerializer):
    class Meta(MachinerySerializer.Meta):
        model = Mower
        fields = MachinerySerializer.Meta.fields + [
            'width'
        ]

class BalerSerializer(MachinerySerializer):
    baler_type_display = serializers.CharField(source='get_baler_type_display')
    bale_size_display = serializers.CharField(source='get_bale_size_display')
    
    class Meta(MachinerySerializer.Meta):
        model = Baler
        fields = MachinerySerializer.Meta.fields + [
            'baler_type', 'baler_type_display', 'bale_size',
            'bale_size_display', 'productivity', 'min_power', 'width'
        ]