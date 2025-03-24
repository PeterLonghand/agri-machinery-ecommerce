from django.contrib import admin
from django.utils.html import format_html

# Register your models here.

from .models import Machinery, Tractor, Harvester, SelfPropelledSprayer, Plow, Seeder, Harrow, TrailedSprayer, Mower, Baler




class MachineryAdmin(admin.ModelAdmin):
    def thumbnail(self, obj):
        if obj.photo:
            return format_html('<img src="{}" width="40" style="border-radius: 5px;" />'.format(obj.photo.url))
        return "-"
    

    thumbnail.short_description = "Фото"

    list_display = ('id', 'thumbnail', 'machinery_type', 'year', 'price', 'condition')
    list_display_links = ('id', 'thumbnail')
    search_fields = ('id', 'machinery_type', 'year')
    list_filter = ('machinery_type', 'condition', 'year')

    #list_display = ('id', 'thumbnail', 'year', 'price', 'condition', 'created_date')
    #list_display_links = ('id', 'thumbnail')
    #search_fields = ('id', 'year', 'price', 'condition')
    #list_filter = ('condition', 'year')

# Регистрируем базовую модель
#admin.site.register(Machinery, MachineryAdmin)

# Регистрируем конкретные виды техники
@admin.register(Tractor)
class TractorAdmin(admin.ModelAdmin):
    def thumbnail(self, obj):
        if obj.photo:
            return format_html('<img src="{}" width="40" style="border-radius: 5px;" />'.format(obj.photo.url))
        return "-"
    
    thumbnail.short_description = "Фото"
    list_display = ('id', 'thumbnail','manufacturer', 'model_name','year',  'drive_type', 'transmission_type', 'power','price')
    list_filter = ('drive_type', 'transmission_type', 'year')
    search_fields = ('id', 'power')

@admin.register(Harvester)
class HarvesterAdmin(admin.ModelAdmin):
    def thumbnail(self, obj):
        if obj.photo:
            return format_html('<img src="{}" width="40" style="border-radius: 5px;" />'.format(obj.photo.url))
        return "-"
    
    thumbnail.short_description = "Фото"
    list_display = ('id', 'thumbnail','manufacturer', 'model_name', 'year', 'price', 'power', 'bunker_volume', 'threshing_type')
    list_filter = ('threshing_type', 'year')
    search_fields = ('id', 'power')

@admin.register(SelfPropelledSprayer)
class SelfPropelledSprayerAdmin(admin.ModelAdmin):
    def thumbnail(self, obj):
        if obj.photo:
            return format_html('<img src="{}" width="40" style="border-radius: 5px;" />'.format(obj.photo.url))
        return "-"
    
    thumbnail.short_description = "Фото"
    
    list_display = ('id','thumbnail','manufacturer', 'model_name', 'year', 'price', 'power', 'minwidth', 'maxwidth', 'tank_capacity')
    search_fields = ('id', 'power', 'minwidth', 'maxwidth')

@admin.register(Plow)
class PlowAdmin(admin.ModelAdmin):
    def thumbnail(self, obj):
        if obj.photo:
            return format_html('<img src="{}" width="40" style="border-radius: 5px;" />'.format(obj.photo.url))
        return "-"
    

    thumbnail.short_description = "Фото"
    list_display = ('id', 'thumbnail', 'manufacturer', 'model_name','year', 'price', 'width', 'bodies', 'reversible')
    list_filter = ('reversible', 'year')
    search_fields = ('id', 'width')

@admin.register(Seeder)
class SeederAdmin(admin.ModelAdmin):
    def thumbnail(self, obj):
        if obj.photo:
            return format_html('<img src="{}" width="40" style="border-radius: 5px;" />'.format(obj.photo.url))
        return "-"
    
    thumbnail.short_description = "Фото"
    list_display = ('id', 'thumbnail','manufacturer', 'model_name','year', 'price', 'width', 'seed_tank_capacity', 'fert_tank_capacity')
    search_fields = ('id', 'working_width')

@admin.register(Harrow)
class HarrowAdmin(admin.ModelAdmin):
    def thumbnail(self, obj):
        if obj.photo:
            return format_html('<img src="{}" width="40" style="border-radius: 5px;" />'.format(obj.photo.url))
        return "-"
    
    thumbnail.short_description = "Фото"
    list_display = ('id','thumbnail','manufacturer', 'model_name', 'year', 'price', 'width', 'harrow_type')
    list_filter = ('harrow_type', 'year')
    search_fields = ('id', 'working_width')

@admin.register(TrailedSprayer)
class TrailedSprayerAdmin(admin.ModelAdmin):
    def thumbnail(self, obj):
        if obj.photo:
            return format_html('<img src="{}" width="40" style="border-radius: 5px;" />'.format(obj.photo.url))
        return "-"
    
    thumbnail.short_description = "Фото"
    list_display = ('id', 'thumbnail','manufacturer', 'model_name', 'year', 'price', 'minwidth', 'maxwidth', 'tank_capacity')
    search_fields = ('id', 'minwidth', 'maxwidth')

@admin.register(Mower)
class MowerAdmin(admin.ModelAdmin):
    def thumbnail(self, obj):
        if obj.photo:
            return format_html('<img src="{}" width="40" style="border-radius: 5px;" />'.format(obj.photo.url))
        return "-"
    
    thumbnail.short_description = "Фото"
    list_display = ('id', 'thumbnail','manufacturer', 'model_name', 'year', 'price', 'width')
    search_fields = ('id', 'working_width')

@admin.register(Baler)
class BalerAdmin(admin.ModelAdmin):
    def thumbnail(self, obj):
        if obj.photo:
            return format_html('<img src="{}" width="40" style="border-radius: 5px;" />'.format(obj.photo.url))
        return "-"
    
    thumbnail.short_description = "Фото"
    list_display = ('id', 'thumbnail','manufacturer', 'model_name','year', 'price', 'baler_type','bale_size','width')
    list_filter = ('baler_type',  'year')
    search_fields = ('id', 'bale_size' 'manufacturer')

