from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('pages.urls')),
    #path('', include('cars.urls')),
    path('cars/', include('cars.urls')),
    path('accounts/', include('accounts.urls')),
    # path('socialaccounts/', include('allauth.urls')),
    path('contacts/', include('contacts.urls')),
    path('catalog/', include('cars.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
