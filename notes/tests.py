from django.test import TestCase
from django.urls import reverse


# Create your tests here.

class TestRedirectToHome(TestCase):
    def test_redirect_to_home_logined(self):
        """GET '/' while logged in"""
        # Create Account
        from .models import Account
        self.u1 = Account.objects.create_user(username='testclient1',
                                              password='password')
        # Log in
        self.client.force_login(self.u1)

        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/home/')

    def test_redirect_to_home_not_logined(self):
        """GET '/' without logged in"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login/?next=/')


class TestSignupView(TestCase):
    def test_sign_up_view(self):
        """GET sigup view"""
        response = self.client.get(reverse('notes:signup'))
        self.assertEqual(response.status_code, 200)


class TestCreateUser(TestCase):
    def test_create_user(self):
        """Create user with POST"""
        from .models import Account

        post_data = {'username': 'testclient1', 'password': 'password'}

        response = self.client.post(reverse('notes:create_user'), post_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('notes:login'))
        self.assertQuerysetEqual(Account.objects.all(),
                                 ['<Account: testclient1>'])

    def test_create_user_get(self):
        """GET"""
        response = self.client.get(reverse('notes:create_user'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('notes:signup'))


class TestLoginView(TestCase):
    @classmethod
    def setUpTestData(cls):
        from .models import Account
        cls.u1 = Account.objects.create_user(username='testclient1',
                                             password='password')
        cls.url = reverse('notes:login')

    def test_login_view_without_logged_in(self):
        """Come to this view without logging in"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_login_view_while_logged_in(self):
        """Come to this view while logging in"""
        self.client.force_login(self.u1)

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('notes:home'))

    def test_login_view_post_correct_user(self):
        """POST registered user information"""
        post_data = {
            'username': 'testclient1',
            'password': 'password'
        }

        response = self.client.post(self.url, post_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('notes:home'))

    def test_login_view_post_wrong_user(self):
        """POST not registered user information"""
        post_data = {
            'username': 'testclient100',
            'password': 'pass',
        }
        response = self.client.post(self.url, post_data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'ユーザ名かパスワードが間違っています')


