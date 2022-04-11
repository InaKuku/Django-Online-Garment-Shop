from django import forms
from project_prep.common.view_mixins import BootstrapFormMixin
from project_prep.main.models import Garment, OwnedGarment, GarmentPhoto


# class CreateGarmentForm(BootstrapFormMixin, forms.ModelForm):
#
#     class Meta:
#         model = Garment
#         fields = ('name', 'type', 'materials', 'description', 'image',)
#         widgets={
#             'name': forms.TextInput(
#                 attrs={
#                     'class': 'form-control',
#                     'placeholder': 'Enter garment name',
#                 }
#             ),
#             'type': forms.Select(
#                 choices=Garment.TYPES,
#                 attrs={
#                     'class': 'form-control',
#                 }
#             ),
#             'materials': forms.Select(
#                 choices=Garment.FABRICS,
#                 attrs={
#                     'class': 'form-control',
#                 }
#             ),
#             'description': forms.Textarea(
#                 attrs={
#                     'class': 'form-control',
#                     'placeholder': 'Enter description',
#                 }
#             ),
#             'image': forms.ClearableFileInput(
#                 attrs={
#                     'class': 'form-control',
#                     'placeholder': 'Enter path to image',
#                 }
#             ),
#         }
#
#
# class EditGarmentForm(forms.ModelForm):
#     class Meta:
#         model = Garment
#         fields = ('name', 'type', 'materials', 'description', 'image',)
#         widgets={
#             'name': forms.TextInput(
#                 attrs={
#                     'class': 'form-control',
#                     'placeholder': 'Enter garment name',
#                 }
#             ),
#             'type': forms.Select(
#                 choices=Garment.TYPES,
#                 attrs={
#                     'class': 'form-control',
#                 }
#             ),
#             'materials': forms.Select(
#                 choices=Garment.FABRICS,
#                 attrs={
#                     'class': 'form-control',
#                 }
#             ),
#             'description': forms.Textarea(
#                 attrs={
#                     'class': 'form-control',
#                     'placeholder': 'Enter description',
#                 }
#             ),
#             'image': forms.ClearableFileInput(
#                 attrs={
#                     'class': 'form-control',
#                     'placeholder': 'Enter path to image',
#                 }
#             ),
#         }
#
# class DeleteGarmentForm(forms.ModelForm):
#     def save(self, commit = True):
#         self.instance.delete()
#         return self.instance
#
#     class Meta:
#         model=Garment
#         fields = ('name', 'type', 'materials', 'description', 'image',)
#         widgets = {
#             'name': forms.TextInput(
#                 attrs={
#                     'class': 'form-control',
#                     'disabled': 'disabled'
#                 }
#             ),
#             'type': forms.Select(
#                 choices=Garment.TYPES,
#                 attrs={
#                     'class': 'form-control',
#                     'disabled': 'disabled'
#                 }
#             ),
#             'materials': forms.Select(
#                 choices=Garment.FABRICS,
#                 attrs={
#                     'class': 'form-control',
#                     'disabled': 'disabled'
#                 }
#             ),
#             'description': forms.Textarea(
#                 attrs={
#                     'class': 'form-control',
#                     'disabled': 'disabled'
#                 }
#             ),
#             'image': forms.ClearableFileInput(
#                 attrs={
#                     'class': 'form-control',
#                     'disabled': 'disabled',
#                 }
#             ),
#         }
#
#     def __init__(self, *args, **kwargs):
#         super(DeleteGarmentForm, self).__init__(*args, **kwargs)
#         for field in self.fields:
#             self.fields[field].required = False
#

class OwnedGarmentForm(forms.ModelForm):

    class Meta:
        model = OwnedGarment
        fields = ('size', 'own_name')
        widgets = {
            'size': forms.Select(
                choices=OwnedGarment.SIZES,
                attrs={
                    'class': 'form-control',
                }
            ),
            'own_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                }
            ),
        }
        labels={
            'own_name': 'Same something for your new garment',
        }




class OwnedGarmentEditForm(forms.ModelForm):

    class Meta:
        model = OwnedGarment
        fields = ('size',)


class CreateMyGarmentPhotoForm(BootstrapFormMixin, forms.ModelForm):

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(CreateMyGarmentPhotoForm, self).__init__(*args, **kwargs)
        self.fields['tagged_garments'].queryset = OwnedGarment.objects.filter(garment_owner=user)
        self._init_bootstrap_form_controls()


        def save(self, commit=True):
            garment_photo = super().save(commit=False)
            if commit:
                garment_photo.save()
            return garment_photo




    class Meta:
        model = GarmentPhoto
        fields = ('photo', 'tagged_garments')
        labels = {
            'tagged_garments': 'Which garment is on the photo?',
        }



class EditMyGarmentPhotoForm(BootstrapFormMixin, forms.ModelForm):

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(EditMyGarmentPhotoForm, self).__init__(*args, **kwargs)
        self.fields['tagged_garments'].queryset = OwnedGarment.objects.filter(garment_owner=user)
        self._init_bootstrap_form_controls()



    class Meta:
        model = GarmentPhoto
        fields = ('tagged_garments',)