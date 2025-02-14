from django.contrib import admin
from .models import Machineryy
from django.utils.html import format_html

# Register your models here.


from .models import Machinery, Tractor, Harvester, SelfPropelledSprayer, Plow, Seeder, Harrow, TrailedSprayer, Mower, Baler

class MachineryAdmin(admin.ModelAdmin):
    def thumbnail(self, obj):
        if obj.car_photo:
            return format_html('<img src="{}" width="40" style="border-radius: 5px;" />'.format(obj.car_photo.url))
        return "-"
    
    thumbnail.short_description = 'Фото'

    list_display = ('id', 'thumbnail', 'year', 'price', 'condition', 'created_date')
    list_display_links = ('id', 'thumbnail')
    search_fields = ('id', 'year', 'price', 'condition')
    list_filter = ('condition', 'year')

# Регистрируем базовую модель
#admin.site.register(Machinery, MachineryAdmin)

# Регистрируем конкретные виды техники
@admin.register(Tractor)
class TractorAdmin(admin.ModelAdmin):
    list_display = ('id', 'year', 'price', 'power', 'drive_type', 'transmission_type')
    list_filter = ('drive_type', 'transmission_type', 'year')
    search_fields = ('id', 'power')

@admin.register(Harvester)
class HarvesterAdmin(admin.ModelAdmin):
    list_display = ('id', 'year', 'price', 'power', 'bunker_volume', 'threshing_type')
    list_filter = ('threshing_type', 'year')
    search_fields = ('id', 'power')

@admin.register(SelfPropelledSprayer)
class SelfPropelledSprayerAdmin(admin.ModelAdmin):
    list_display = ('id', 'year', 'price', 'power', 'width', 'tank_capacity')
    search_fields = ('id', 'power')

@admin.register(Plow)
class PlowAdmin(admin.ModelAdmin):
    list_display = ('id', 'year', 'price', 'width', 'bodies', 'reversible')
    list_filter = ('reversible', 'year')
    search_fields = ('id', 'width')

@admin.register(Seeder)
class SeederAdmin(admin.ModelAdmin):
    list_display = ('id', 'year', 'price', 'width', 'seed_tank_capacity', 'fert_tank_capacity')
    search_fields = ('id', 'working_width')

@admin.register(Harrow)
class HarrowAdmin(admin.ModelAdmin):
    list_display = ('id', 'year', 'price', 'width', 'harrow_type')
    list_filter = ('harrow_type', 'year')
    search_fields = ('id', 'working_width')

@admin.register(TrailedSprayer)
class TrailedSprayerAdmin(admin.ModelAdmin):
    list_display = ('id', 'year', 'price', 'width', 'tank_capacity')
    search_fields = ('id', 'working_width')

@admin.register(Mower)
class MowerAdmin(admin.ModelAdmin):
    list_display = ('id', 'year', 'price', 'width')
    search_fields = ('id', 'working_width')

@admin.register(Baler)
class BalerAdmin(admin.ModelAdmin):
    list_display = ('id', 'year', 'price', 'baler_type', 'bale_size', 'capacity')
    list_filter = ('baler_type', 'bale_size', 'year')
    search_fields = ('id', 'bale_size')

