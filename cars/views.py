from django.shortcuts import render, get_object_or_404
from .models import Machineryy
from cars.models import Machinery, Tractor, Harvester, SelfPropelledSprayer, Plow, Seeder, Harrow, TrailedSprayer, Mower, Baler
import json
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import JsonResponse


from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import MachinerySerializer
# Create your views here.
def cars(request):
    machinery = [m.get_real_instance() for m in Machinery.objects.all().order_by('-created_date')]
    paginator = Paginator(machinery, 4)
    page = request.GET.get('page')
    paged_machinery = paginator.get_page(page)

    type_search = [choice[1] for choice in Machinery.MACHINERY_TYPES]
    #city_search = Machineryy.objects.values_list('city', flat=True).distinct()
    year_search = Machinery.objects.values_list('year', flat=True).distinct()
    brand_search = Machinery.objects.values_list('manufacturer', flat=True).distinct()
    
    data = {
        'machinery': paged_machinery,
        'type_search': type_search,
        #'city_search': city_search,
        'year_search': year_search,
        'brand_search': json.dumps(list(brand_search)),  
    }
    return render(request, 'cars/cars.html', data)

def get_manufacturers(request):
    """Возвращает список производителей в формате JSON"""
    brand_search = list(Machinery.objects.values_list('manufacturer', flat=True).distinct())
    return JsonResponse({'manufacturers': brand_search})

def car_detail(request, id):
    this_machinery = get_object_or_404(Machinery, pk=id).get_real_instance()

    data = {
        'this_machinery': this_machinery,
    }
    return render(request, 'cars/car_detail.html', data)


def search(request):
    cars = Machineryy.objects.order_by('-created_date')

    type_search = Machineryy.objects.values_list('model', flat=True).distinct()
    city_search = Machineryy.objects.values_list('city', flat=True).distinct()
    year_search = Machineryy.objects.values_list('year', flat=True).distinct()
    body_style_search = Machineryy.objects.values_list('body_style', flat=True).distinct()
    transmission_search = Machineryy.objects.values_list('transmission', flat=True).distinct()

    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            cars = cars.filter(description__icontains=keyword)

    if 'model' in request.GET:
        model = request.GET['model']
        if model:
            cars = cars.filter(model__iexact=model)

    if 'city' in request.GET:
        city = request.GET['city']
        if city:
            cars = cars.filter(city__iexact=city)

    if 'year' in request.GET:
        year = request.GET['year']
        if year:
            cars = cars.filter(year__iexact=year)

    if 'body_style' in request.GET:
        body_style = request.GET['body_style']
        if body_style:
            cars = cars.filter(body_style__iexact=body_style)

    if 'min_price' in request.GET:
        min_price = request.GET['min_price']
        max_price = request.GET['max_price']
        if max_price:
            cars = cars.filter(price__gte=min_price, price__lte=max_price)

    data = {
        'cars': cars,
        'type_search': type_search,
        'city_search': city_search,
        'year_search': year_search,
        'body_style_search': body_style_search,
        'transmission_search': transmission_search,
    }
    return render(request, 'cars/search.html', data)

from django.shortcuts import render
from .models import Machinery

def machinery_catalog(request):
    """View for the machinery catalog page."""
    # We'll only use this to render the initial template
    # The actual machinery data will be loaded via AJAX
    return render(request, 'machinery_catalog.html')

def machinery_detail(request, machinery_id):
    """View for the machinery detail page."""
    machinery = Machinery.objects.get(pk=machinery_id)
    # Get the real instance with the specific machinery type
    real_instance = machinery.get_real_instance()
    
    context = {
        'machinery': real_instance
    }
    return render(request, 'machinery_detail.html', context)

