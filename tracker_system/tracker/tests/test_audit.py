from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from tracker.models import Location, Car, ActionLog

class AuditLogTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user('t','t@example.com','pw')
        self.client = Client()
        self.client.login(username='t', password='pw')
        self.loc = Location.objects.create(name='AuditLoc')
        self.car = Car.objects.create(board_number='B1', state_number='S1', model='Other', location=self.loc)

    def test_update_creates_actionlog(self):
        url = f'/tracker/cars/{self.car.pk}/update/'
        r = self.client.post(url, {'board_number':'B1','state_number':'S2','model':'Other','location':self.loc.id,'comment':'x'})
        self.assertIn(r.status_code, (200,302))
        log = ActionLog.objects.filter(content_type__model='car', object_id=str(self.car.pk)).order_by('-timestamp').first()
        self.assertIsNotNone(log)
        self.assertEqual(log.action, 'update')
        self.assertTrue('state_number' in (log.changes or {}))
