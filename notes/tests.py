from django.test import TestCase
from django.urls import resolve, reverse

# Create your tests here.

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
        cls.u1 = Account.objects.create_user(username='testclient1', password='password')
        cls.u2 = Account.objects.create_user(username='testclient2', password='password')
        cls.u3 = Account.objects.create_user(username='testclient3', password='password')

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

