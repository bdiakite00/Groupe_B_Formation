from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.

class GoogleSheet(models.Model):
    lien_google_sheet = models.URLField(max_length=200, verbose_name=_(""))

    def __str__(self):
        return self.lien_google_sheet