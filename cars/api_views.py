from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.db.models import Min, Max
from django.db.models import Q

from .models import (
    Machinery, Tractor, Harvester, SelfPropelledSprayer,
    Plow, Seeder, Harrow, TrailedSprayer, Mower, Baler
)
from .serializers import (
    MachinerySerializer, TractorSerializer, HarvesterSerializer,
    SelfPropelledSprayerSerializer, PlowSerializer, SeederSerializer,
    HarrowSerializer, TrailedSprayerSerializer, MowerSerializer, BalerSerializer
)
from .filters import (
    MachineryFilter, TractorFilter, HarvesterFilter, SelfPropelledSprayerFilter,
    PlowFilter, SeederFilter, HarrowFilter, TrailedSprayerFilter, MowerFilter, BalerFilter
)

class MachineryPagination(PageNumberPagination):
    page_size = 9
    page_size_query_param = 'page_size'
    max_page_size = 50

class MachineryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Machinery.objects.all().order_by('-created_date')
    serializer_class = MachinerySerializer
    filterset_class = MachineryFilter
    pagination_class = MachineryPagination

class TractorViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tractor.objects.all().order_by('-created_date')
    serializer_class = TractorSerializer
    filterset_class = TractorFilter
    pagination_class = MachineryPagination

class HarvesterViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Harvester.objects.all().order_by('-created_date')
    serializer_class = HarvesterSerializer
    filterset_class = HarvesterFilter
    pagination_class = MachineryPagination

class SelfPropelledSprayerViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SelfPropelledSprayer.objects.all().order_by('-created_date')
    serializer_class = SelfPropelledSprayerSerializer
    filterset_class = SelfPropelledSprayerFilter
    pagination_class = MachineryPagination

class PlowViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Plow.objects.all().order_by('-created_date')
    serializer_class = PlowSerializer
    filterset_class = PlowFilter
    pagination_class = MachineryPagination

class SeederViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Seeder.objects.all().order_by('-created_date')
    serializer_class = SeederSerializer
    filterset_class = SeederFilter
    pagination_class = MachineryPagination

class HarrowViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Harrow.objects.all().order_by('-created_date')
    serializer_class = HarrowSerializer
    filterset_class = HarrowFilter
    pagination_class = MachineryPagination

class TrailedSprayerViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TrailedSprayer.objects.all().order_by('-created_date')
    serializer_class = TrailedSprayerSerializer
    filterset_class = TrailedSprayerFilter
    pagination_class = MachineryPagination

class MowerViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Mower.objects.all().order_by('-created_date')
    serializer_class = MowerSerializer
    filterset_class = MowerFilter
    pagination_class = MachineryPagination

class BalerViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Baler.objects.all().order_by('-created_date')
    serializer_class = BalerSerializer
    filterset_class = BalerFilter
    pagination_class = MachineryPagination

