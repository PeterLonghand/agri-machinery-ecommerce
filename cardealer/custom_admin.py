from django.contrib import admin

class CustomAdminSite(admin.AdminSite):
    def get_app_list(self, request):
        app_list = super().get_app_list(request)
        return [app for app in app_list if app['app_label'] != 'account']  # Убираем приложение "account"

admin.site = CustomAdminSite()  # Подменяем стандартную админку
