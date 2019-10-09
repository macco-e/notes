from django.test import LiveServerTestCase
from django.urls import reverse
from selenium.webdriver.chrome.webdriver import WebDriver


class LoginTest(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def setUp(self):
        self.selenium.get('http://localhost:8000' + str(reverse('notes:login')))

    def test_login_success(self):
        username_input = self.selenium.find_element_by_name("username")
        username_input.send_keys('admin')
        password_input = self.selenium.find_element_by_name("password")
        password_input.send_keys('admin')
        self.selenium.find_element_by_class_name('btn').click()

        self.assertEquals('Home', self.selenium.title)

    def test_login_failed(self):
        username_input = self.selenium.find_element_by_name("username")
        username_input.send_keys('adminnnn')
        password_input = self.selenium.find_element_by_name("password")
        password_input.send_keys('adminnnnn')
        self.selenium.find_element_by_class_name('btn').click()

        self.assertEquals('Login', self.selenium.title)
        element = self.selenium.find_element_by_class_name('login-error-msg')
        self.assertIn(element.text, 'ユーザ名かパスワードが間違っています')


class LogoutTest(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()

        cls.selenium.get('http://localhost:8000' + str(reverse('notes:login')))

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def setUp(self):
        self.selenium.get('http://localhost:8000' + str(reverse('notes:login')))

    def test_logout(self):
        username_input = self.selenium.find_element_by_name("username")
        username_input.send_keys('admin')
        password_input = self.selenium.find_element_by_name("password")
        password_input.send_keys('admin')

        # log in
        self.selenium.find_element_by_class_name('btn').click()
        self.assertEquals('Home', self.selenium.title)

        # log out
        # element click will be intercepted by #djHideToolBarButton
        element = self.selenium.find_element_by_class_name('logout-btn')
        self.selenium.execute_script("arguments[0].click();", element)
        self.assertEquals('Login', self.selenium.title)


class TestHome(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.get('http://localhost:8000' + str(reverse('notes:login')))

        # Log in
        username_input = cls.selenium.find_element_by_name("username")
        username_input.send_keys('admin')
        password_input = cls.selenium.find_element_by_name("password")
        password_input.send_keys('admin')
        cls.selenium.find_element_by_class_name('btn').click()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def setUp(self):
        self.selenium.get('http://localhost:8000' + str(reverse('notes:home')))

    def test_home_view(self):
        # Login username
        element = self.selenium.find_element_by_class_name('navbar-brand')
        self.assertIn(element.text, 'admin')

        # Dashboard title
        element = self.selenium.find_element_by_tag_name('h1')
        self.assertIn(element.text, 'Home')

    def test_home_view_link(self):
        # Link Home
        self.selenium.get('http://localhost:8000' + str(reverse('notes:home')))
        self.selenium.find_element_by_link_text('Home').click()
        element = self.selenium.find_element_by_tag_name('h1')
        self.assertIn(element.text, 'Home')

        # Link All notes
        self.selenium.get('http://localhost:8000' + str(reverse('notes:home')))
        self.selenium.find_element_by_link_text('All notes').click()
        element = self.selenium.find_element_by_tag_name('h1')
        self.assertIn(element.text, 'All notes')

        # Link Users
        self.selenium.get('http://localhost:8000' + str(reverse('notes:home')))
        self.selenium.find_element_by_link_text('Users').click()
        element = self.selenium.find_element_by_tag_name('h1')
        self.assertIn(element.text, 'Users')

        # Link My page
        self.selenium.get('http://localhost:8000' + str(reverse('notes:home')))
        self.selenium.find_element_by_link_text('My page').click()
        element = self.selenium.find_element_by_class_name('target-username')
        self.assertIn(element.text, '@ admin')

        # Link settings
        self.selenium.get('http://localhost:8000' + str(reverse('notes:home')))
        self.selenium.find_element_by_link_text('settings').click()
        element = self.selenium.find_element_by_tag_name('h1')
        self.assertIn(element.text, 'Settings @admin')
