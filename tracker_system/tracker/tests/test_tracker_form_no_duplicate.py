from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from tracker.models import Tracker, Location, Car

class TrackerFormRenderTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user('u4','u4@example.com','pw')
        self.client = Client()
        self.client.login(username='u4', password='pw')
        self.loc = Location.objects.create(name='Lx')
        self.car = Car.objects.create(board_number='BX1', state_number='SX1', model='Other', location=self.loc)
        self.tr = Tracker.objects.create(imei='777777777777777', serial_number='SN7', inventory_number_tracker='INV7', model='Model7')

    def test_current_car_field_rendered_once_on_edit(self):
        url = reverse('tracker:tracker_update', kwargs={'pk': self.tr.pk})
        r = self.client.get(url)
        self.assertEqual(r.status_code, 200)
        content = r.content.decode('utf-8')
        # id should appear exactly once
        self.assertEqual(content.count('id="id_current_car"'), 1)
        # name should appear exactly once
        self.assertEqual(content.count('name="current_car"'), 1)
        # current location hint should be present once
        self.assertIn('Текущая локация', content)
