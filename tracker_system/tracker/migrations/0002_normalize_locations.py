"""Normalize existing Car.location values to standard choices"""
from django.db import migrations

LOCATIONS = [
    'Андрушівка','Баранівка','Бараші','Бердичів місто','Бердичівський р-н','Білокоровичі','Бондарі','Брусилів','Городниця','Ємільчино','Житомир ППБ1','Житомир Центр','Житомир Центр ПС1','Житомир Центр ПС2','Звягель','Іванопіль','Іршанск','Корнин','Коростень місто','Коростень р-н','Коростишів','Лугини','Любар','Малин','Миропіль','Н.Борова','Народичі','Овруч','Олевск','Поліське','Попільня','Потіївка','Пулини','Радовель','Радомишль','Романів','Ружин','сим в АССу','Словечне','Тойота','установ на Тойота','Хорошів','Черняхів','Чоповичі','Чуднів','Ярунь'
]


def normalize_locations(apps, schema_editor):
    Car = apps.get_model('tracker', 'Car')
    for car in Car.objects.all():
        if car.location and car.location.strip():
            loc = car.location.strip()
            # case-insensitive match
            matched = None
            for canonical in LOCATIONS:
                if loc.lower() == canonical.lower():
                    matched = canonical
                    break
            if matched:
                if car.location != matched:
                    car.location = matched
                    car.save()
            else:
                # If not in known list, mark as Other
                if car.location != 'Other':
                    car.location = 'Other'
                    car.save()


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(normalize_locations, lambda apps, schema_editor: None),
    ]
