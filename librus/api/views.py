from django.contrib import auth
from django.contrib.auth import authenticate, login
from rest_framework import generics, views
from rest_framework.response import Response

from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from .serializers import (
    SprawdzianListSerializer,
    PracaKlasowaListSerializer,
    UserAPISerializer,
    AktualizacjaSerializer,
    UserLoginSerializer,
    UserCreateSerializer
)
from account.models import (
    Sprawdzian,
    PracaKlasowa,
    Profile,
)

from django.contrib.auth.models import User


class SprawdzianAPIData(generics.ListAPIView):
    serializer_class = SprawdzianListSerializer

    def get_queryset(self):
        current_user = self.request.user
        return Sprawdzian.objects.filter(user=current_user)


class PraceKlasoweAPIData(generics.ListAPIView):
    serializer_class = PracaKlasowaListSerializer

    def get_queryset(self):
        current_user = self.request.user
        return PracaKlasowa.objects.filter(user=current_user)


class UserAPIData(generics.ListAPIView):
    serializer_class = UserAPISerializer

    def get_queryset(self):
        current_user = self.request.user
        return Profile.objects.filter(user=current_user)


class AktualizacjaAPI(generics.ListCreateAPIView):
    serializer_class = AktualizacjaSerializer

    def get_queryset(self):
        return Profile.objects.filter(user=self.request.user)


class UserLoginAPI(views.APIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)

    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        data = request.data  # request.POST
        serializer = UserLoginSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            new_data = serializer.data
            user = authenticate(username=new_data['username'], password=new_data['password'])
            login(request, user)
            return Response(new_data, status=HTTP_200_OK)
        new_data = {
            'xd': 10
        }
        return Response(new_data)


class UserCreateAPI(generics.CreateAPIView):
    serializer_class = UserCreateSerializer
    queryset = User.objects.all()

    def perform_create(self, serializer):
        instance = serializer.save()
        instance.set_password(instance.password)
        instance.save()
        info = 'Zaktualizuj dane, aby zobaczyć wynik.'
        Profile.objects.create(user=instance,
                               imie=info,
                               oceny=info,
                               srednia=info,
                               data_numerka=info)


class ChartData(views.APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        current_user = auth.get_user(request)  # get current user
        oceny = current_user.profile.oceny
        labels = ['0', "1", "2", "3", "4", "5", "6"]
        zero = oceny.count('0')
        jeden = oceny.count('1')
        dwa = oceny.count('2')
        trzy = oceny.count('3')
        cztery = oceny.count('4')
        piec = oceny.count('5')
        szesc = oceny.count('6')
        oceny_data = [zero, jeden, dwa, trzy, cztery, piec, szesc]
        data = {
            'labels': labels,
            'default': oceny_data,
            'max': max(oceny_data) + 1
        }
        return Response(data)
