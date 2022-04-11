#It should be registered after session middleware
from project_prep.main.models import GarmentPhoto


# def last_viewed_garment_photos_middleware(get_response):
#     def middleware(request):
#         garments_photo_ids = request.session.get('last_viewed_pet_photo_ids', [])
#         photos = GarmentPhoto.objects.filter(id__in=garments_photo_ids)
#         request.last_viewed_garment_photos = photos
#         return get_response(request)
#
#     return middleware