class TestHomeView(TestCase):

    def _follow(self, follow_user, follower_user):
        from .models import Follow
        f = Follow(follow=follow_user, follower=follower_user)
        f.save()

    def _create_note(self, author, text):
        from .models import Notes
        note = Notes(author=author, text=text)
        note.save()

    @classmethod
    def setUpTestData(cls):
        from .models import Account
        cls.u1 = Account.objects.create_user(username='testclient1',
                                             password='password')
        cls.u2 = Account.objects.create_user(username='testclient2',
                                             password='password')
        cls.u3 = Account.objects.create_user(username='testclient3',
                                             password='password')

        cls.url = reverse('notes:home')

    def test_home_view_status_code_200(self):
        """GET URL while logged in"""
        self.client.force_login(self.u1)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_home_view_status_code_302(self):
        """GET URL without logged in"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login/?next=/home/')

    def test_home_view_display_notes(self):
        """
        Check extracted notes from follow relationships

        u1: follow u2, noted 'hello'
        u2: follow   , noted 'world'
        u3: follow   , noted
        """
        self._create_note(self.u1, 'hello')
        self._create_note(self.u2, 'world')
        self._follow(self.u1, self.u2)

        # Check u1 context
        self.client.force_login(self.u1)
        response = self.client.get(self.url)
        self.assertQuerysetEqual(
            response.context['notes_list'],
            ['<Notes: testclient2:world>', '<Notes: testclient1:hello>'])
        self.client.logout()

        # Check u2 context
        self.client.force_login(self.u2)
        response = self.client.get(self.url)
        self.assertQuerysetEqual(
            response.context['notes_list'],
            ['<Notes: testclient2:world>'])
        self.client.logout()

        # Check u3 context
        self.client.force_login(self.u3)
        response = self.client.get(self.url)
        self.assertQuerysetEqual(
            response.context['notes_list'],
            [])
        self.client.logout()

    def test_home_view_search_notes(self):
        """
        Check the search function for notes extracted from follow relationships
        """
        self._create_note(self.u1, 'aaaaa')
        self._create_note(self.u1, 'bbbbb')
        self._create_note(self.u2, 'abbbb')
        self._create_note(self.u2, 'bbbbb')
        self._follow(self.u1, self.u2)

        self.client.force_login(self.u1)

        response = self.client.get(self.url, {'q': 'a'})
        self.assertQuerysetEqual(
            response.context['notes_list'],
            ['<Notes: testclient2:abbbb>', '<Notes: testclient1:aaaaa>'])
        self.client.logout()


class TestNotesView(TestCase):

    def _follow(self, follow_user, follower_user):
        from .models import Follow
        f = Follow(follow=follow_user, follower=follower_user)
        f.save()

    def _create_note(self, author, text):
        from .models import Notes
        note = Notes(author=author, text=text)
        note.save()

    @classmethod
    def setUpTestData(cls):
        from .models import Account
        cls.u1 = Account.objects.create_user(username='testclient1',
                                             password='password')
        cls.u2 = Account.objects.create_user(username='testclient2',
                                             password='password')
        cls.u3 = Account.objects.create_user(username='testclient3',
                                             password='password')
        cls.url = reverse('notes:notes')

    def test_notes_view_status_code_200(self):
        """GET URL while logged in"""
        self.client.force_login(self.u1)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_notes_view_status_code_302(self):
        """GET URL without logged in"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login/?next=/notes/')

    def test_notes_view_display_notes(self):
        """
        Check extract notes from follow relationships
        u1: noted 'test1'
        u2: noted 'test2'
        u3: noted 'test3'
        """
        self._create_note(self.u1, 'test1')
        self._create_note(self.u2, 'test2')
        self._create_note(self.u3, 'test3')

        # Check if all notes can be extracted
        self.client.force_login(self.u1)
        response = self.client.get(self.url)
        self.assertQuerysetEqual(
            response.context['notes_list'],
            ['<Notes: testclient3:test3>',
             '<Notes: testclient2:test2>',
             '<Notes: testclient1:test1>', ])

    def test_notes_view_search_notes(self):
        """Check the search function for all notes"""
        self._create_note(self.u1, 'aaaaa')
        self._create_note(self.u1, 'bbbbb')
        self._create_note(self.u2, 'aaaaa')
        self._create_note(self.u2, 'bbbbb')
        self._create_note(self.u3, 'aaaaa')
        self._create_note(self.u3, 'bbbbb')

        # Check if all notes can be extracted by search words
        self.client.force_login(self.u1)
        response = self.client.get(self.url, {'q': 'a'})
        self.assertQuerysetEqual(
            response.context['notes_list'],
            ['<Notes: testclient3:aaaaa>',
             '<Notes: testclient2:aaaaa>',
             '<Notes: testclient1:aaaaa>']
        )


