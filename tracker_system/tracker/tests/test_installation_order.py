from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from tracker.models import Car, Tracker, InstallationHistory, Location, OrderDocument
from datetime import date

class InstallationOrderTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user('u3','u3@example.com','pw')
        self.client = Client()
        self.client.login(username='u3', password='pw')
        self.loc = Location.objects.create(name='LOC')
        self.car = Car.objects.create(board_number='BX', state_number='SX', model='Other', location=self.loc)
        self.tr = Tracker.objects.create(imei='888888888888888', serial_number='SNX2', inventory_number_tracker='INVY', model='ModelA')
        self.order = OrderDocument.objects.create(car=self.car, document='test.pdf', document_type='Приказ', document_number='ORD-1', issue_date=date(2024,1,1))

    def test_installation_requires_order(self):
        url = reverse('tracker:installation_create')
        # ensure no orders exist
        from tracker.models import OrderDocument
        OrderDocument.objects.all().delete()
        r = self.client.get(url)
        self.assertEqual(r.status_code, 200)
        content = r.content.decode('utf-8')
        # page should advise creating a new order
        self.assertIn('Создать новый элемент', content)
        data = {
            'car': str(self.car.pk),
            'tracker': str(self.tr.pk),
            'installation_date': '2024-01-01',
            'is_active': 'on',
            'comment': 'no order'
        }
        r = self.client.post(url, data)
        self.assertEqual(r.status_code, 200)
        # Required field error should be present
        self.assertIn('Обязательное поле.', r.content.decode('utf-8'))

    def test_installation_with_order_succeeds(self):
        url = reverse('tracker:installation_create')
        data = {
            'car': str(self.car.pk),
            'tracker': str(self.tr.pk),
            'installation_date': '2024-01-01',
            'is_active': 'on',
            'order_document': str(self.order.pk),
            'comment': 'with order'
        }
        r = self.client.post(url, data, follow=True)
        self.assertEqual(r.status_code, 200)
        inst = InstallationHistory.objects.filter(tracker=self.tr, car=self.car, order_document=self.order)
        self.assertTrue(inst.exists())

    def test_update_form_with_attached_order_hides_create_prompt(self):
        # Create an installation already associated with an order and open its edit page
        inst = InstallationHistory.objects.create(car=self.car, tracker=self.tr, installation_date=date(2024,1,1), is_active=True, order_document=self.order)
        url = reverse('tracker:installation_update', args=[inst.pk])
        r = self.client.get(url)
        self.assertEqual(r.status_code, 200)
        content = r.content.decode('utf-8')
        # The warning about missing orders should NOT be present when the current record already has an order
        self.assertNotIn('Нет доступных приказов', content)
        self.assertNotIn('Создать новый элемент', content)

    def test_installation_list_hides_global_create_prompt_when_orders_exist(self):
        # The installations list shouldn't show the global "no orders" warning when at least one OrderDocument exists
        url = reverse('tracker:installation_list')
        r = self.client.get(url)
        self.assertEqual(r.status_code, 200)
        content = r.content.decode('utf-8')
        self.assertNotIn('Нет доступных приказов', content)
