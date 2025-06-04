from django.db import models
from datetime import datetime
from ckeditor.fields import RichTextField
from multiselectfield import MultiSelectField

class Machinery(models.Model):
    MACHINERY_TYPES = [
        ('Tractor', 'Трактор'),
        ('Harvester', 'Комбайн'),
        ('SelfPropelledSprayer', 'Опрыскиватель самоходный'),
        ('Plow', 'Плуг'),
        ('Seeder', 'Сеялка'),
        ('Harrow', 'Борона'),
        ('TrailedSprayer', 'Опрыскиватель прицепной'),
        ('Mower', 'Косилка прицепная'),
        ('Baler', 'Пресс-подборщик'),
    ]
    manufacturer = models.CharField(max_length=30, verbose_name="Производитель")
    model_name = models.CharField(max_length=30, verbose_name="Название модели")

    machinery_type = models.CharField(max_length=50, choices=MACHINERY_TYPES, editable=False)
    YEAR_CHOICES = [(r, r) for r in range(1990, datetime.now().year + 1)][::-1]
    CONDITION_CHOICES = [('new', 'Новый'), ('used', 'Б/у')]

    year = models.IntegerField(choices=YEAR_CHOICES, verbose_name="Год выпуска")
    price = models.IntegerField(verbose_name="Цена")
    condition = models.CharField(max_length=10, choices=CONDITION_CHOICES, verbose_name="Состояние")
    description = RichTextField(verbose_name="Описание")
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/', verbose_name="Основное фото")
    photo_1 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True, verbose_name="Дополнительное фото 1")
    photo_2 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True, verbose_name="Дополнительное фото 2")
    photo_3 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True, verbose_name="Дополнительное фото 3")
    photo_4 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True, verbose_name="Дополнительное фото 4")
    created_date = models.DateTimeField(default=datetime.now, blank=True, verbose_name="Дата добавления")

    def get_real_instance(self):
        """Возвращает объект с реальным типом (SelfPropelledSprayer, Harvester и т.д.)."""
        for subclass in self.__class__.__subclasses__():
            if subclass.objects.filter(pk=self.pk).exists():
                return subclass.objects.get(pk=self.pk)
        return self  # Если дочерней модели нет, вернуть сам объект


    class Meta:
        verbose_name = "Техника"
        verbose_name_plural = "Техника"

    def save(self, *args, **kwargs):
        if not self.machinery_type:
            self.machinery_type = self.__class__.__name__
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.manufacturer} {self.model_name} ({self.year})"

class Tractor(Machinery):
    DRIVE_TYPE_CHOICES = [('wheeled_awd', 'Колёсный, полный привод'), ('wheeled_rwd', 'Колёсный, задний привод'), ('tracked', 'Гусеничный')]
    TRANSMISSION_CHOICES = [('manual', 'Механическая'), ('auto', 'Автоматическая')]
    TOW_CLASS_CHOICES = [(i, f'Класс {i}') for i in [0.6, 0.9, 1.4, 2, 3, 4, 5, 6]]
    
    drive_type = models.CharField(choices=DRIVE_TYPE_CHOICES, verbose_name="Тип")
    power = models.IntegerField(verbose_name="Мощность (л.с.)")
    engine_volume = models.FloatField(verbose_name="Объём двигателя (л)")
    transmission_type = models.CharField(choices=TRANSMISSION_CHOICES, verbose_name="Тип КПП")
    tow_class = models.FloatField(choices=TOW_CLASS_CHOICES, verbose_name="Тяговый класс")
    class Meta:
        verbose_name = "Трактор"
        verbose_name_plural = "Тракторы"

class Harvester(Machinery):
    THRESHING_TYPE_CHOICES = [('drum', 'Барабан'), ('rotor', 'Ротор'), ('hybrid', 'Гибрид')]
    
    power = models.IntegerField(verbose_name="Мощность (л.с.)")
    engine_volume = models.FloatField(verbose_name= "Объём двигателя (л)")
    bunker_volume = models.IntegerField(verbose_name="Объём бункера (л)")
    threshing_type = models.CharField(choices=THRESHING_TYPE_CHOICES, verbose_name="Тип молотильного аппарата")
    class Meta:
        verbose_name = "Комбайн зерновой"
        verbose_name_plural = "Комбайны зерновые"

