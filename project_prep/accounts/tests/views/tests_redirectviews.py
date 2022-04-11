from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from project_prep.main.models import Garment, GarmentPhoto, OwnedGarment
from project_prep.accounts.models import Profile


UserModel = get_user_model()

class ProfileDetailsViewTests(TestCase):

    VALID_USER_CREDENTIALS = {'email': 'test_testov@abv.bg', 'password': '12345qwe'}
    VALID_PROFILE_DATA = {'first_name': 'Test', 'last_name': 'Testov', 'permission': 'True',}


    def __create_valid_user_and_profile(self):
        user = UserModel.objects.create_user(**self.VALID_USER_CREDENTIALS)
        profile = Profile.objects.create(**self.VALID_PROFILE_DATA, user=user)
        return (user, profile)

    def test_redirect_after_successful_register(self):
        user, profile = self.__create_valid_user_and_profile()
        response = self.client.get(reverse('index'))

    def test_redirect_after_successful_login(self):
        user, profile = self.__create_valid_user_and_profile()
        response = self.client.get(reverse('dashboard'))