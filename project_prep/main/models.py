from django.contrib.auth import get_user_model
from django.db import models
from project_prep.accounts.models import AppUser
from project_prep.common.validators import MaxFileSizeInMbValidator
from cloudinary import models as cloudinary_models

UserModel = get_user_model()

class Garment(models.Model):
    DRESS = 'Dress'
    TROUSERS = 'Trousers'
    SKIRT = 'Skirt'
    SHIRT = 'Shirt'
    COAT = 'Coat'
    CARDIGANS = 'Cardigans'
    OTHER = 'Other'
    TYPES = [(x, x) for x in (DRESS, TROUSERS, SKIRT, SHIRT, COAT, CARDIGANS, OTHER)]

    LINEN = 'linen'
    COTTON = 'Cotton'
    LINNEN_AND_COTTON = 'Linnen/Cotton'
    SILK = 'Silk'
    WOOL = 'Wool'
    FABRICS = [(x, x) for x in (LINEN, COTTON, LINNEN_AND_COTTON, SILK, WOOL)]

    NAME_MAX_LENGTH = 50

    name = models.CharField(
        max_length=NAME_MAX_LENGTH
    )

    number = models.IntegerField(
        unique=True,
    )

    type = models.CharField(
        max_length=max(len(x) for (x, _) in TYPES),
        choices=TYPES,
    )

    materials = models.CharField(
        max_length=max(len(x) for (x, _) in FABRICS),
        choices=FABRICS,
    )

    description = models.TextField(
        null=True,
        blank=True,
    )

    # image = models.ImageField()
    image = cloudinary_models.CloudinaryField('image')

    def __str__(self):
        return f'{self.name} - {self.type}'


class OwnedGarment(models.Model):

    XS = "XS"
    S = "S"
    M = "M"
    L  = "L"
    XL = "XL"
    XXL = "XXL"
    SIZES = [(x, x) for x in (XS, S, M, L, XL, XXL)]

    size = models.CharField(
        max_length=max(len(x) for (x, _) in SIZES),
        choices=SIZES,
    )

    own_name = models.CharField(
        max_length=40,
        null = True,
        blank = True,
    )

    garment = models.ForeignKey(
        Garment,
        on_delete=models.CASCADE,
        null=True,
    )

    garment_owner = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
    )


    def __str__(self):
        return f'{self.own_name} - {self.size}'


class GarmentPhoto(models.Model):

    photo = cloudinary_models.CloudinaryField('image')
    #         (
    #     validators=(
    #         MaxFileSizeInMbValidator(5),
    #     )
    # )



    description = models.TextField(
        null=True,
        blank=True,
    )

    publication_date = models.DateTimeField(
        auto_now_add=True,
    )

    likes = models.IntegerField(
        default=0,
    )

    tagged_garments = models.ManyToManyField(
        OwnedGarment,
    )

    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
    )