class SelfPropelledSprayer(Machinery):
    power = models.IntegerField(verbose_name="Мощность (л.с.)")
    engine_volume = models.FloatField(verbose_name= "Объём двигателя (л)")
    minwidth = models.IntegerField(verbose_name="Ширина обработки от, м")
    maxwidth = models.IntegerField(verbose_name="Ширина обработки до, м")
    tank_capacity = models.IntegerField(verbose_name="Объём бака удобрений (л)")
    pump_productivity = models.IntegerField(verbose_name="Макс. производительность насоса (л/мин)")
    class Meta:
        verbose_name = "Опрыскиватель самоходный"
        verbose_name_plural = "Опрыскиватели самоходные"

class Plow(Machinery):
    width = models.FloatField(verbose_name="Ширина (м)")
    bodies = models.IntegerField(verbose_name="Число корпусов")
    reversible = models.BooleanField(verbose_name="Оборотный")
    #depth = models.IntegerField(verbose_name="Глубина обработки (см)")
    weight = models.IntegerField(verbose_name="Вес (кг)")
    min_power = models.IntegerField(verbose_name="Минимальная мощность трактора (л.с.)")
    class Meta:
        verbose_name = "Плуг"
        verbose_name_plural = "Плуги"

class Seeder(Machinery):
    SEED_TYPE_CHOICES = [('grain', 'Зерновая'), ('rowcrop', 'Пропашная'),('universal', 'Универсальная')]
    width = models.FloatField(verbose_name="Ширина захвата (м)")
    seed_tank_capacity = models.IntegerField(verbose_name="Объём бункера для семян (л)")
    fert_tank_capacity = models.IntegerField(verbose_name="Объём бункера для удобрений (л)")
    seed_type=models.CharField(choices=SEED_TYPE_CHOICES, verbose_name="Тип")
    class Meta:
        verbose_name = "Сеялка"
        verbose_name_plural = "Сеялки"

class Harrow(Machinery):
    HARROW_TYPE_CHOICES = [('disc', 'Дисковая'), ('tooth', 'Зубовая'), ('rotary', 'Ротационная')]
    
    width = models.FloatField(verbose_name="Ширина захвата (м)")
    harrow_type = models.CharField(choices=HARROW_TYPE_CHOICES, verbose_name="Тип бороны")
    min_depth = models.IntegerField(verbose_name="Минимальная глубина обработки (см)")
    max_depth = models.IntegerField(verbose_name="Максимальная глубина обработки (см)")
    productivity = models.IntegerField(verbose_name="Макс. производительность (га/час)")
    class Meta:
        verbose_name = "Борона"
        verbose_name_plural = "Бороны"
class TrailedSprayer(Machinery):
    #width = models.FloatField(verbose_name="Ширина обработки (м)")
    tank_capacity = models.IntegerField(verbose_name="Ёмкость бака для удобрений (л)")
    minwidth = models.IntegerField(verbose_name="Ширина обработки от, м")
    maxwidth = models.IntegerField(verbose_name="Ширина обработки до, м")
    pump_productivity = models.IntegerField(verbose_name="Макс. производительность насоса (л/мин)")
    class Meta:
        verbose_name = "Опрыскиватель прицепной"
        verbose_name_plural = "Опрыскиватели прицепные"

class Mower(Machinery):
    MOWER_TYPE_CHOICES = [('rotary', 'Роторная'), ('disc', 'Дисковая')]    
    mower_type = models.CharField(choices=MOWER_TYPE_CHOICES, verbose_name="Тип косилки")
    width = models.FloatField(verbose_name="Ширина захвата (м)")
    rotation_speed = models.IntegerField(verbose_name="Скорость вращения (об/мин)")
    productivity = models.FloatField(verbose_name="Макс. производительность (га/час))")
    min_power = models.IntegerField(verbose_name="Мин. мощность трактора (л.с.)")
    class Meta:
        verbose_name = "Косилка прицепная"
        verbose_name_plural = "Косилки прицепные"

class Baler(Machinery):
    BALER_TYPE_CHOICES = [('round', 'Рулонный'), ('rectangular', 'Тюковой')]
    #BALE_SIZE_CHOICES = [('110', '110см'), ('120', '120см'), ('140', '140см'), ('180', '180см)')]
    width = models.FloatField(verbose_name="Ширина захвата (м)")
    baler_type = models.CharField(choices=BALER_TYPE_CHOICES, verbose_name="Тип")
    bale_size = models.IntegerField( verbose_name="Размер тюка (см)")
    productivity = models.IntegerField(verbose_name="Макс. производительность (тюков/час)")
    min_power = models.IntegerField(verbose_name="Мин. мощность трактора (л.с.)")
    class Meta:
        verbose_name = "Пресс-подборщик"
        verbose_name_plural = "Пресс-подборщики"






