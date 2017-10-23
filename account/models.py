from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.utils import timezone


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    imie = models.CharField(max_length=150, default='')
    klasa = models.CharField(max_length=20, default='')
    oceny = models.CharField(max_length=150, default='')
    srednia = models.CharField(max_length=5, default='')
    szczesliwy_numerek = models.CharField(max_length=3, default='')
    data_numerka = models.CharField(max_length=150, default='')
    liczba_spr = models.CharField(max_length=20, default='')
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username


class Sprawdzian(models.Model):
    user = models.ForeignKey(User)
    data = models.DateField(null=True)
    nr_lekcji = models.CharField(max_length=30)
    nauczyciel = models.CharField(max_length=30)
    rodzaj = models.CharField(max_length=30)
    przedmiot = models.CharField(max_length=30)
    opis = models.CharField(max_length=100)
    data_dodania = models.CharField(max_length=30)

    class Meta:
        ordering = ['data']

    def __str__(self):
        return "{} - {} - {}".format(self.user, self.rodzaj, self.przedmiot)


class PracaKlasowa(models.Model):
    user = models.ForeignKey(User)
    data = models.DateField(null=True)
    nr_lekcji = models.CharField(max_length=30)
    nauczyciel = models.CharField(max_length=30)
    rodzaj = models.CharField(max_length=30)
    przedmiot = models.CharField(max_length=30, default='')
    opis = models.CharField(max_length=100)
    data_dodania = models.CharField(max_length=30)

    class Meta:
        ordering = ['data']

    def __str__(self):
        return "{} - {}".format(self.user, self.rodzaj)
