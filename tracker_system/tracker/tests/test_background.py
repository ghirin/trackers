from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse

class BackgroundTests(TestCase):
    def test_dashboard_has_background_css(self):
        User = get_user_model()
        u = User.objects.create_user('u1', 'u1@example.com', 'pw')
        c = Client()
        c.login(username='u1', password='pw')
        url = reverse('tracker:dashboard')
        r = c.get(url)
        self.assertEqual(r.status_code, 200)
        content = r.content.decode('utf-8')
        # Ensure CSS includes our static image path (new original image)
        self.assertIn('tracker/img/RenaultMaster.jpg', content)
