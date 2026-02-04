from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.template.loader import get_template
from django.urls import reverse

class AdminTemplateTests(TestCase):
    def test_actionlog_change_list_template_and_admin_page(self):
        # Template loader can find the template
        tpl = get_template('admin/tracker/actionlog/change_list.html')
        self.assertIsNotNone(tpl)

        # Admin changelist is accessible to a superuser
        User = get_user_model()
        admin = User.objects.create_superuser(username='admin', email='admin@example.com', password='pw')
        c = Client()
        logged_in = c.login(username='admin', password='pw')
        self.assertTrue(logged_in)
        url = reverse('admin:tracker_actionlog_changelist')
        r = c.get(url)
        self.assertEqual(r.status_code, 200)
