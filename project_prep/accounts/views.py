from django.contrib.auth import views as views, login, get_user_model
from django.contrib.auth.views import PasswordChangeView, LogoutView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView, UpdateView

from project_prep.accounts.forms import CreateProfileForm, EditProfileForm, DeleteProfileForm
from project_prep.accounts.models import Profile
from project_prep.common.view_mixins import RedirectToDashboard
from project_prep.main.models import GarmentPhoto, OwnedGarment


class UserLoginView(views.LoginView):
    template_name = 'accounts/login_page.html'
    success_url = reverse_lazy('dashboard')


    def get_success_url(self):
        if self.success_url:
            return self.success_url
        return super().get_success_url()


class UserRegisterView(RedirectToDashboard, CreateView):
    form_class = CreateProfileForm
    template_name = 'accounts/profile_create.html'
    success_url = reverse_lazy('index')

    def form_valid(self, *args, **kwargs):
        result = super().form_valid(*args, **kwargs)
        login(self.request, self.object)
        return result

class ProfileDetailsView(DetailView):
    model = Profile
    template_name = 'accounts/profile_details.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        owned_garments = list(OwnedGarment.objects \
                    .filter(garment_owner_id=self.request.user.id))

        garment_photos = GarmentPhoto.objects \
            .filter(tagged_garments__in=owned_garments) \
            .distinct()

        total_garment_photos_count = len(garment_photos)
        total_likes_count = sum(p.likes for p in garment_photos)

        context.update({
            'total_likes_count': total_likes_count,
            'owned_garments': owned_garments,
            'total_garment_photos_count': total_garment_photos_count,
            'is_owner': self.object.user_id == self.request.user.id,
            'garment_photos': garment_photos
        })
        return context


class EditProfileView(UpdateView):
    model = Profile
    template_name = 'accounts/profile_edit.html'
    fields = ['first_name', 'last_name', ]

    def get_success_url(self):
        return reverse_lazy('profile details',  kwargs={'pk': self.object.pk})

class DeleteProfileView(UpdateView):
    form_class = DeleteProfileForm
    model = Profile
    template_name = 'accounts/profile_delete.html'
    success_url = reverse_lazy('index')

class ChangeUserPasswordView(PasswordChangeView):
    template_name = 'accounts/change_password.html'

class UserLogoutView(LogoutView):
    next_page = reverse_lazy('index')

