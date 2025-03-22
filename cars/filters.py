import django_filters
from django.db.models import Q
from .models import (
    Machinery, Tractor, Harvester, SelfPropelledSprayer,
    Plow, Seeder, Harrow, TrailedSprayer, Mower, Baler
)

class MachineryFilter(django_filters.FilterSet):
    manufacturer = django_filters.CharFilter(lookup_expr='iexact')
    manufacturer_in = django_filters.CharFilter(method='filter_manufacturer_in')
    price_min = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    price_max = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    year_min = django_filters.NumberFilter(field_name='year', lookup_expr='gte')
    year_max = django_filters.NumberFilter(field_name='year', lookup_expr='lte')
    condition = django_filters.CharFilter(lookup_expr='iexact')
    condition_in = django_filters.CharFilter(method='filter_condition_in')
    
    def filter_manufacturer_in(self, queryset, name, value):
        manufacturers = value.split(',')
        return queryset.filter(manufacturer__in=manufacturers)
    
    def filter_condition_in(self, queryset, name, value):
        conditions = value.split(',')
        return queryset.filter(condition__in=conditions)
    
    class Meta:
        model = Machinery
        fields = ['manufacturer', 'price', 'year', 'condition']

class TractorFilter(MachineryFilter):
    drive_type = django_filters.CharFilter(lookup_expr='iexact')
    drive_type_in = django_filters.CharFilter(method='filter_drive_type_in')
    power_min = django_filters.NumberFilter(field_name='power', lookup_expr='gte')
    power_max = django_filters.NumberFilter(field_name='power', lookup_expr='lte')
    engine_volume_min = django_filters.NumberFilter(field_name='engine_volume', lookup_expr='gte')
    engine_volume_max = django_filters.NumberFilter(field_name='engine_volume', lookup_expr='lte')
    transmission_type = django_filters.CharFilter(lookup_expr='iexact')
    transmission_type_in = django_filters.CharFilter(method='filter_transmission_type_in')
    tow_class = django_filters.NumberFilter(lookup_expr='exact')
    tow_class_in = django_filters.CharFilter(method='filter_tow_class_in')
    
    def filter_drive_type_in(self, queryset, name, value):
        drive_types = value.split(',')
        return queryset.filter(drive_type__in=drive_types)
    
    def filter_transmission_type_in(self, queryset, name, value):
        transmission_types = value.split(',')
        return queryset.filter(transmission_type__in=transmission_types)
    
    def filter_tow_class_in(self, queryset, name, value):
        tow_classes = [float(x) for x in value.split(',')]
        return queryset.filter(tow_class__in=tow_classes)
    
    class Meta(MachineryFilter.Meta):
        model = Tractor
        fields = MachineryFilter.Meta.fields + [
            'drive_type', 'power', 'engine_volume', 
            'transmission_type', 'tow_class'
        ]

class HarvesterFilter(MachineryFilter):
    power_min = django_filters.NumberFilter(field_name='power', lookup_expr='gte')
    power_max = django_filters.NumberFilter(field_name='power', lookup_expr='lte')
    engine_volume_min = django_filters.NumberFilter(field_name='engine_volume', lookup_expr='gte')
    engine_volume_max = django_filters.NumberFilter(field_name='engine_volume', lookup_expr='lte')
    bunker_volume_min = django_filters.NumberFilter(field_name='bunker_volume', lookup_expr='gte')
    bunker_volume_max = django_filters.NumberFilter(field_name='bunker_volume', lookup_expr='lte')
    threshing_type = django_filters.CharFilter(lookup_expr='iexact')
    threshing_type_in = django_filters.CharFilter(method='filter_threshing_type_in')
    
    def filter_threshing_type_in(self, queryset, name, value):
        threshing_types = value.split(',')
        return queryset.filter(threshing_type__in=threshing_types)
    
    class Meta(MachineryFilter.Meta):
        model = Harvester
        fields = MachineryFilter.Meta.fields + [
            'power', 'engine_volume', 'bunker_volume', 'threshing_type'
        ]

class SelfPropelledSprayerFilter(MachineryFilter):
    power_min = django_filters.NumberFilter(field_name='power', lookup_expr='gte')
    power_max = django_filters.NumberFilter(field_name='power', lookup_expr='lte')
    engine_volume_min = django_filters.NumberFilter(field_name='engine_volume', lookup_expr='gte')
    engine_volume_max = django_filters.NumberFilter(field_name='engine_volume', lookup_expr='lte')
    width_min = django_filters.NumberFilter(field_name='width', lookup_expr='gte')
    width_max = django_filters.NumberFilter(field_name='width', lookup_expr='lte')
    tank_capacity_min = django_filters.NumberFilter(field_name='tank_capacity', lookup_expr='gte')
    tank_capacity_max = django_filters.NumberFilter(field_name='tank_capacity', lookup_expr='lte')
    
    class Meta(MachineryFilter.Meta):
        model = SelfPropelledSprayer
        fields = MachineryFilter.Meta.fields + [
            'power', 'engine_volume', 'width', 'tank_capacity'
        ]

