import time

from django.apps import apps
from django.conf import settings
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import resolve_url
from django.test import Client
from django.test import LiveServerTestCase
from django.test import TestCase
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.webdriver import WebDriver

from sample.models import Movement
from sample.models import Tag

AUTH_USER_MODEL = apps.get_model(settings.AUTH_USER_MODEL)


class TagTest(TestCase):
    def setUp(self):
        Tag.objects.bulk_create([
            Tag(name='a'),
            Tag(name='b'),
        ])

    def test_count(self):
        self.assertEqual(Tag.objects.count(), 2)

    def test_get_by_name(self):
        self.assertIsNotNone(Tag.objects.get(name='a'))

    def test_object_not_found(self):
        with self.assertRaises(ObjectDoesNotExist):
            Tag.objects.get(name='z')


class MovementSuperuserViewTest(LiveServerTestCase):
    def setUp(self):
        username = 'root_tester'
        password = 'pass123'
        user = AUTH_USER_MODEL(username=username, is_superuser=True, is_staff=True)
        user.set_password(password)
        user.save()
        self.client = Client()
        self.client.login(username=username, password=password)

    def test_empty_list(self):
        response = self.client.get(resolve_url('sample:web:movement-list'))
        self.assertEqual(response.status_code, 200)
        tags = response.context['object_list']
        self.assertEqual(len(tags), 0)

    def test_list(self):
        Movement.objects.create(value=100, remark='test')
        response = self.client.get(resolve_url('sample:web:movement-list'))
        self.assertEqual(response.status_code, 200)
        tags = response.context['object_list']
        self.assertEqual(len(tags), 1)


class MovementNoneuserViewTest(LiveServerTestCase):
    def setUp(self):
        username = 'none_tester'
        password = 'pass123'
        user = AUTH_USER_MODEL(username=username, is_superuser=False, is_staff=False)
        user.set_password(password)
        user.save()
        self.client = Client()
        self.client.login(username=username, password=password)

    def test_list(self):
        response = self.client.get(resolve_url('sample:web:movement-list'))
        self.assertEqual(response.status_code, 302)


class TagITest(StaticLiveServerTestCase):
    username = 'root_tester'
    password = 'pass123'

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.browser = WebDriver()
        cls.browser.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        super().tearDownClass()

    def resolve_url(self, *args, **kwargs):
        return self.live_server_url + resolve_url(*args, **kwargs)

    def setUp(self):
        user = AUTH_USER_MODEL(username=self.username, is_superuser=True, is_staff=True)
        user.set_password(self.password)
        user.save()

    def test_add(self):
        self.browser.get(self.resolve_url('admin:login'))
        username_input = self.browser.find_element_by_name('username')
        username_input.send_keys(self.username)
        password_input = self.browser.find_element_by_name('password')
        password_input.send_keys(self.password)
        password_input.send_keys(Keys.ENTER)
        time.sleep(0.1)
        self.browser.get(self.live_server_url + '/admin/sample/tag/add')
        self.browser.find_element_by_name('name').send_keys('tag-name')
        self.browser.find_element_by_name('_save').click()
        self.assertIsNotNone(Tag.objects.get(name='tag-name'))
