from django.contrib.auth.urls import url
from . import views
from .views import (
    ChartData,
    LibrusMain,
    LibrusSprawdziany,
    LibrusPraceKlasowe
)

urlpatterns = [
    url(r'^$', LibrusMain.as_view(), name='home'),
    url(r'^aktualizacja/$', views.aktualizacja, name='aktualizacja'),
    url(r'^sprawdziany/$', LibrusSprawdziany.as_view(), name='terminarz'),
    url(r'^prace-klasowe/$', LibrusPraceKlasowe.as_view(), name='prace-klasowe'),
    url(r'^api/chart/data/$', ChartData.as_view())
]
