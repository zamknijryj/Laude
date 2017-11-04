from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from librus.librus import LibrusOceny
from librus.models import Oceny
from account.models import (
    Sprawdzian,
    PracaKlasowa,
    Profile
)
from django.contrib.auth.models import User
from django.db.models import Q

class UserLoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=False, allow_blank=True)
    class Meta:
        model = User
        fields = [
            'username',
            'password'
        ]

    def validate(self, data):
        user_obj = None
        username = data.get("username", None)
        password = data["password"]
        if not username:
            raise ValidationError("Musisz podac nazwe uzytkownika.")

        user = User.objects.filter(
            Q(username=username)
        ).distinct()

        if user.exists() and user.count() == 1:
            user_obj = user.first()
        else:
            raise ValidationError("Zła nazwa użytkownika.")

        if user_obj:
            if not user_obj.check_password(password):
                raise ValidationError("Złe dane")

        return data




class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username'
        ]


class AktualizacjaSerializer(serializers.ModelSerializer):
    # username = serializers.CharField(required=True)
    # password = serializers.CharField(required=True)

    class Meta:
        model = Profile
        fields = [
            'login',
            'passwd'
        ]


class UserAPISerializer(serializers.ModelSerializer):
    user = UserDetailSerializer()

    class Meta:
        model = Profile
        fields = [
            'user',
            'imie',
            'klasa',
            'oceny',
            'srednia',
            'data_numerka',
            'szczesliwy_numerek'
        ]


class SprawdzianListSerializer(serializers.ModelSerializer):
    user = UserDetailSerializer()

    class Meta:
        model = Sprawdzian
        fields = [
            'user',
            'data',
            'nauczyciel',
            'rodzaj',
            'przedmiot',
            'opis'
        ]


class PracaKlasowaListSerializer(serializers.ModelSerializer):
    user = UserDetailSerializer()

    class Meta:
        model = PracaKlasowa
        fields = [
            'user',
            'data',
            'nauczyciel',
            'rodzaj',
            'przedmiot',
            'opis'
        ]
