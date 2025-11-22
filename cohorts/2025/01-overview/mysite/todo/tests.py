from django.test import TestCase, Client
from django.template.loader import render_to_string
from django.urls import reverse, NoReverseMatch
from .models import Task

class TaskModelTests(TestCase):
    def test_create_task_defaults(self):
        t = Task.objects.create(title='Test task')
        self.assertEqual(str(t), 'Test task')
        self.assertFalse(t.completed)
        self.assertIsNotNone(t.created_at)

    def test_title_required(self):
        # If your model enforces blank=False (default), creating without title should raise
        with self.assertRaises(Exception):
            Task.objects.create(title='')  # may raise IntegrityError or ValidationError depending on model

class TemplateTests(TestCase):
    def test_base_and_home_templates_render(self):
        # ensure templates render without raising template errors
        rendered = render_to_string('todo/home.html', {})
        self.assertIn('My TODO App', rendered)  # base.html contains this header

class HomeViewTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_home_view_status_and_template(self):
        try:
            url = reverse('home')
        except NoReverseMatch:
            self.skipTest("No URL named 'home' found; add `path('', views.home, name='home')` to `todo/urls.py` and include it in project urls.")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'todo/home.html')

    def test_home_shows_tasks(self):
        # create a few tasks and make sure their titles show up in home rendering
        Task.objects.create(title='A')
        Task.objects.create(title='B', completed=True)
        try:
            url = reverse('home')
        except NoReverseMatch:
            self.skipTest("No URL named 'home' found; skipping display test.")
        resp = self.client.get(url)
        self.assertContains(resp, 'A')
        self.assertContains(resp, 'B')