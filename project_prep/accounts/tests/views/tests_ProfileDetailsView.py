from datetime import date

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from project_prep.main.models import Garment, GarmentPhoto, OwnedGarment
from project_prep.accounts.models import Profile


UserModel = get_user_model()

class ProfileDetailsViewTests(TestCase):

    VALID_USER_CREDENTIALS = {'email': 'test_testov@abv.bg', 'password': '12345qwe'}
    VALID_PROFILE_DATA = {'first_name': 'Test', 'last_name': 'Testov',}
    VALID_GARMENT_DATA = {'name': 'White Dress', 'number': '12837264', 'type': Garment.DRESS, 'materials': Garment.LINEN, 'description': '', 'image': 'some.png'}
    VALID_OWNEDGARMENT_DATA = {'own_name': 'My fav white dress', 'size': OwnedGarment.S}
    VALID_GARMENT_PHOTO = {'photo': 'some_other.png', 'description': '', 'publication_date': date.today(),}

    def __create_valid_user_and_profile(self):
        user = UserModel.objects.create_user(**self.VALID_USER_CREDENTIALS)
        profile = Profile.objects.create(**self.VALID_PROFILE_DATA, user=user)
        return (user, profile)

    def __create_valid_garment_ownedgarment_and_garment_photo(self, user):
        garment = Garment.objects.create(**self.VALID_GARMENT_DATA)
        owned_garment = OwnedGarment.objects.create(**self.VALID_OWNEDGARMENT_DATA, garment=garment, garment_owner=user)
        garment_photo = GarmentPhoto.objects.create(**self.VALID_GARMENT_PHOTO, user=user)
        garment_photo.tagged_garments.add(owned_garment)
        garment_photo.save()
        return (garment, owned_garment, garment_photo)

    def __create_user(self, **credentials):
        return UserModel.objects.create_user(**credentials)

    def test_when_openning_non_existing_profile__expect_404(self):
        response = self.client.get(reverse('profile details', kwargs = {'pk':9328472349320489721}))
        self.assertEqual(404, response.status_code)

    def test_when_openning_existing_profile_not_logged_in__expect_404(self):
        response = self.client.get(reverse('profile details', kwargs = {'pk':7}))
        self.assertEqual(404, response.status_code)

    def test_when_openning_existing_profile_logged_in_with_another_profile__expect_404(self):
        user, profile = self.__create_valid_user_and_profile()
        valid_user2_credentials = {'email': 'test_testov_1@abv.bg', 'password': '12345qwe'}
        user2 = self.__create_user(**valid_user2_credentials)
        self.client.login(**valid_user2_credentials)
        response = self.client.get(reverse('profile details', kwargs={'pk': 7}))
        self.assertEqual(404, response.status_code)


    def test_when_user_is_owner__expect_is_owner_to_be_true(self):
        user, profile = self.__create_valid_user_and_profile()
        self.client.login(**self.VALID_USER_CREDENTIALS)
        response = self.client.get(reverse('profile details', kwargs = {'pk':profile.pk}))
        self.assertTrue(response.context['is_owner'])

    def test_when_user_is_not_owner__expect_is_owner_to_be_false(self):
        user, profile = self.__create_valid_user_and_profile()
        valid_user2_credentials = {'email': 'test_testov_1@abv.bg', 'password': '12345qwe'}
        user2 = self.__create_user(**valid_user2_credentials)
        self.client.login(**valid_user2_credentials)
        response = self.client.get(reverse('profile details', kwargs = {'pk':profile.pk}))
        self.assertFalse(response.context['is_owner'])

    def test_when_no_photos_likes__expect_total_likes_to_be_zero(self):
        user, profile = self.__create_valid_user_and_profile()
        garment, owned_garment, photo = self.__create_valid_garment_ownedgarment_and_garment_photo(user)
        self.client.login(**self.VALID_USER_CREDENTIALS)
        response = self.client.get(reverse('profile details', kwargs={'pk': profile.pk}))
        self.assertEqual(0, response.context['total_likes_count'])

    def test_when_3_photos_likes__expect_total_likes_to_be_3(self):
        user, profile = self.__create_valid_user_and_profile()
        garment, owned_garment, garment_photo = self.__create_valid_garment_ownedgarment_and_garment_photo(user)
        garment_photo.likes = 3
        garment_photo.save()
        self.client.login(**self.VALID_USER_CREDENTIALS)
        response = self.client.get(reverse('profile details', kwargs={'pk': profile.pk}))
        self.assertEqual( 3, response.context['total_likes_count'])

    def test_when_no_photos_0_photos_count(self):
        user, profile = self.__create_valid_user_and_profile()
        self.client.login(**self.VALID_USER_CREDENTIALS)
        response = self.client.get(reverse('profile details', kwargs={'pk': profile.pk}))
        self.assertEqual(0, response.context['total_garment_photos_count'])

    def test_when_user_has_owned_garments__expect_to_return_only_users_garments(self):
        user, profile = self.__create_valid_user_and_profile()
        garment, owned_garment, garment_photo = self.__create_valid_garment_ownedgarment_and_garment_photo(user)

        credentials = {
            'email': 'test_testov2@abv.bg',
            'password': '12345qwe'
        }
        owned_garment_2_data = {'own_name': 'What a beautiful dress', 'size': OwnedGarment.M}

        user2 = UserModel.objects.create_user(**credentials)
        owned_garment_2 = OwnedGarment.objects.create(**owned_garment_2_data, garment=garment, garment_owner = user2)

        self.client.login(**self.VALID_USER_CREDENTIALS)
        response = self.client.get(reverse('profile details', kwargs={'pk': profile.pk}))
        self.assertEqual([owned_garment], response.context['owned_garments'])

    def test_when_user_has_no_pets__expect_pets_to_be_empty_list(self):
        user, profile = self.__create_valid_user_and_profile()
        self.client.login(**self.VALID_USER_CREDENTIALS)
        response = self.client.get(reverse('profile details', kwargs={'pk': profile.pk}))
        self.assertEqual([], response.context['owned_garments'])

    def test_when_user_has_no_pets_likes_and_photos__expect_pets_to_be_empty_list_counts_to_be_zero(self):
        user, profile = self.__create_valid_user_and_profile()
        self.client.login(**self.VALID_USER_CREDENTIALS)
        response = self.client.get(reverse('profile details', kwargs={'pk': profile.pk}))
        self.assertEqual([], response.context['owned_garments'])
        self.assertEqual(0, response.context['total_garment_photos_count'])
        self.assertEqual(0, response.context['total_likes_count'])












