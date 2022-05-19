from django.test import TestCase
from django.urls import resolve
from .views import index

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from django.urls import reverse
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.utils.translation import activate


class UserAuthenticationTestCase(TestCase):

    def test_root_url_resolves_to_index_view(self):
        found = resolve('/')
        self.assertEqual(found.func, index)


class TestGoogleLogin(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)
        self.browser.wait = WebDriverWait(self.browser, 10)
        activate('es')

    def tearDown(self):
        self.browser.quit()

    def get_element_by_id(self, element_id):
        return self.browser.wait.until(EC.presence_of_element_located((By.ID, element_id)))

    def get_button_by_id(self, element_id):
        return self.browser.wait.until(EC.element_to_be_clickable((By.ID, element_id)))

    def get_full_url(self, namespace):
        return self.live_server_url + reverse(namespace)

    def test_google_login(self):
        self.browser.get(self.get_full_url("index"))
        google_login = self.get_element_by_id("google_login")
        with self.assertRaises(TimeoutException):
            self.get_element_by_id("logout")
        self.assertEqual(
            google_login.get_attribute("href"),
            self.live_server_url + "/accounts/google/login/")
        google_login.click()
        with self.assertRaises(TimeoutException):
            self.get_element_by_id("google_login")
        google_logout = self.get_element_by_id("logout")
        google_logout.click()
