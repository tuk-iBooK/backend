from django.test import TestCase
from users.models import User

class UserTestCase(TestCase):
    def test_create_user(self):
        user = User.objects.create_user(email='test@example.com', nickname='testuser', password='testpassword')
        self.assertEqual(user.email, 'test@example.com')
        self.assertEqual(user.nickname, 'testuser')
        self.assertTrue(user.check_password('testpassword'))
        self.assertTrue(user.is_active)
