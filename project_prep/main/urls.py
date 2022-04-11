from django.urls import path

from project_prep.main.views import \
    like_garment_photo, \
    HomeView, DashboardView,\
    GarmentPhotoDetailsView, DeleteMyGarmentPhotoView, ShopView, \
    CreateMyGarment, CreateMyGarmentPhoto, EditMyGarmentPhotoView

urlpatterns = [
    path('', HomeView.as_view(), name='index'),
    path('shop/', ShopView.as_view(), name='shop'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('garment/details/<int:pk>/', CreateMyGarment, name='garment details'),
    path('photo/details/<int:pk>/', GarmentPhotoDetailsView.as_view(), name='garment photo details'),
    path('photo/add/', CreateMyGarmentPhoto, name='create garment photo'),
    path('photo/edit/<int:pk>', EditMyGarmentPhotoView, name='edit garment photo'),
    path('photo/delete/<int:pk>', DeleteMyGarmentPhotoView.as_view(), name='delete garment photo'),
    path('photo/like/<int:pk>/', like_garment_photo, name='like garment photo'),

]