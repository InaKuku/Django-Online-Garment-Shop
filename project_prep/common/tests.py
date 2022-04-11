from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase

from project_prep.accounts.models import Profile, AppUser
from project_prep.common.validators import MaxFileSizeInMbValidator

UserModel = get_user_model()

class only_letters_validatorTests(TestCase):

    VALID_USER_DATA = {
        'email': 'test123@abv.bg',
        'password': '123qwe',
    }

    user = AppUser(**VALID_USER_DATA)
    user.full_clean()


#FIRST_NAME VALIDATION
    def test_profile_create__when_first_name_contains_only_letters__expect_sucess(self):
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
        self.assertIsNotNone(profile.pk)
        self.assertEqual('Test', self.user.profile.first_name)


    def test_profile_create_when_first_name_contains_a_digit__expect_to_fail(self):
        self.user.save()
        VALID_PROFILE_DATA = {
            'first_name': 'Test1',
            'last_name': 'Testov',
            'permission': 'True',
            'user': self.user,
        }
        profile = Profile(**VALID_PROFILE_DATA)
        with self.assertRaises(ValidationError) as context:
            profile.full_clean()
            profile.save()
        self.assertIsNotNone(context.exception)


    def test_profile_create_when_first_name_contains_a_dollar_sign__expect_to_fail(self):
        self.user.save()
        VALID_PROFILE_DATA = {
            'first_name': '$Test',
            'last_name': 'Testov',
            'permission': 'True',
            'user': self.user,
        }
        profile = Profile(**VALID_PROFILE_DATA)
        with self.assertRaises(ValidationError) as context:
            profile.full_clean()
            profile.save()
        self.assertIsNotNone(context.exception)


    def test_profile_create_when_first_name_contains_a_space__expect_to_fail(self):
        self.user.save()
        VALID_PROFILE_DATA = {
            'first_name': ' Test',
            'last_name': 'Testov',
            'permission': 'True',
            'user': self.user,
        }
        profile = Profile(**VALID_PROFILE_DATA)
        with self.assertRaises(ValidationError) as context:
            profile.full_clean()
            profile.save()
        self.assertIsNotNone(context.exception)



#LAST_NAME VALIDATION
    def test_profile_create__when_last_name_contains_only_letters__expect_sucess(self):
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
        self.assertIsNotNone(profile.pk)
        self.assertEqual('Testov', self.user.profile.last_name)


    def test_profile_create_when_last_name_contains_a_digit__expect_to_fail(self):
        self.user.save()
        VALID_PROFILE_DATA = {
            'first_name': 'Test',
            'last_name': 'Testov7',
            'permission': 'True',
            'user': self.user,
        }
        profile = Profile(**VALID_PROFILE_DATA)
        with self.assertRaises(ValidationError) as context:
            profile.full_clean()
            profile.save()
        self.assertIsNotNone(context.exception)


    def test_profile_create_when_last_name_contains_a_dollar_sign__expect_to_fail(self):
        self.user.save()
        VALID_PROFILE_DATA = {
            'first_name': 'Test',
            'last_name': 'Testov$',
            'permission': 'True',
            'user': self.user,
        }
        profile = Profile(**VALID_PROFILE_DATA)
        with self.assertRaises(ValidationError) as context:
            profile.full_clean()
            profile.save()
        self.assertIsNotNone(context.exception)


    def test_profile_create_when_last_name_contains_a_space__expect_to_fail(self):
        self.user.save()
        VALID_PROFILE_DATA = {
            'first_name': 'Test',
            'last_name': 'Te stov',
            'permission': 'True',
            'user': self.user,
        }
        profile = Profile(**VALID_PROFILE_DATA)
        with self.assertRaises(ValidationError) as context:
            profile.full_clean()
            profile.save()
        self.assertIsNotNone(context.exception)


class FakeFile:
    size = 5

class FakeImage:
    file = FakeFile()

class MaxFileSizeInMbValidatorTests(TestCase):

    def test_when_file_is_bigger__expect_to_raise(self):
        validator = MaxFileSizeInMbValidator(0.0000001)
        file = FakeImage()
        with self.assertRaises(ValidationError) as context:
            validator(file)
