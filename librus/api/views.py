from django.contrib import auth
from rest_framework import generics, views
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from .serializers import (
    SprawdzianListSerializer,
    PracaKlasowaListSerializer,
    UserAPISerializer,
    AktualizacjaSerializer,
    UserLoginSerializer
)
from account.models import (
    Sprawdzian,
    PracaKlasowa,
    Profile
)


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
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        data = request.data # request.POST
        serializer = UserLoginSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            new_data = serializer.data
            return Response(new_data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)



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
