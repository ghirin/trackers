from django.db import migrations, models


def migrate_locations(apps, schema_editor):
    Car = apps.get_model('tracker', 'Car')
    Location = apps.get_model('tracker', 'Location')
    for car in Car.objects.all():
        loc_name = car.location
        if loc_name:
            try:
                loc = Location.objects.get(name__iexact=loc_name)
            except Location.DoesNotExist:
                loc, _ = Location.objects.get_or_create(name=loc_name)
            # the field was temporarily created as 'location_id' (a ForeignKey),
            # so assign the Location instance (not an integer id)
            car.location_id = loc
            car.save()


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0004_create_location'),
    ]

    operations = [
        migrations.AddField(
            model_name='car',
            name='location_id',
            field=models.ForeignKey(null=True, blank=True, on_delete=models.SET_NULL, related_name='cars', to='tracker.Location'),
        ),
        migrations.RunPython(migrate_locations, lambda apps, schema_editor: None),
        migrations.RemoveField(
            model_name='car',
            name='location',
        ),
        migrations.RenameField(
            model_name='car',
            old_name='location_id',
            new_name='location',
        ),
    ]
