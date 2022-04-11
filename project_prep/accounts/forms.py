from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
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

    permission = forms.BooleanField(
        initial=True,
        required=False,
        label="Do you want your collection of photos to be visible to the other Sunny shop users?"
    )


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_bootstrap_form_controls()

    def save(self, commit=True):
        user = super().save(commit=commit)
        profile = Profile(
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            permission=self.cleaned_data['permission'],
            user=user,
        )
        if commit:
            profile.save()
        return user

    class Meta:
        model = UserModel
        fields = ('email', 'first_name', 'last_name', 'permission', 'password1', 'password2',)



class EditProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'permission',)


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





