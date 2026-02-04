from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from tracker.models import Car, Tracker, InstallationHistory, Location
from django.utils import timezone
from datetime import date

class TrackerAssignmentTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user('u2','u2@example.com','pw')
        self.client = Client()
        self.client.login(username='u2', password='pw')
        self.loc1 = Location.objects.create(name='LocA')
        self.loc2 = Location.objects.create(name='LocB')
        self.car1 = Car.objects.create(board_number='B10', state_number='S10', model='Other', location=self.loc1)
        self.car2 = Car.objects.create(board_number='B20', state_number='S20', model='Other', location=self.loc2)
        self.tracker = Tracker.objects.create(imei='999999999999999', serial_number='SNX', inventory_number_tracker='INVX', model='ModelZ')

    def test_assign_via_update_creates_installation(self):
        url = reverse('tracker:tracker_update', kwargs={'pk': self.tracker.pk})
        data = {
            'imei': self.tracker.imei,
            'serial_number': self.tracker.serial_number,
            'inventory_number_tracker': self.tracker.inventory_number_tracker,
            'inventory_number_antenna': '',
            'model': self.tracker.model,
            'protocol': self.tracker.protocol,
            'holder_number': '',
            'sim_old': '',
            'n_card': '',
            'sim_new': '',
            'comment': '',
            'is_active': 'on',
            'current_car': str(self.car1.pk),
        }
        resp = self.client.post(url, data, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.tracker.refresh_from_db()
        self.assertEqual(self.tracker.current_location, self.car1.location.name)
        inst = InstallationHistory.objects.filter(tracker=self.tracker, car=self.car1, is_active=True)
        self.assertTrue(inst.exists())

    def test_reassign_deactivates_previous_and_creates_new(self):
        # create initial installation to car1
        InstallationHistory.objects.create(car=self.car1, tracker=self.tracker, installation_date=date(2021,1,1), is_active=True)
        url = reverse('tracker:tracker_update', kwargs={'pk': self.tracker.pk})
        data = {
            'imei': self.tracker.imei,
            'serial_number': self.tracker.serial_number,
            'inventory_number_tracker': self.tracker.inventory_number_tracker,
            'inventory_number_antenna': '',
            'model': self.tracker.model,
            'protocol': self.tracker.protocol,
            'holder_number': '',
            'sim_old': '',
            'n_card': '',
            'sim_new': '',
            'comment': '',
            'is_active': 'on',
            'current_car': str(self.car2.pk),
        }
        resp = self.client.post(url, data, follow=True)
        self.assertEqual(resp.status_code, 200)
        # previous active should be deactivated
        self.assertFalse(InstallationHistory.objects.filter(tracker=self.tracker, car=self.car1, is_active=True).exists())
        self.assertTrue(InstallationHistory.objects.filter(tracker=self.tracker, car=self.car2, is_active=True).exists())

    def test_clear_assignment_deactivates_active(self):
        InstallationHistory.objects.create(car=self.car1, tracker=self.tracker, installation_date=date(2022,6,1), is_active=True)
        url = reverse('tracker:tracker_update', kwargs={'pk': self.tracker.pk})
        data = {
            'imei': self.tracker.imei,
            'serial_number': self.tracker.serial_number,
            'inventory_number_tracker': self.tracker.inventory_number_tracker,
            'inventory_number_antenna': '',
            'model': self.tracker.model,
            'protocol': self.tracker.protocol,
            'holder_number': '',
            'sim_old': '',
            'n_card': '',
            'sim_new': '',
            'comment': '',
            'is_active': 'on',
            # no current_car posted -> should clear
        }
        resp = self.client.post(url, data, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertFalse(InstallationHistory.objects.filter(tracker=self.tracker, is_active=True).exists())