class TestUsersView(TestCase):

    def _follow(self, follow_user, follower_user):
        from .models import Follow
        f = Follow(follow=follow_user, follower=follower_user)
        f.save()

    def _create_note(self, author, text):
        from .models import Notes
        note = Notes(author=author, text=text)
        note.save()

    @classmethod
    def setUpTestData(cls):
        from .models import Account
        cls.u1 = Account.objects.create_user(username='testclient1',
                                             password='password')
        cls.u2 = Account.objects.create_user(username='testclient2',
                                             password='password')
        cls.u3 = Account.objects.create_user(username='testclient3',
                                             password='password')
        cls.url = reverse('notes:users')

    def test_users_view_status_code_200(self):
        """GET URL while logged in"""
        self.client.force_login(self.u1)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_users_view_status_code_302(self):
        """GET URL without logged in"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login/?next=/users/')

    def test_users_view_get_users(self):
        """Get all users"""
        self.client.force_login(self.u1)
        response = self.client.get(self.url)
        self.assertQuerysetEqual(
            response.context['users_list'],
            ['<Account: testclient1>',
             '<Account: testclient2>',
             '<Account: testclient3>'], ordered=False)

    def test_users_view_get_users_by_searchword(self):
        """Get all users by search word"""
        self.client.force_login(self.u1)
        response = self.client.get(self.url, {'q': '1'})
        self.assertQuerysetEqual(
            response.context['users_list'],
            ['<Account: testclient1>'], ordered=False)


class TestUserView(TestCase):

    def _follow(self, follow_user, follower_user):
        from .models import Follow
        f = Follow(follow=follow_user, follower=follower_user)
        f.save()

    def _create_note(self, author, text):
        from .models import Notes
        note = Notes(author=author, text=text)
        note.save()

    @classmethod
    def setUpTestData(cls):
        from .models import Account
        cls.u1 = Account.objects.create_user(username='testclient1',
                                             password='password')
        cls.u2 = Account.objects.create_user(username='testclient2',
                                             password='password')
        cls.u3 = Account.objects.create_user(username='testclient3',
                                             password='password')

    def test_user_view_status_code_200(self):
        """GET URL while logged in"""
        self.client.force_login(self.u1)

        url = reverse('notes:user_page', args=(self.u1.pk,))
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_user_view_status_code_302(self):
        """GET URL without logged in"""
        url = reverse('notes:user_page', args=(self.u1.pk,))
        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'/login/?next=/user/{self.u1.pk}')

    def test_user_view_get_target_user(self):
        """Get target user of target page"""
        self.client.force_login(self.u1)

        url = reverse('notes:user_page', args=(self.u2.pk,))
        response = self.client.get(url)

        self.assertEqual(
            response.context['target_user'], self.u2)

    def test_user_view_get_num_follow(self):
        """Get the number of follows of the target user"""
        self._follow(self.u1, self.u2)
        self._follow(self.u1, self.u3)

        self.client.force_login(self.u1)

        url = reverse('notes:user_page', args=(self.u1.pk,))
        response = self.client.get(url)

        self.assertEqual(response.context['num_follow'], 2)

    def test_user_view_get_num_follower(self):
        """Get the number of followers of the target user"""
        self._follow(self.u2, self.u1)
        self._follow(self.u3, self.u1)

        self.client.force_login(self.u1)

        url = reverse('notes:user_page', args=(self.u1.pk,))
        response = self.client.get(url)

        self.assertEqual(response.context['num_follower'], 2)

    def test_user_view_get_is_follow(self):
        """Get Whether the logged-in user is following the target user"""
        self._follow(self.u1, self.u2)

        self.client.force_login(self.u1)

        url = reverse('notes:user_page', args=(self.u2.pk,))
        response = self.client.get(url)

        self.assertEqual(response.context['is_follow'], True)

    def test_user_view_get_notes(self):
        """Get user notes"""
        self._create_note(self.u1, 'aaaaa')
        self._create_note(self.u1, 'bbbbb')
        self._create_note(self.u1, 'ccccc')

        self.client.force_login(self.u1)

        url = reverse('notes:user_page', args=(self.u1.pk,))
        response = self.client.get(url)

        self.assertQuerysetEqual(
            response.context['target_user_notes_list'],
            ['<Notes: testclient1:ccccc>',
             '<Notes: testclient1:bbbbb>',
             '<Notes: testclient1:aaaaa>'],
            ordered=True)

    def test_user_view_get_notes_by_searchword(self):
        """Get user notes by search word"""
        self._create_note(self.u1, 'aaaaa')
        self._create_note(self.u1, 'bbbbb')
        self._create_note(self.u1, 'ccccc')
        self._create_note(self.u1, 'adddd')

        self.client.force_login(self.u1)

        url = reverse('notes:user_page', args=(self.u1.pk,))
        response = self.client.get(url, {'q': 'a'})

        self.assertQuerysetEqual(
            response.context['target_user_notes_list'],
            ['<Notes: testclient1:adddd>',
             '<Notes: testclient1:aaaaa>'], ordered=True)


class TestSettingsView(TestCase):
    @classmethod
    def setUpTestData(cls):
        from .models import Account
        cls.u1 = Account.objects.create_user(username='testclient1',
                                             password='password')
        cls.u2 = Account.objects.create_user(username='testclient2',
                                             password='password')

    def test_settings_view_status_code_200(self):
        """GET URL while logged in"""
        self.client.force_login(self.u1)
        url = reverse('notes:settings', args=(self.u1.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_settings_view_status_code_302(self):
        """GET URL without logged in"""
        url = reverse('notes:settings', args=(self.u1.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'/login/?next=/settings/{self.u1.pk}')

    def test_settings_view_account(self):
        """Whether it is my setting page"""

        # Whether u1 object is passed when logging in as u1
        self.client.force_login(self.u1)
        url = reverse('notes:settings', args=(self.u1.pk,))
        response = self.client.get(url)
        self.assertEqual(response.context['object'], self.u1)
        self.client.logout()

        # Whether u2 object is passed when logging in as u2
        self.client.force_login(self.u2)
        url = reverse('notes:settings', args=(self.u2.pk,))
        response = self.client.get(url)
        self.assertEqual(response.context['object'], self.u2)
        self.client.logout()
