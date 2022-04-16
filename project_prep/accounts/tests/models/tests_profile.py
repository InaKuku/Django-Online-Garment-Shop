from django.contrib.auth import get_user_model
from django.test import TestCase

from project_prep.accounts.models import Profile, AppUser


UserModel = get_user_model()

class UserTests(TestCase):

    VALID_USER_DATA = {
        'email': 'test123@abv.bg',
        'password': '123qwe',
    }

    user = AppUser(**VALID_USER_DATA)
    user.full_clean()



    def test_user_create__expect_sucess(self):
        self.user.save()
        self.assertEqual('test123@abv.bg', self.user.email)


    def test_profile_create__expect_success(self):
        self.user.save()
        VALID_PROFILE_DATA = {
            'first_name': 'Test',
            'last_name': 'Testov',
            'user': self.user,
        }
        profile = Profile(**VALID_PROFILE_DATA)
        profile.full_clean()
        profile.save()
        self.assertEqual('Test Testov', profile.__str__())
        self.assertEqual('test123@abv.bg', profile.user.email)



