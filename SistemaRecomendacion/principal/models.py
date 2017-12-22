from django.db import models
from django.core.validators import URLValidator

# Create your models here.

class Usuario(models.Model):
    idUsuario = models.IntegerField(unique=True)
    edad = models.IntegerField(min_value = 0, max_value=200)
    localizacion = models.CharField()

    def __unicode__(self):
        return self.idUsuario

class Libro(models.Model):
    isbn = models.CharField()
    titulo = models.CharField()
    autor = models.CharField()
    añoPublicacion = models.IntegerField
    editor = models.CharField()
    url = models.CharField()

    def __unicode__(self):
        return self.isbn

class Puntuacion(models.Model):
    idUsuario = models.ForeignKey(Usuario.idUsuario)
    isbn = models.ForeignKey(Libro.isbn)
    puntuacion = models.IntegerField(min_value=1, max_value=10)

    def __unicode__(self):
        return self.idUsuario + self.isbn