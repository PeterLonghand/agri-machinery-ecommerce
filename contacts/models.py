from django.db import models
from datetime import datetime
from cars.models import *

class Contact(models.Model):
    STATUS_CHOICES = (
        ('processing', 'В обработке'),
        ('approved', 'Одобрена'),
        ('rejected', 'Отклонена'),
    )
    
    first_name = models.CharField(max_length=100, verbose_name='Имя')
    last_name = models.CharField(max_length=100, verbose_name='Фамилия')
    car_id = models.IntegerField(verbose_name='ID техники')
    customer_need = models.CharField(max_length=100, verbose_name='Тип заявки')
    car_title = models.CharField(max_length=100, verbose_name='Название техники')
    email = models.EmailField(max_length=100, verbose_name='Email')
    phone = models.CharField(max_length=100, blank=True, verbose_name='Телефон')
    message = models.TextField(blank=True, verbose_name='Сообщение')
    user_id = models.IntegerField(blank=True, verbose_name='ID пользователя')
    create_date = models.DateTimeField(blank=True, default=datetime.now, verbose_name='Дата создания')
    
    # Новое поле статуса
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='processing',
        verbose_name='Статус'
    )
    
    # Поля для лизинга
    leasing_advance = models.IntegerField(null=True, blank=True, verbose_name='Первоначальный взнос, %')
    leasing_term = models.IntegerField(null=True, blank=True, verbose_name='Срок лизинга, мес.')
    leasing_payment_type = models.CharField(max_length=20, null=True, blank=True, verbose_name='Тип платежей')
    leasing_monthly_payment = models.CharField(max_length=50, null=True, blank=True, verbose_name='Ежемесячный платеж')
    leasing_full_payment = models.IntegerField(null=True, blank=True, verbose_name='Полная сумма')
    staff_response = models.TextField(blank=True, null=True, verbose_name='Ответ администратора')
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.car_title}"
    def get_machine_price (self):
        print(Machinery.objects.get(id=self.car_id).price)
        return Machinery.objects.get(id=self.car_id).price
    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'