@api_view(['GET'])
def get_filter_options(request):
    """Get all filter options for the machinery catalog."""
    
    # Get all manufacturers
    manufacturers = Machinery.objects.values_list('manufacturer', flat=True).distinct().order_by('manufacturer')
    
    # Get year range
    year_range = Machinery.objects.aggregate(min=Min('year'), max=Max('year'))
    
    # Get price range
    price_range = Machinery.objects.aggregate(min=Min('price'), max=Max('price'))
    
    # Get power range (for machinery with power)
    power_models = Q(tractor__isnull=False) | Q(harvester__isnull=False) | Q(selfpropelledsprayer__isnull=False)
    
    # Получаем минимальные и максимальные значения из каждой модели
    tractor_range = Tractor.objects.aggregate(min_power=Min('power'), max_power=Max('power'))
    harvester_range = Harvester.objects.aggregate(min_power=Min('power'), max_power=Max('power'))
    sprayer_range = SelfPropelledSprayer.objects.aggregate(min_power=Min('power'), max_power=Max('power'))

    # Вычисляем общий min и max в Python
    power_range = {
        'min': min(filter(None, [tractor_range['min_power'], harvester_range['min_power'], sprayer_range['min_power']])),
        'max': max(filter(None, [tractor_range['max_power'], harvester_range['max_power'], sprayer_range['max_power']]))
    }
    
    
    # Получаем диапазон объема двигателя из каждой модели
    tractor_volume = Tractor.objects.aggregate(min_volume=Min('engine_volume'), max_volume=Max('engine_volume'))
    harvester_volume = Harvester.objects.aggregate(min_volume=Min('engine_volume'), max_volume=Max('engine_volume'))
    sprayer_volume = SelfPropelledSprayer.objects.aggregate(min_volume=Min('engine_volume'), max_volume=Max('engine_volume'))

    # Находим общий min и max в Python
    engine_volume_range = {
        'min': min(filter(None, [tractor_volume['min_volume'], harvester_volume['min_volume'], sprayer_volume['min_volume']])),
        'max': max(filter(None, [tractor_volume['max_volume'], harvester_volume['max_volume'], sprayer_volume['max_volume']]))
    }
    
    # Get width range (for machinery with width)
    width_models = Q(plow__isnull=False) | Q(seeder__isnull=False) | Q(harrow__isnull=False) | \
                  Q(trailedsprayer__isnull=False) | Q(mower__isnull=False) | Q(selfpropelledsprayer__isnull=False) | Q(baler__isnull=False)
    # Диапазон ширины (width)
    from django.db.models.functions import Coalesce
    width_range = Machinery.objects.aggregate(
        min=Min(Coalesce(
            'plow__width', 'seeder__width', 'harrow__width',
             'mower__width',  'baler__width'
        )),
        max=Max(Coalesce(
            'plow__width', 'seeder__width', 'harrow__width',
             'mower__width', 'baler__width'
        ))
    )

    sprayer_minwidth_range=Machinery.objects.aggregate(min=Min(Coalesce('selfpropelledsprayer__minwidth','trailedsprayer__minwidth')),
                                                    max=Max(Coalesce('selfpropelledsprayer__minwidth','trailedsprayer__minwidth')))
                              
    sprayer_maxwidth_range=Machinery.objects.aggregate(min=Min(Coalesce('selfpropelledsprayer__maxwidth','trailedsprayer__maxwidth')),
                                                    max=Max(Coalesce('selfpropelledsprayer__maxwidth','trailedsprayer__maxwidth')))
    sprayer_tank_range=Machinery.objects.aggregate(min=Min(Coalesce('selfpropelledsprayer__tank_capacity','trailedsprayer__tank_capacity')),
                                                    max=Max(Coalesce('selfpropelledsprayer__tank_capacity','trailedsprayer__tank_capacity')))
    sprayer_pump_productivity_range = Machinery.objects.aggregate(min=Min(Coalesce('selfpropelledsprayer__pump_productivity','trailedsprayer__pump_productivity')),
                                                    max=Max(Coalesce('selfpropelledsprayer__pump_productivity','trailedsprayer__pump_productivity')))
    seeder_seed_tank_capacity_range = Machinery.objects.aggregate(min=Min('seeder__seed_tank_capacity'), max=Max('seeder__seed_tank_capacity'))                 
    seeder_fert_tank_capacity_range = Machinery.objects.aggregate(min=Min('seeder__fert_tank_capacity'), max=Max('seeder__fert_tank_capacity'))
    seeder_width_range = Machinery.objects.aggregate(min=Min('seeder__width'), max=Max('seeder__width'))
    bale_size_range = Machinery.objects.aggregate(min=Min('baler__bale_size'), max=Max('baler__bale_size'))
    baler_width_range = Machinery.objects.aggregate(min=Min('baler__width'), max=Max('baler__width'))
    baler_productivity_range = Machinery.objects.aggregate(min=Min('baler__productivity'), max=Max('baler__productivity'))
    baler_min_power_range = Machinery.objects.aggregate(min=Min('baler__min_power'), max=Max('baler__min_power'))
    
    harrow_min_depth_range = Machinery.objects.aggregate(min=Min('harrow__min_depth'), max=Max('harrow__min_depth'))
    harrow_max_depth_range = Machinery.objects.aggregate(min=Min('harrow__max_depth'), max=Max('harrow__max_depth'))
    harrow_width_range = Machinery.objects.aggregate(min=Min('harrow__width'), max=Max('harrow__width'))
    harrow_productivity_range = Machinery.objects.aggregate(min=Min('harrow__productivity'), max=Max('harrow__productivity'))


    mower_min_power_range = Machinery.objects.aggregate(min=Min('mower__min_power'), max=Max('mower__min_power'))
    plow_min_power_range = Machinery.objects.aggregate(min=Min('plow__min_power'), max=Max('plow__min_power'))
    mower_productivity_range = Machinery.objects.aggregate(min=Min('mower__productivity'), max=Max('mower__productivity'))
    
    # Prepare tractor-specific options
    tractor_options = {
        'drive_types': [choice[0] for choice in Tractor.DRIVE_TYPE_CHOICES],
        'transmission_types': [choice[0] for choice in Tractor.TRANSMISSION_CHOICES],
        'tow_classes': [choice[0] for choice in Tractor.TOW_CLASS_CHOICES],
    }
    
    # Prepare harvester-specific options
    harvester_options = {
        'threshing_types': [choice[0] for choice in Harvester.THRESHING_TYPE_CHOICES],
    }
    
    # Prepare seeder-specific options
    seeder_options = {
        'seed_types': [choice[0] for choice in Seeder.SEED_TYPE_CHOICES],
    }
    
    # Prepare harrow-specific options
    harrow_options = {
        'harrow_types': [choice[0] for choice in Harrow.HARROW_TYPE_CHOICES],
    }

    mower_options = {
        'mower_types': [choice[0] for choice in Mower.MOWER_TYPE_CHOICES],
    }
    
    # Prepare baler-specific options
    baler_options = {
        'baler_types': [choice[0] for choice in Baler.BALER_TYPE_CHOICES],
    }
    
    # Count of each machinery type
    machinery_counts = {
        'Tractor': Tractor.objects.count(),
        'Harvester': Harvester.objects.count(),
        'SelfPropelledSprayer': SelfPropelledSprayer.objects.count(),
        'Plow': Plow.objects.count(),
        'Seeder': Seeder.objects.count(),
        'Harrow': Harrow.objects.count(),
        'TrailedSprayer': TrailedSprayer.objects.count(),
        'Mower': Mower.objects.count(),
        'Baler': Baler.objects.count(),
    }
    
    return Response({
        'manufacturers': list(manufacturers),
        'year_range': year_range,
        'price_range': price_range,
        'power_range': power_range,
        'engine_volume_range': engine_volume_range,
        'width_range': width_range,
        'sprayer_minwidth_range': sprayer_minwidth_range,
        'sprayer_maxwidth_range': sprayer_maxwidth_range,
        'sprayer_pump_productivity_range': sprayer_pump_productivity_range,
        'sprayer_tank_range': sprayer_tank_range,
        'seeder_seed_tank_capacity_range': seeder_seed_tank_capacity_range,
        'seeder_fert_tank_capacity_range': seeder_fert_tank_capacity_range,
        'seeder_width_range': seeder_width_range,
        'bale_size_range': bale_size_range,
        'baler_width_range': baler_width_range,
        'baler_productivity_range': baler_productivity_range,
        'baler_min_power_range': baler_min_power_range,
        'mower_productivity_range': mower_productivity_range,
        'mower_min_power_range': mower_min_power_range,
        'plow_min_power_range': plow_min_power_range,
        'harrow_min_depth_range': harrow_min_depth_range,
        'harrow_max_depth_range': harrow_max_depth_range,
        'harrow_width_range': harrow_width_range,
        'harrow_productivity_range': harrow_productivity_range,
        'tractor_options': tractor_options,
        'harvester_options': harvester_options,
        'seeder_options': seeder_options,
        'harrow_options': harrow_options,
        'mower_options': mower_options,
        'baler_options': baler_options,
        'machinery_counts': machinery_counts,
    })

