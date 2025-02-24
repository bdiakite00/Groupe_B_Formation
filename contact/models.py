from django.db import models

class Coach(models.Model):
    nom_du_coach = models.CharField(max_length=100)
    description = models.TextField()
    lien_photo = models.URLField()
    lien_site_internet = models.URLField()
    message_publicite = models.TextField()
    email = models.EmailField()

    class Meta:
        app_label = 'contact'
