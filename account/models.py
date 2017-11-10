from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.utils import timezone


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    imie = models.CharField(max_length=150)
    klasa = models.CharField(max_length=20)
    num_w_dzienniku = models.CharField(max_length=10)
    oceny = models.CharField(max_length=150)
    srednia = models.CharField(max_length=5)
    szczesliwy_numerek = models.PositiveIntegerField(null=True)
    data_numerka = models.CharField(max_length=150)
    updated = models.DateTimeField(auto_now=True)

    # TEST
    login = models.CharField(max_length=50)
    passwd = models.CharField(max_length=70)

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
        return "Sprawdzian"


class PracaKlasowa(models.Model):
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
        return "{} - {}".format(self.user, self.rodzaj)

class SprawdzianZaliczony(models.Model):

    KAT = (
        ('sprawdzian', 'sprawdzian'),
        ('kartkówka', 'kartkówka'),
        ('odpowiedź ustana', 'odpowiedź ustana')
    )

    PRZED = (
        ('default', '------------------------------------'),
        ('Biologia', 'Biologia'),
        ('Chemia', 'Chemia'),
        ('Edukacja dla bezpieczeństwa', 'EDB'),
        ('Fizyka', 'Fizyka'),
        ('Historia', 'Historia'),
        ('Informatyka', 'Informatyka'),
        ('Język angielski', 'Język angielski'),
        ('Język niemiecki', 'Język niemiecki'),
        ('Język francuski', 'Język francuski'),
        ('Język polski', 'Język polski'),
        ('Matematyka', 'Matematyka'),
        ('Podstawy przedsiębiorczości', 'Podstawy przedsiębiorczości'),
        ('Religia', 'Religia'),
        ('Wiedza o kulturze', 'WOK'),
        ('Wiedza o społeczeństwie', 'WOS'),
        ('Wychowanie fizyczne', 'WF')
    )

    user = models.ForeignKey(User)
    ocena = models.CharField(max_length=5)
    kategoria = models.CharField(max_length=50, choices=KAT, default='sprawdzian')
    data = models.CharField(max_length=30)
    nauczyciel = models.CharField(max_length=60)
    przedmiot = models.CharField(max_length=60, choices=PRZED, default='default')
    komentarz = models.CharField(max_length=140)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return "{} - {} - {} - Zaliczony".format(self.user, self.kategoria, self.przedmiot)
