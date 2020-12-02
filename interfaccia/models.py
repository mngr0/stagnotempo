from django.db import models

# Create your models here.
class Configurazione(models.Model):
    indice = models.IntegerField(primary_key = True)
    durata = models.IntegerField()