@api_view(['GET'])
def combined_machinery_list(request):
    print(list(Machinery.objects.values_list('machinery_type', flat=True).distinct()))
    """
    Get a combined list of all machinery with pagination and filtering.
    This endpoint returns all machinery types in a single list.
    """
    # Start with all machinery
    queryset = Machinery.objects.all().order_by('-created_date')
    
    # Apply machinery type filter if specified
    machinery_types = []
    machinery_type_param = request.query_params.get('machinery_type', '')
    if machinery_type_param:
        machinery_types = [m_type.strip() for m_type in machinery_type_param.split(',')]


    if machinery_types:
        # Создаем фильтр с OR-условиями для каждого типа с нечувствительностью к регистру
        import django.db.models
        q_objects = django.db.models.Q()
        for m_type in machinery_types:
            q_objects |= django.db.models.Q(machinery_type__iexact=m_type)
        queryset = queryset.filter(q_objects)
    
    # Apply common filters
    common_filter = MachineryFilter(request.query_params, queryset=queryset)
    queryset = common_filter.qs
    
    # Get real instances of each machinery item
    real_instances = [item.get_real_instance() for item in queryset]
    
# Apply type-specific filters
    filtered_instances = []
    for item in real_instances:
        include_item = True
        
        # Фильтры для Тракторов
        if isinstance(item, Tractor):
            power_min = request.query_params.get('power_min')
            power_max = request.query_params.get('power_max')
            engine_volume_min = request.query_params.get('engine_volume_min')
            engine_volume_max = request.query_params.get('engine_volume_max')
            tow_class = request.query_params.get('tow_class')
           
            # Фильтрация по тяговому классу
            if tow_class:
                tow_classes = [float(tc.strip()) for tc in tow_class.split(',')]
                if item.tow_class not in tow_classes:
                    include_item = False

            if power_min and item.power < float(power_min):
                include_item = False
            if power_max and item.power > float(power_max):
                include_item = False
            if engine_volume_min and item.engine_volume < float(engine_volume_min):
                include_item = False
            if engine_volume_max and item.engine_volume > float(engine_volume_max):
                include_item = False
           
                
                
                
            drive_type = request.query_params.get('drive_type')
            if drive_type:
                drive_types = [dt.strip() for dt in drive_type.split(',')]
                if item.drive_type not in drive_types:
                    include_item = False
            
            # Добавить фильтрацию по типу трансмиссии с поддержкой множества значений
            transmission_type = request.query_params.get('transmission_type')
            if transmission_type:
                transmission_types = [tt.strip() for tt in transmission_type.split(',')]
                if item.transmission_type not in transmission_types:
                    include_item = False
        
        # Фильтры для Комбайнов
        elif isinstance(item, Harvester):
            power_min = request.query_params.get('harvester_power_min')
            power_max = request.query_params.get('harvester_power_max')
            engine_volume_min = request.query_params.get('harvester_engine_volume_min')
            engine_volume_max = request.query_params.get('harvester_engine_volume_max')
            bunker_volume_min = request.query_params.get('bunker_volume_min')
            bunker_volume_max = request.query_params.get('bunker_volume_max')
            
            if power_min and item.power < float(power_min):
                include_item = False
            if power_max and item.power > float(power_max):
                include_item = False
            if engine_volume_min and item.engine_volume < float(engine_volume_min):
                include_item = False
            if engine_volume_max and item.engine_volume > float(engine_volume_max):
                include_item = False
            if bunker_volume_min and item.bunker_volume < float(bunker_volume_min):
                include_item = False
            if bunker_volume_max and item.bunker_volume > float(bunker_volume_max):
                include_item = False

            threshing_type = request.query_params.get('threshing_type')
            if threshing_type:
                threshing_types = [tt.strip() for tt in threshing_type.split(',')]
                if item.threshing_type not in threshing_types:
                    include_item = False
        
        # Фильтры для Самоходных опрыскивателей
        elif isinstance(item, SelfPropelledSprayer):
            power_min = request.query_params.get('self_sprayer_power_min')
            power_max = request.query_params.get('self_sprayer_power_max')
            engine_volume_min = request.query_params.get('self_sprayer_engine_volume_min')
            engine_volume_max = request.query_params.get('self_sprayer_engine_volume_max')
            minwidth_min = request.query_params.get('self_sprayer_minwidth_min')
            minwidth_max = request.query_params.get('self_sprayer_minwidth_max')
            maxwidth_min = request.query_params.get('self_sprayer_maxwidth_min')
            maxwidth_max = request.query_params.get('self_sprayer_maxwidth_max')
            tank_min = request.query_params.get('self_sprayer_tank_min')
            tank_max = request.query_params.get('self_sprayer_tank_max')
            pump_prodictivity_min = request.query_params.get('self_sprayer_pump_prodictivity_min')
            pump_prodictivity_max = request.query_params.get('self_sprayer_pump_prodictivity_max')


            
            if power_min and item.power < float(power_min):
                include_item = False
            if power_max and item.power > float(power_max):
                include_item = False
            if engine_volume_min and item.engine_volume < float(engine_volume_min):
                include_item = False
            if engine_volume_max and item.engine_volume > float(engine_volume_max):
                include_item = False
            if minwidth_min and item.minwidth < float(minwidth_min):
                include_item = False
            if minwidth_max and item.minwidth > float(minwidth_max):
                include_item = False
            if maxwidth_min and item.maxwidth < float(maxwidth_min):
                include_item = False
            if maxwidth_max and item.maxwidth > float(maxwidth_max):
                include_item = False
            if tank_min and item.tank_capacity < float(tank_min):
                include_item = False
            if tank_max and item.tank_capacity > float(tank_max):
                include_item = False
            if pump_prodictivity_min and item.pump_productivity < float(pump_prodictivity_min):
                include_item = False
            if pump_prodictivity_max and item.pump_productivity > float(pump_prodictivity_max): 
                include_item = False
        
        # Фильтры для Плугов
        elif isinstance(item, Plow):
            width_min = request.query_params.get('width_min')
            width_max = request.query_params.get('width_max')
            bodies_min = request.query_params.get('bodies_min')
            bodies_max = request.query_params.get('bodies_max')
            weight_min = request.query_params.get('weight_min')
            weight_max = request.query_params.get('weight_max')
            min_power_min = request.query_params.get('min_power_min')
            min_power_max = request.query_params.get('min_power_max')
            
            if width_min and item.width < float(width_min):
                include_item = False
            if width_max and item.width > float(width_max):
                include_item = False
            if bodies_min and item.bodies < int(bodies_min):
                include_item = False
            if bodies_max and item.bodies > int(bodies_max):
                include_item = False
            if weight_min and item.weight < int(weight_min):
                include_item = False
            if weight_max and item.weight > int(weight_max):
                include_item = False
            if min_power_min and item.min_power < int(min_power_min):
                include_item = False
            if min_power_max and item.min_power > int(min_power_max):
                include_item = False
        
        # Фильтры для Сеялок
        elif isinstance(item, Seeder):
            width_min = request.query_params.get('seeder_width_min')
            width_max = request.query_params.get('seeder_width_max')
            seed_tank_min = request.query_params.get('seed_tank_min')
            seed_tank_max = request.query_params.get('seed_tank_max')
            fert_tank_min = request.query_params.get('fert_tank_min')
            fert_tank_max = request.query_params.get('fert_tank_max')
            
            if width_min and item.width < float(width_min):
                include_item = False
            if width_max and item.width > float(width_max):
                include_item = False
            if seed_tank_min and item.seed_tank_capacity < int(seed_tank_min):
                include_item = False
            if seed_tank_max and item.seed_tank_capacity > int(seed_tank_max):
                include_item = False
            if fert_tank_min and item.fert_tank_capacity < int(fert_tank_min):
                include_item = False
            if fert_tank_max and item.fert_tank_capacity > int(fert_tank_max):
                include_item = False
            seed_type = request.query_params.get('seed_type')
            if seed_type:
                seed_types = [st.strip() for st in seed_type.split(',')]
                if item.seed_type not in seed_types:
                    include_item = False
        
        # Фильтры для Борон
        elif isinstance(item, Harrow):
            width_min = request.query_params.get('harrow_width_min')
            width_max = request.query_params.get('harrow_width_max')
            min_depth_min = request.query_params.get('harrow_min_depth_min')
            min_depth_max = request.query_params.get('harrow_min_depth_max')
            max_depth_min = request.query_params.get('harrow_max_depth_min')
            max_depth_max = request.query_params.get('harrow_max_depth_max')
            productivity_min = request.query_params.get('harrow_productivity_min')
            productivity_max = request.query_params.get('harrow_productivity_max')

            harrow_type = request.query_params.get('harrow_type')
            if harrow_type:
                harrow_types = [ht.strip() for ht in harrow_type.split(',')]
                if item.harrow_type not in harrow_types:
                    include_item = False
            
            if width_min and item.width < float(width_min):
                include_item = False
            if width_max and item.width > float(width_max):
                include_item = False
            if min_depth_min and item.min_depth < float(min_depth_min):
                include_item = False
            if min_depth_max and item.min_depth > float(min_depth_max):
                include_item = False
            if max_depth_min and item.max_depth < float(max_depth_min):
                include_item = False            
            if max_depth_max and item.max_depth > float(max_depth_max):
                include_item = False
            if productivity_min and item.productivity < float(productivity_min):
                include_item = False
            if productivity_max and item.productivity > float(productivity_max):
                include_item = False

        
        # Фильтры для Прицепных опрыскивателей
        elif isinstance(item, TrailedSprayer):
            minwidth_min = request.query_params.get('trailed_sprayer_minwidth_min')
            minwidth_max = request.query_params.get('trailed_sprayer_minwidth_max')
            maxwidth_min = request.query_params.get('trailed_sprayer_maxwidth_min')
            maxwidth_max = request.query_params.get('trailed_sprayer_maxwidth_max')
            tank_min = request.query_params.get('trailed_sprayer_tank_min')
            tank_max = request.query_params.get('trailed_sprayer_tank_max')
            pump_prodictivity_min = request.query_params.get('trailed_sprayer_pump_prodictivity_min')
            pump_prodictivity_max = request.query_params.get('trailed_sprayer_pump_prodictivity_max')
            
            if minwidth_min and item.minwidth < float(minwidth_min):
                include_item = False
            if minwidth_max and item.minwidth > float(minwidth_max):
                include_item = False
            if maxwidth_min and item.maxwidth < float(maxwidth_min):
                include_item = False
            if maxwidth_max and item.maxwidth > float(maxwidth_max):
                include_item = False
            if tank_min and item.tank_capacity < int(tank_min):
                include_item = False
            if tank_max and item.tank_capacity > int(tank_max):
                include_item = False
            if pump_prodictivity_min and item.pump_prodictivity < int(pump_prodictivity_min):
                include_item = False
            if pump_prodictivity_max and item.pump_prodictivity > int(pump_prodictivity_max):
                include_item = False
        
        # Фильтры для Косилок
        elif isinstance(item, Mower):
            width_min = request.query_params.get('mower_width_min')
            width_max = request.query_params.get('mower_width_max')
            productivity_min = request.query_params.get('mower_productivity_min')
            productivity_max = request.query_params.get('mower_productivity_max')
            min_power_min = request.query_params.get('mower_min_power_min')
            min_power_max = request.query_params.get('mower_min_power_max')
            
            if width_min and item.width < float(width_min):
                include_item = False
            if width_max and item.width > float(width_max):
                include_item = False
            if productivity_min and item.productivity < float(productivity_min):
                include_item = False
            if productivity_max and item.productivity > float(productivity_max):
                include_item = False
            if min_power_min and item.min_power < float(min_power_min):
                include_item = False
            if min_power_max and item.min_power > float(min_power_max):
                include_item = False
            
            mower_type = request.query_params.get('mower_type')
            if mower_type:
                mower_types = [mt.strip() for mt in mower_type.split(',')]
                if item.mower_type not in mower_types:
                    include_item = False
        
        # Фильтры для Пресс-подборщиков
        elif isinstance(item, Baler):
            productivity_min = request.query_params.get('productivity_min')
            productivity_max = request.query_params.get('productivity_max')
            capacity_min = request.query_params.get('capacity_min')
            capacity_max = request.query_params.get('capacity_max')
            width_max = request.query_params.get('baler_width_max')
            width_min = request.query_params.get('baler_width_min')
            
            if width_max and item.width > float(width_max):
                include_item = False
            if width_min and item.width < float(width_min):
                include_item = False
            

            baler_type = request.query_params.get('baler_type')
            if baler_type:
                baler_types = [bt.strip() for bt in baler_type.split(',')]
                if item.baler_type not in baler_types:
                    include_item = False
            
            # Добавить фильтрацию по размеру тюка с поддержкой множества значений
            bale_size = request.query_params.get('bale_size')
            if bale_size:
                bale_sizes = [bs.strip() for bs in bale_size.split(',')]
                if item.bale_size not in bale_sizes:
                    include_item = False
            
            if productivity_min and item.productivity < int(productivity_min):
                include_item = False
            if productivity_max and item.productivity > int(productivity_max):
                include_item = False
            if capacity_min and item.capacity < int(capacity_min):
                include_item = False
            if capacity_max and item.capacity > int(capacity_max):
                include_item = False
        
        if include_item:
            filtered_instances.append(item)
   


    # Применяем сортировку, если она указана
    ordering = request.query_params.get('ordering')
    if ordering:
        # Определяем поле для сортировки (без минуса, если он есть)
        sort_field = ordering[1:] if ordering.startswith('-') else ordering
        # Определяем направление сортировки
        reverse_order = ordering.startswith('-')
        
        # Проверяем, что поле существует во всех объектах
        if hasattr(filtered_instances[0] if filtered_instances else None, sort_field):
            # Сортируем список объектов
            filtered_instances.sort(
                key=lambda x: getattr(x, sort_field) if hasattr(x, sort_field) else 0,
                reverse=reverse_order
            )

    # Apply pagination
    paginator = MachineryPagination()
    page = paginator.paginate_queryset(filtered_instances, request)
   
    # Serialize each item according to its actual type
    serialized_data = []
    for item in page:
        if isinstance(item, Tractor):
            serialized_data.append(TractorSerializer(item).data)
        elif isinstance(item, Harvester):
            serialized_data.append(HarvesterSerializer(item).data)
        elif isinstance(item, SelfPropelledSprayer):
            serialized_data.append(SelfPropelledSprayerSerializer(item).data)
        elif isinstance(item, Plow):
            serialized_data.append(PlowSerializer(item).data)
        elif isinstance(item, Seeder):
            serialized_data.append(SeederSerializer(item).data)
        elif isinstance(item, Harrow):
            serialized_data.append(HarrowSerializer(item).data)
        elif isinstance(item, TrailedSprayer):
            serialized_data.append(TrailedSprayerSerializer(item).data)
        elif isinstance(item, Mower):
            serialized_data.append(MowerSerializer(item).data)
        elif isinstance(item, Baler):
            serialized_data.append(BalerSerializer(item).data)
        else:
            serialized_data.append(MachinerySerializer(item).data)
   
    return paginator.get_paginated_response(serialized_data)