from django.shortcuts import render, get_object_or_404
from .models import Machineryy
from cars.models import Machinery, Tractor, Harvester, SelfPropelledSprayer, Plow, Seeder, Harrow, TrailedSprayer, Mower, Baler

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

# Create your views here.
def cars(request):
    machinery = [m.get_real_instance() for m in Machinery.objects.all().order_by('-created_date')]
    paginator = Paginator(machinery, 4)
    page = request.GET.get('page')
    paged_machinery = paginator.get_page(page)

    type_search = [choice[1] for choice in Machinery.MACHINERY_TYPES]
    city_search = Machineryy.objects.values_list('city', flat=True).distinct()
    year_search = Machinery.objects.values_list('year', flat=True).distinct()
    brand_search = Machinery.objects.values_list('manufacturer', flat=True).distinct()
    
    data = {
        'machinery': paged_machinery,
        'type_search': type_search,
        'city_search': city_search,
        'year_search': year_search,
        'brand_search': brand_search,
    }
    return render(request, 'cars/cars.html', data)

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
