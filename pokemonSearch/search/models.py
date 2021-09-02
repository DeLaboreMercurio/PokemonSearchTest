from django.conf import settings
from django.db import models


class Pokemon(models.Model):
    name = models.CharField(
        max_length=100
    )  # I highly doubt that pokemon names even exceed 50 chars, but one can always be prepared for the unexpected.
    url = models.CharField(max_length=500)  # Unnecesarily long, most likely.
    image = models.ImageField(upload_to="img_pokemon")

    def __str__(self):
        return self.name
