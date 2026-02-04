from django.db import models
from django.core.validators import RegexValidator
from django.core.validators import FileExtensionValidator
import os

def order_scan_upload_path(instance, filename):
    """Путь для сохранения сканов приказов"""
    return f'orders/car_{instance.car.id}/{filename}'

class Car(models.Model):
    """Модель автомобиля"""
    CAR_MODELS = [
        ('Volvo', 'Volvo'),
        ('Scania', 'Scania'),
        ('MAN', 'MAN'),
        ('Mercedes', 'Mercedes'),
        ('DAF', 'DAF'),
        ('Renault', 'Renault'),
        ('Other', 'Другое'),
    ]
    
    state_number = models.CharField(
        'Державний номер',
        max_length=50,
        unique=True,
        help_text="Уникальный державний номер автомобиля"
    )

    board_number = models.CharField(
        'Бортовой номер',
        max_length=50,
        blank=True,
        null=True,
        help_text="Бортовой номер автомобиля (необязательно)"
    )
    
    model = models.CharField(
        'Модель',
        max_length=50,
        choices=CAR_MODELS,
        default='Other'
    )
    

    location = models.ForeignKey(
        'Location',
        verbose_name='Локация',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='cars'
    )
    
    comment = models.TextField(
        'Комментарий',
        blank=True,
        null=True
    )
    
    is_active = models.BooleanField(
        'Активен',
        default=True
    )
    
    created_at = models.DateTimeField(
        'Дата создания',
        auto_now_add=True
    )
    
    updated_at = models.DateTimeField(
        'Дата обновления',
        auto_now=True
    )
    
    class Meta:
        verbose_name = 'Автомобиль'
        verbose_name_plural = 'Автомобили'
        ordering = ['state_number']

    def __str__(self):
        return f"{self.state_number} - {self.get_model_display()}"

class Location(models.Model):
    """Модель для управляемого списка локаций"""
    name = models.CharField('Локация', max_length=200, unique=True)

    # legacy list of choices used for initial seed
    LOCATION_CHOICES = [
        ('Андрушівка','Андрушівка'),
        ('Баранівка','Баранівка'),
        ('Бараші','Бараші'),
        ('Бердичів місто','Бердичів місто'),
        ('Бердичівський р-н','Бердичівський р-н'),
        ('Білокоровичі','Білокоровичі'),
        ('Бондарі','Бондарі'),
        ('Брусилів','Брусилів'),
        ('Городниця','Городниця'),
        ('Ємільчино','Ємільчино'),
        ('Житомир ППБ1','Житомир ППБ1'),
        ('Житомир Центр','Житомир Центр'),
        ('Житомир Центр ПС1','Житомир Центр ПС1'),
        ('Житомир Центр ПС2','Житомир Центр ПС2'),
        ('Звягель','Звягель'),
        ('Іванопіль','Іванопіль'),
        ('Іршанск','Іршанск'),
        ('Корнин','Корнин'),
        ('Коростень місто','Коростень місто'),
        ('Коростень р-н','Коростень р-н'),
        ('Коростишів','Коростишів'),
        ('Лугини','Лугини'),
        ('Любар','Любар'),
        ('Малин','Малин'),
        ('Миропіль','Миропіль'),
        ('Н.Борова','Н.Борова'),
        ('Народичі','Народичі'),
        ('Овруч','Овруч'),
        ('Олевск','Олевск'),
        ('Поліське','Поліське'),
        ('Попільня','Попільня'),
        ('Потіївка','Потіївка'),
        ('Пулини','Пулини'),
        ('Радовель','Радовель'),
        ('Радомишль','Радомишль'),
        ('Романів','Романів'),
        ('Ружин','Ружин'),
        ('сим в АССу','сим в АССу'),
        ('Словечне','Словечне'),
        ('Тойота','Тойота'),
        ('установ на Тойота','установ на Тойота'),
        ('Хорошів','Хорошів'),
        ('Черняхів','Черняхів'),
        ('Чоповичі','Чоповичі'),
        ('Чуднів','Чуднів'),
        ('Ярунь','Ярунь'),
        ('Other','Other'),
    ]

    class Meta:
        verbose_name = 'Локация'
        verbose_name_plural = 'Локации'
        ordering = ['name']

    def __str__(self):
        return self.name