class PlowFilter(MachineryFilter):
    width_min = django_filters.NumberFilter(field_name='width', lookup_expr='gte')
    width_max = django_filters.NumberFilter(field_name='width', lookup_expr='lte')
    bodies_min = django_filters.NumberFilter(field_name='bodies', lookup_expr='gte')
    bodies_max = django_filters.NumberFilter(field_name='bodies', lookup_expr='lte')
    reversible = django_filters.BooleanFilter()
    weight_min = django_filters.NumberFilter(field_name='weight', lookup_expr='gte')
    weight_max = django_filters.NumberFilter(field_name='weight', lookup_expr='lte')
    min_power_min = django_filters.NumberFilter(field_name='min_power', lookup_expr='gte')
    min_power_max = django_filters.NumberFilter(field_name='min_power', lookup_expr='lte')
    
    class Meta(MachineryFilter.Meta):
        model = Plow
        fields = MachineryFilter.Meta.fields + [
            'width', 'bodies', 'reversible', 'weight', 'min_power'
        ]

class SeederFilter(MachineryFilter):
    width_min = django_filters.NumberFilter(field_name='width', lookup_expr='gte')
    width_max = django_filters.NumberFilter(field_name='width', lookup_expr='lte')
    seed_tank_capacity_min = django_filters.NumberFilter(field_name='seed_tank_capacity', lookup_expr='gte')
    seed_tank_capacity_max = django_filters.NumberFilter(field_name='seed_tank_capacity', lookup_expr='lte')
    fert_tank_capacity_min = django_filters.NumberFilter(field_name='fert_tank_capacity', lookup_expr='gte')
    fert_tank_capacity_max = django_filters.NumberFilter(field_name='fert_tank_capacity', lookup_expr='lte')
    seed_type = django_filters.CharFilter(lookup_expr='iexact')
    seed_type_in = django_filters.CharFilter(method='filter_seed_type_in')
    
    class Meta(MachineryFilter.Meta):
        model = Seeder
        fields = MachineryFilter.Meta.fields + [
            'width', 'seed_tank_capacity', 'fert_tank_capacity','seed_type'
        ]

class HarrowFilter(MachineryFilter):
    width_min = django_filters.NumberFilter(field_name='width', lookup_expr='gte')
    width_max = django_filters.NumberFilter(field_name='width', lookup_expr='lte')
    harrow_type = django_filters.CharFilter(lookup_expr='iexact')
    harrow_type_in = django_filters.CharFilter(method='filter_harrow_type_in')
    
    def filter_harrow_type_in(self, queryset, name, value):
        harrow_types = value.split(',')
        return queryset.filter(harrow_type__in=harrow_types)
    
    class Meta(MachineryFilter.Meta):
        model = Harrow
        fields = MachineryFilter.Meta.fields + [
            'width', 'harrow_type'
        ]

class TrailedSprayerFilter(MachineryFilter):
    width_min = django_filters.NumberFilter(field_name='width', lookup_expr='gte')
    width_max = django_filters.NumberFilter(field_name='width', lookup_expr='lte')
    tank_capacity_min = django_filters.NumberFilter(field_name='tank_capacity', lookup_expr='gte')
    tank_capacity_max = django_filters.NumberFilter(field_name='tank_capacity', lookup_expr='lte')
    
    class Meta(MachineryFilter.Meta):
        model = TrailedSprayer
        fields = MachineryFilter.Meta.fields + [
            'width', 'tank_capacity'
        ]

class MowerFilter(MachineryFilter):
    width_min = django_filters.NumberFilter(field_name='width', lookup_expr='gte')
    width_max = django_filters.NumberFilter(field_name='width', lookup_expr='lte')
    
    class Meta(MachineryFilter.Meta):
        model = Mower
        fields = MachineryFilter.Meta.fields + [
            'width'
        ]

class BalerFilter(MachineryFilter):
    baler_type = django_filters.CharFilter(lookup_expr='iexact')
    baler_type_in = django_filters.CharFilter(method='filter_baler_type_in')
    bale_size = django_filters.CharFilter(lookup_expr='iexact')
    bale_size_in = django_filters.CharFilter(method='filter_bale_size_in')
    productivity_min = django_filters.NumberFilter(field_name='productivity', lookup_expr='gte')
    productivity_max = django_filters.NumberFilter(field_name='productivity', lookup_expr='lte')
    min_power_min = django_filters.NumberFilter(field_name='min_power', lookup_expr='gte')
    min_power_max = django_filters.NumberFilter(field_name='min_power', lookup_expr='lte')
    width_min = django_filters.NumberFilter(field_name='width', lookup_expr='gte')
    width_max = django_filters.NumberFilter(field_name='width', lookup_expr='lte')
    
    def filter_baler_type_in(self, queryset, name, value):
        baler_types = value.split(',')
        return queryset.filter(baler_type__in=baler_types)
    
    def filter_bale_size_in(self, queryset, name, value):
        bale_sizes = value.split(',')
        return queryset.filter(bale_size__in=bale_sizes)
    
    class Meta(MachineryFilter.Meta):
        model = Baler
        fields = MachineryFilter.Meta.fields + [
            'baler_type', 'bale_size', 'productivity', 'min_power', 'width'
        ]