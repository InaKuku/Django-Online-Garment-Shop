from django.urls import path, reverse_lazy
from django.views.generic import RedirectView

from project_prep.accounts.views import UserLoginView, ProfileDetailsView, UserRegisterView, ChangeUserPasswordView, \
    UserLogoutView, EditProfileView, DeleteProfileView

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login user'),
    path('profile/<int:pk>/', ProfileDetailsView.as_view(), name='profile details'),
    path('profile/create/', UserRegisterView.as_view(), name='create profile'),
    path('edit-password/', ChangeUserPasswordView.as_view(), name='change password'),
    path('password_change_done/', RedirectView.as_view(url=reverse_lazy('dashboard')), name='password_change_done'),
    path('logout/', UserLogoutView.as_view(), name = 'logout form'),
    path('edit/profile/<int:pk>/', EditProfileView.as_view(), name='edit profile'),
    path('profile/delete/<int:pk>/', DeleteProfileView.as_view(), name='delete profile'),
    # path('test/', test, name='test'),

]