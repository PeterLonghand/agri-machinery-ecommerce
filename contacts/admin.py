# admin.py
from django.contrib import admin
from .models import Contact
from django.utils.safestring import mark_safe

class ContactAdmin(admin.ModelAdmin):
    class Meta:
        verbose_name = "Заявка"
        verbose_name_plural = "Заявки"

    list_display = ('id', 'first_name', 'last_name', 'car_title', 'customer_need', 'create_date', 'status', 'get_leasing_info')
    list_display_links = ('id',)  # Только ID будет ссылкой
    search_fields = ('first_name', 'last_name', 'email', 'car_title')
    list_filter = ('customer_need', 'status', 'create_date')
    list_editable = ('status',)  # Только статус редактируется в списке
    readonly_fields = ('first_name', 'last_name', 'car_id', 'car_title', 'email', 
                       'phone', 'message', 'user_id', 'create_date', 'customer_need',
                       'leasing_advance', 'leasing_term', 'get_payment_type_display', 
                       'leasing_monthly_payment', 'leasing_full_payment')
    
    def get_payment_type_display(self, obj):
        if obj.leasing_payment_type == 'equal':
            return "Равномерный"
        elif obj.leasing_payment_type == 'decreasing':
            return "Убывающий"
        return obj.leasing_payment_type
    
    get_payment_type_display.short_description = 'Тип платежа'
    
    def get_leasing_info(self, obj):
        if obj.customer_need != 'Лизинг':
            return "—"
        
        result = f"Аванс: {obj.leasing_advance}%, "
        result += f"Срок: {obj.leasing_term} мес., "
        result += f"Тип: {'Равномерный' if obj.leasing_payment_type == 'equal' else 'Убывающий'}, "
        result += f"Полная сумма: {obj.leasing_full_payment} руб."
        if obj.leasing_monthly_payment and '-' in str(obj.leasing_monthly_payment):
            min_payment, max_payment = obj.leasing_monthly_payment.split('-')
            result += f"Платеж: от {min_payment} до {max_payment} руб."
        else:
            payment = obj.leasing_monthly_payment or '—'
            result += f"Платеж: {payment} руб."
        
        return result
    
    get_leasing_info.short_description = 'Параметры лизинга'
    
    def get_fieldsets(self, request, obj=None):
        # Базовые поля для всех типов заявок
        fieldsets = [
            ('Контактная информация', {
                'fields': ('first_name', 'last_name', 'email', 'phone', 'user_id'),
                'description': '<div style="color: #999">Эта информация доступна только для чтения</div>'
            }),
            ('Информация о технике', {
                'fields': ('car_id', 'car_title'),
                'description': '<div style="color: #999">Эта информация доступна только для чтения</div>'
            }),
            ('Детали заявки', {
                'fields': ('customer_need', 'message', 'create_date'),
                'description': '<div style="color: #999">Эта информация доступна только для чтения</div>'
            }),
            ('Обработка заявки', {
                'fields': ('status', 'staff_response'),
                'description': '<div style="color: #007bff">Эти поля доступны для редактирования</div>'
            }),
        ]
        
        # Если это заявка на лизинг, добавляем соответствующие поля
        if obj and obj.customer_need == 'Лизинг':
            fieldsets.append(
                ('Параметры лизинга', {
                    'fields': ('leasing_advance', 'leasing_term', 'get_payment_type_display', 'leasing_monthly_payment', 'leasing_full_payment'),
                    'description': '<div style="color: #999">Эта информация доступна только для чтения</div>',
                    'classes': ('collapse',)  # Можно свернуть этот раздел
                }),
            )
        
        return fieldsets
    
    def has_delete_permission(self, request, obj=None):
        # Запрещаем удаление заявок
        return True
    
    def get_status_html(self, obj):
        status_colors = {
            'processing': '#3498db',
            'approved': '#2ecc71',
            'rejected': '#e74c3c',
        }
        color = status_colors.get(obj.status, 'black')
        status_text = dict(obj.STATUS_CHOICES).get(obj.status, obj.status)
        return mark_safe(f'<span style="color: {color}; font-weight: bold;">{status_text}</span>')
    
    get_status_html.short_description = 'Статус'
    get_status_html.admin_order_field = 'status'

admin.site.register(Contact, ContactAdmin)