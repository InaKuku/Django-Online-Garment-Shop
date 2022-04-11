from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect

from django.urls import reverse_lazy
from django.views import generic as views

from project_prep.accounts.models import AppUser
from project_prep.main.forms import EditMyGarmentPhotoForm, CreateMyGarmentPhotoForm, OwnedGarmentForm
from project_prep.main.models import GarmentPhoto, Garment, OwnedGarment


class HomeView(views.TemplateView):
    template_name = 'main/home_page.html'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['hide_additional_nav_items'] = True
    #     return context

class DashboardView(views.ListView):
    model = GarmentPhoto
    template_name = 'main/dashboard.html'
    context_object_name = 'garments_photos'

class ShopView(views.ListView):
    model = Garment
    template_name = 'main/shop.html'
    context_object_name = 'garments'


def CreateMyGarment(request, pk):

    garment = Garment.objects.get(pk=pk)

    if request.method == "POST":
        owned_garment_form = OwnedGarmentForm(request.POST)
        if owned_garment_form.is_valid():
            owned_garment_form.instance.garment_owner = request.user
            owned_garment_form.instance.garment = garment
            owned_garment_form.save()
            return redirect('shop')
    else:
        owned_garment_form = OwnedGarmentForm()
    context = {
        'owned_garment_form': owned_garment_form,
        'garment': garment,
    }
    return render(request, 'main/garment_details.html', context)



class GarmentPhotoDetailsView(LoginRequiredMixin, views.DetailView):
    model = GarmentPhoto
    template_name = 'main/photo_details.html'
    context_object_name = 'garment_photo'


    def get_queryset(self):
        return super()\
            .get_queryset()\
            .prefetch_related('tagged_garments')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_owner'] = self.object.user == self.request.user
        return context

    # def dispatch(self, request, *args, **kwargs):
    #     response = super().dispatch(request, *args, **kwargs)
    #     viewed_garment_photos = request.session.get('last_viewed_garment_photo_ids', [])
    #     viewed_garment_photos.insert(0, self.kwargs['pk'])
    #     request.session['last_viewed_garment_photo_ids'] = viewed_garment_photos[:4]
    #     return response

def like_garment_photo(request, pk):
    garment_photo = GarmentPhoto.objects.get(pk=pk)
    garment_photo.likes += 1
    garment_photo.save()
    return redirect('garment photo details', pk)


# class CreateGarmentView(views.CreateView):
#     template_name = 'main/garment_create.html'
#     form_class = CreateGarmentForm
#     success_url = reverse_lazy('dashboard')
#
#     def get_form_kwargs(self):
#         kwargs = super().get_form_kwargs()
#         kwargs['user'] = self.request.user
#         return kwargs
#
# class EditGarmentView(views.UpdateView):
#     template_name = 'main/pet_edit.html'
#     form_class = EditGarmentForm
#
# class DeleteGarmentView(views.DeleteView):
#     template_name = 'main/pet_delete.html'
#     form_class = DeleteGarmentForm



def CreateMyGarmentPhoto(request):
    own_garments = OwnedGarment.objects.filter(garment_owner=request.user.id)
    if request.method == "POST":
        photo_form = CreateMyGarmentPhotoForm(request.POST, request.FILES, user=request.user)
        if photo_form.is_valid():
            photo_form.instance.user = request.user
            photo_form.save()
            tagged_garments = request.POST.getlist('tagged_garments')
            photo_form.instance.tagged_garments.add(*tagged_garments)
            photo_form.save()
            return redirect('dashboard')
    else:
        photo_form = CreateMyGarmentPhotoForm(request.FILES, user=request.user)

    context = {
        'photo_form': photo_form,
        'own_garments': own_garments
    }
    return render(request, 'main/photo_create.html', context)



def EditMyGarmentPhotoView(request, pk):
    photo_for_edit = GarmentPhoto.objects.get(pk=pk)
    own_garments = OwnedGarment.objects.filter(garment_owner=request.user.id)
    if request.method == "POST":
        photo_form = EditMyGarmentPhotoForm(request.POST, request.FILES, instance=photo_for_edit, user=request.user)
        if photo_form.is_valid():
            photo_form.save()
            for tagged_garment in photo_form.instance.tagged_garments.all():
                photo_form.instance.tagged_garments.remove(tagged_garment)
            tagged_garments = request.POST.getlist('tagged_garments')
            photo_form.instance.tagged_garments.add(*tagged_garments)
            photo_form.save()
            return redirect('garment photo details', pk=pk)
    else:
        photo_form = EditMyGarmentPhotoForm(request.FILES, instance=photo_for_edit, user=request.user)

    context = {
        'photo_form': photo_form,
        'own_garments': own_garments,
        'photo_for_edit': photo_for_edit
    }
    return render(request, 'main/photo_edit.html', context)

class DeleteMyGarmentPhotoView(views.DeleteView):
    model = GarmentPhoto
    template_name = 'main/delete_photo.html'
    success_url = reverse_lazy('dashboard')




