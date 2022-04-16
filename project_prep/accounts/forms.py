from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from project_prep.accounts.models import Profile
from project_prep.common.view_mixins import BootstrapFormMixin
from django import forms
from project_prep.main.models import GarmentPhoto, OwnedGarment

UserModel = get_user_model()

class CreateProfileForm(BootstrapFormMixin, UserCreationForm):

    first_name = forms.CharField(
        max_length = Profile.FIRST_NAME_MAX_LENGTH,
    )

    last_name = forms.CharField(
        max_length=Profile.LAST_NAME_MAX_LENGTH,
    )



    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_bootstrap_form_controls()


    def clean(self):
        cleaned_data = super().clean()
        f_name = cleaned_data.get('first_name')
        l_name = cleaned_data.get('last_name')

        for ch in f_name:
            if not ch.isalpha():
                raise ValidationError('First name must contain only letters')
        for ch in l_name:
            if not ch.isalpha():
                raise ValidationError('Last name must contain only letters')


    def save(self, commit=True):
        user = super().save(commit=commit)
        profile = Profile(
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            user=user,
        )
        if commit:
            profile.save()
        return user




    class Meta:
        model = UserModel
        fields = ('email', 'first_name', 'last_name', 'password1', 'password2',)



class EditProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', )


class DeleteProfileForm(forms.ModelForm):
    def save(self, commit = True):
        try:
            user = UserModel.objects.get(pk = self.instance.user_id)
            GarmentPhoto.objects.filter(user=user).delete()
            own_garments = OwnedGarment.objects.filter(garment__ownedgarment__garment_owner_id=user.id)
            own_garments.delete()
            self.instance.delete()
            user.delete()
            return self.instance
        except User.DoesNotExist as exc:
            raise User.DoesNotExist(
                "User doesn't exist in the system. "
                "Create a user first!") from exc

    class Meta:
        model=Profile
        fields=()





