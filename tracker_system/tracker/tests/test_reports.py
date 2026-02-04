from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from tracker.models import Car, Tracker, InstallationHistory, Location
from datetime import date

class ReportsExportTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user('t', 't@example.com', 'pw')
        self.client = Client()
        self.client.login(username='t', password='pw')

        loc = Location.objects.create(name='TestLoc')
        car = Car.objects.create(board_number='B1', state_number='S1', model='Other', location=loc)
        tracker = Tracker.objects.create(imei='123456789012345', serial_number='SN1', inventory_number_tracker='INV1', model='ModelX')
        InstallationHistory.objects.create(car=car, tracker=tracker, installation_date=date(2026,1,1), is_active=True)

    def test_filter_by_imei(self):
        r = self.client.get('/tracker/reports/?imei=1234', HTTP_HOST='127.0.0.1')
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, '123456789012345')

    def test_export_with_filters(self):
        r = self.client.get('/tracker/reports/export/?date_from=2026-01-01&date_to=2026-12-31&location=%s' % Location.objects.first().id, HTTP_HOST='127.0.0.1')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r['Content-Type'], 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