""" 
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
    page_size = 10
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
    """ """Get all filter options for the machinery catalog.""" """
    
    # Get all manufacturers
    manufacturers = Machinery.objects.values_list('manufacturer', flat=True).distinct()
    
    # Get year range
    year_range = Machinery.objects.aggregate(min=Min('year'), max=Max('year'))
    
    # Get price range
    price_range = Machinery.objects.aggregate(min=Min('price'), max=Max('price'))
    
    # Get power range (for machinery with power)
    power_models = Q(tractor__isnull=False) | Q(harvester__isnull=False) | Q(selfpropelledsprayer__isnull=False)
    power_range = Machinery.objects.filter(power_models).aggregate(
        min=Min('tractor__power', 'harvester__power', 'selfpropelledsprayer__power'),
        max=Max('tractor__power', 'harvester__power', 'selfpropelledsprayer__power')
    )
    
    # Get engine volume range
    engine_volume_range = Machinery.objects.filter(power_models).aggregate(
        min=Min('tractor__engine_volume', 'harvester__engine_volume', 'selfpropelledsprayer__engine_volume'),
        max=Max('tractor__engine_volume', 'harvester__engine_volume', 'selfpropelledsprayer__engine_volume')
    )
    
    # Get width range (for machinery with width)
    width_models = Q(plow__isnull=False) | Q(seeder__isnull=False) | Q(harrow__isnull=False) | \
                  Q(trailedsprayer__isnull=False) | Q(mower__isnull=False) | Q(selfpropelledsprayer__isnull=False)
    width_range = Machinery.objects.filter(width_models).aggregate(
        min=Min('plow__width', 'seeder__width', 'harrow__width', 
                'trailedsprayer__width', 'mower__width', 'selfpropelledsprayer__width'),
        max=Max('plow__width', 'seeder__width', 'harrow__width', 
                'trailedsprayer__width', 'mower__width', 'selfpropelledsprayer__width')
    )
    
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
    
    # Prepare harrow-specific options
    harrow_options = {
        'harrow_types': [choice[0] for choice in Harrow.HARROW_TYPE_CHOICES],
    }
    
    # Prepare baler-specific options
    baler_options = {
        'baler_types': [choice[0] for choice in Baler.BALER_TYPE_CHOICES],
        'bale_sizes': [choice[0] for choice in Baler.BALE_SIZE_CHOICES],
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
        'tractor_options': tractor_options,
        'harvester_options': harvester_options,
        'harrow_options': harrow_options,
        'baler_options': baler_options,
        'machinery_counts': machinery_counts,
    })

@api_view(['GET'])
def combined_machinery_list(request):
    """ """
    Get a combined list of all machinery with pagination and filtering.
    This endpoint returns all machinery types in a single list.
    """"""
    # Start with all machinery
    queryset = Machinery.objects.all().order_by('-created_date')
    
    # Apply machinery type filter if specified
    machinery_types = request.query_params.getlist('machinery_type', [])
    if machinery_types:
        queryset = queryset.filter(machinery_type__in=machinery_types)
    
    # Apply common filters
    common_filter = MachineryFilter(request.query_params, queryset=queryset)
    queryset = common_filter.qs
    
    # Get real instances of each machinery item
    real_instances = [item.get_real_instance() for item in queryset]
    
    # Apply pagination
    paginator = MachineryPagination()
    page = paginator.paginate_queryset(real_instances, request)
    
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


"""

""" 
@api_view(['GET'])
def filter_machinery(request):
    queryset = Machinery.objects.all()
    
    # Фильтрация
    manufacturer = request.GET.getlist('manufacturer')
    condition = request.GET.getlist('condition')
    year_min = request.GET.get('year_min')
    year_max = request.GET.get('year_max')
    machinery_type = request.GET.getlist('machinery_type')

    if manufacturer:
        queryset = queryset.filter(manufacturer__in=manufacturer)
    if condition:
        queryset = queryset.filter(condition__in=condition)
    if year_min and year_max:
        queryset = queryset.filter(year__range=(year_min, year_max))
    if machinery_type:
        queryset = queryset.filter(machinery_type__in=machinery_type)

    serializer = MachinerySerializer(queryset, many=True)
    return Response(serializer.data) """
