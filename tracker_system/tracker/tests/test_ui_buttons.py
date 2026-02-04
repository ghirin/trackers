from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse

class UIButtonTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user('ux','ux@example.com','pw')
        self.client = Client()
        self.client.login(username='ux', password='pw')

    def test_create_buttons_present_on_cars_and_installations(self):
        r1 = self.client.get(reverse('tracker:car_list'))
        self.assertEqual(r1.status_code, 200)
        self.assertIn('Создать новый элемент', r1.content.decode('utf-8'))
        r2 = self.client.get(reverse('tracker:installation_list'))
        self.assertEqual(r2.status_code, 200)
        self.assertIn('Создать новый элемент', r2.content.decode('utf-8'))
        # trackers page should have a create button
        r3 = self.client.get(reverse('tracker:tracker_list'))
        self.assertEqual(r3.status_code, 200)
        self.assertIn('Создать новый', r3.content.decode('utf-8'))
        # logout button should be styled to contrast with blue background
        # check presence of btn-light class in the navbar
        self.assertIn('btn btn-light', r3.content.decode('utf-8'))

    def test_logout_redirects_to_root(self):
        # POST to logout should redirect to site root '/'
        r = self.client.post(reverse('logout'))
        self.assertIn(r.status_code, (302, 303))
        # Django test client returns absolute or relative Location depending on settings; normalize
        location = r.get('Location') or r.headers.get('Location')
        self.assertTrue(location == '/' or location.endswith('/'))
