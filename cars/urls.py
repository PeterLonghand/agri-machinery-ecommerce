from . import views
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import api_views

router = DefaultRouter()
router.register(r'machinery', api_views.MachineryViewSet)
router.register(r'tractors', api_views.TractorViewSet)
router.register(r'harvesters', api_views.HarvesterViewSet)
router.register(r'selfpropelledsprayers', api_views.SelfPropelledSprayerViewSet)
router.register(r'plows', api_views.PlowViewSet)
router.register(r'seeders', api_views.SeederViewSet)
router.register(r'harrows', api_views.HarrowViewSet)
router.register(r'trailedsprayers', api_views.TrailedSprayerViewSet)
router.register(r'mowers', api_views.MowerViewSet)
router.register(r'balers', api_views.BalerViewSet)


urlpatterns = [
    path('', views.cars, name='cars'),
    path('<int:id>', views.car_detail, name='car_detail'),
    path('search', views.search, name='search'),

    path('api/', include(router.urls)),
    path('api/filter-options/', api_views.get_filter_options, name='filter-options'),
    path('api/machinery-combined/', api_views.combined_machinery_list, name='machinery-combined'),
]