class Tracker(models.Model):
    """Модель GPS-трекера"""
    PROTOCOLS = [
        ('wialon', 'Wialon'),
        ('galileosky', 'GalileoSky'),
        ('teltonika', 'Teltonika'),
        ('other', 'Другое'),
    ]
    
    imei = models.CharField(
        'IMEI',
        max_length=20,
        unique=True,
        validators=[
            RegexValidator(
                regex='^[0-9]{15,20}$',
                message='IMEI должен содержать 15-20 цифр'
            )
        ]
    )
    
    serial_number = models.CharField(
        'S/N трекера',
        max_length=100,
        unique=True
    )
    
    inventory_number_tracker = models.CharField(
        'Инвентарный номер трекера',
        max_length=100,
        unique=True
    )
    
    inventory_number_antenna = models.CharField(
        'Инвентарный номер антенны',
        max_length=100,
        blank=True,
        null=True
    )
    
    model = models.CharField(
        'Модель трекера',
        max_length=100
    )
    
    protocol = models.CharField(
        'Протокол',
        max_length=50,
        choices=PROTOCOLS,
        default='wialon'
    )
    
    holder_number = models.CharField(
        'Держатель N',
        max_length=50,
        blank=True,
        null=True
    )
    
    sim_old = models.CharField(
        'Старый SIM',
        max_length=50,
        blank=True,
        null=True
    )
    
    n_card = models.CharField(
        'N Card',
        max_length=50,
        blank=True,
        null=True
    )
    
    sim_new = models.CharField(
        'Новый SIM',
        max_length=50,
        blank=True,
        null=True
    )
    
    comment = models.TextField(
        'Комментарий',
        blank=True,
        null=True
    )
    
    is_active = models.BooleanField(
        'Активен',
        default=True
    )
    
    created_at = models.DateTimeField(
        'Дата создания',
        auto_now_add=True
    )
    
    class Meta:
        verbose_name = 'Трекер'
        verbose_name_plural = 'Трекеры'
        ordering = ['serial_number']
    
    def __str__(self):
        return f"{self.serial_number} (IMEI: {self.imei})"

class InstallationHistory(models.Model):
    """История установки трекеров на автомобили"""
    car = models.ForeignKey(
        Car,
        on_delete=models.CASCADE,
        related_name='installations',
        verbose_name='Автомобиль'
    )
    
    tracker = models.ForeignKey(
        Tracker,
        on_delete=models.CASCADE,
        related_name='installations',
        verbose_name='Трекер'
    )
    
    installation_date = models.DateField(
        'Дата установки'
    )
    
    removal_date = models.DateField(
        'Дата снятия',
        blank=True,
        null=True
    )
    
    is_active = models.BooleanField(
        'Активная установка',
        default=True
    )
    
    comment = models.TextField(
        'Комментарий к установке',
        blank=True,
        null=True
    )
    
    created_at = models.DateTimeField(
        'Дата создания записи',
        auto_now_add=True
    )
    
    class Meta:
        verbose_name = 'История установки'
        verbose_name_plural = 'История установок'
        ordering = ['-installation_date']
    
    def __str__(self):
        return f"{self.car.board_number} - {self.tracker.serial_number} ({self.installation_date})"

class OrderDocument(models.Model):
    """Модель для хранения сканов приказов"""
    car = models.ForeignKey(
        Car,
        on_delete=models.CASCADE,
        related_name='order_documents',
        verbose_name='Автомобиль'
    )
    
    document = models.FileField(
        'Скан документа',
        upload_to=order_scan_upload_path,
        validators=[
            FileExtensionValidator(['pdf', 'jpg', 'jpeg', 'png'])
        ]
    )
    
    document_type = models.CharField(
        'Тип документа',
        max_length=100,
        default='Приказ'
    )
    
    document_number = models.CharField(
        'Номер документа',
        max_length=100,
        blank=True,
        null=True
    )
    
    issue_date = models.DateField(
        'Дата документа'
    )
    
    comment = models.TextField(
        'Комментарий',
        blank=True,
        null=True
    )
    
    uploaded_at = models.DateTimeField(
        'Дата загрузки',
        auto_now_add=True
    )
    
    class Meta:
        verbose_name = 'Скан документа'
        verbose_name_plural = 'Сканы документов'
        ordering = ['-issue_date']
    
    def __str__(self):
        return f"{self.document_type} {self.document_number or ''} - {self.car.board_number}"
    
    def filename(self):
        return os.path.basename(self.document.name)


# --- Audit log model ---
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
try:
    # Django 3.1+: JSONField in django.db.models
    from django.db.models import JSONField
except Exception:
    # For older Django, fallback to TextField
    JSONField = None

class ActionLog(models.Model):
    ACTIONS = [
        ('create', 'Create'),
        ('update', 'Update'),
        ('delete', 'Delete'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Пользователь'
    )
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        verbose_name='Тип объекта'
    )
    object_id = models.CharField('ID объекта', max_length=255)
    content_object = GenericForeignKey('content_type', 'object_id')
    object_repr = models.CharField('Представление объекта', max_length=255)
    action = models.CharField('Действие', max_length=10, choices=ACTIONS)
    changes = JSONField('Изменения', null=True, blank=True) if JSONField else models.TextField('Изменения (JSON)', null=True, blank=True)
    timestamp = models.DateTimeField('Время', auto_now_add=True)
    request_path = models.CharField('Путь запроса', max_length=200, blank=True, null=True)
    ip_address = models.CharField('IP адрес', max_length=100, blank=True, null=True)

    class Meta:
        verbose_name = 'Лог действий'
        verbose_name_plural = 'Логи действий'
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.timestamp} - {self.user or 'system'} - {self.action} - {self.object_repr}"