class Machineryy(models.Model):

    state_choice = (
        ('AL', 'Alabama'),
        ('AK', 'Alaska'),
        ('AZ', 'Arizona'),
        ('AR', 'Arkansas'),
        ('CA', 'California'),
        ('CO', 'Colorado'),
        ('CT', 'Connecticut'),
        ('DE', 'Delaware'),
        ('DC', 'District Of Columbia'),
        ('FL', 'Florida'),
        ('GA', 'Georgia'),
        ('HI', 'Hawaii'),
        ('ID', 'Idaho'),
        ('IL', 'Illinois'),
        ('IN', 'Indiana'),
        ('IA', 'Iowa'),
        ('KS', 'Kansas'),
        ('KY', 'Kentucky'),
        ('LA', 'Louisiana'),
        ('ME', 'Maine'),
        ('MD', 'Maryland'),
        ('MA', 'Massachusetts'),
        ('MI', 'Michigan'),
        ('MN', 'Minnesota'),
        ('MS', 'Mississippi'),
        ('MO', 'Missouri'),
        ('MT', 'Montana'),
        ('NE', 'Nebraska'),
        ('NV', 'Nevada'),
        ('NH', 'New Hampshire'),
        ('NJ', 'New Jersey'),
        ('NM', 'New Mexico'),
        ('NY', 'New York'),
        ('NC', 'North Carolina'),
        ('ND', 'North Dakota'),
        ('OH', 'Ohio'),
        ('OK', 'Oklahoma'),
        ('OR', 'Oregon'),
        ('PA', 'Pennsylvania'),
        ('RI', 'Rhode Island'),
        ('SC', 'South Carolina'),
        ('SD', 'South Dakota'),
        ('TN', 'Tennessee'),
        ('TX', 'Texas'),
        ('UT', 'Utah'),
        ('VT', 'Vermont'),
        ('VA', 'Virginia'),
        ('WA', 'Washington'),
        ('WV', 'West Virginia'),
        ('WI', 'Wisconsin'),
        ('WY', 'Wyoming'),
    )

    year_choice = []
    for r in range(2000, (datetime.now().year+1)):
        year_choice.append((r,r))

    features_choices = (
        ('Cruise Control', 'Cruise Control'),
        ('Audio Interface', 'Audio Interface'),
        ('Airbags', 'Airbags'),
        ('Air Conditioning', 'Air Conditioning'),
        ('Seat Heating', 'Seat Heating'),
        ('Alarm System', 'Alarm System'),
        ('ParkAssist', 'ParkAssist'),
        ('Power Steering', 'Power Steering'),
        ('Reversing Camera', 'Reversing Camera'),
        ('Direct Fuel Injection', 'Direct Fuel Injection'),
        ('Auto Start/Stop', 'Auto Start/Stop'),
        ('Wind Deflector', 'Wind Deflector'),
        ('Bluetooth Handset', 'Bluetooth Handset'),
    )

    door_choices = (
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
        ('6', '6'),
    )

    car_title = models.CharField(max_length=255)
    state = models.CharField(choices=state_choice, max_length=100)
    city = models.CharField(max_length=100)
    color = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.IntegerField(('year'), choices=year_choice)
    condition = models.CharField(max_length=100)
    price = models.IntegerField()
    description = RichTextField()
    car_photo = models.ImageField(upload_to='photos/%Y/%m/%d/')
    car_photo_1 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    car_photo_2 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    car_photo_3 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    car_photo_4 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    features = MultiSelectField(choices=features_choices)
    body_style = models.CharField(max_length=100)
    engine = models.CharField(max_length=100)
    transmission = models.CharField(max_length=100)
    interior = models.CharField(max_length=100)
    miles = models.IntegerField()
    doors = models.CharField(choices=door_choices, max_length=10)
    passengers = models.IntegerField()
    vin_no = models.CharField(max_length=100)
    milage = models.IntegerField()
    fuel_type = models.CharField(max_length=50)
    no_of_owners = models.CharField(max_length=100)
    is_featured = models.BooleanField(default=False)
    created_date = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return self.car_title
