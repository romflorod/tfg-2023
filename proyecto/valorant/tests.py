from django.test import TestCase
from django.contrib.auth.models import User
from users.models import Profile


class test(TestCase):
    def setUp(self):
        User.objects.create(username="UserTest1", password="tester123")

    def testUserCreate(self):
        UserTest = User.objects.get(username="UserTest1")
        self.assertEqual(UserTest.username, "UserTest1")