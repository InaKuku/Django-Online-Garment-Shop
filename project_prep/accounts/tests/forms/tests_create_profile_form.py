from django.test import TestCase
from django.urls import reverse

from project_prep.accounts.models import AppUser, Profile


class FillInProfileFormTests(TestCase):

        VALID_USER_DATA = {
            'email': 'test123@abv.bg',
            'password': '123qwe',
        }

        user = AppUser(**VALID_USER_DATA)
        user.full_clean()

#it tests register (and login) made together

        def test_profile_create_and_login__expect_success(self):
            self.user.save()
            VALID_PROFILE_DATA = {
                'first_name': 'Test',
                'last_name': 'Testov',
                'permission': 'True',
                'user': self.user,
            }
            profile = Profile(**VALID_PROFILE_DATA)
            profile.full_clean()
            profile.save()
            response = self.client.get(reverse('logout form'))
            self.assertEqual(302, response.status_code)

