from django.db import migrations, models


def create_locations(apps, schema_editor):
    Location = apps.get_model('tracker', 'Location')
    choices = getattr(Location, 'LOCATION_CHOICES', None)
    if not choices:
        # Fallback list
        choices = [
            ('Other','Other'),
        ]
    for val, label in choices:
        Location.objects.get_or_create(name=label)


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0003_merge'),
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True, verbose_name='Локация')),
            ],
            options={'verbose_name': 'Локация', 'verbose_name_plural': 'Локации', 'ordering': ['name']},
        ),
        migrations.RunPython(create_locations, lambda apps, schema_editor: None),
    ]
