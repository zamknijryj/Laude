from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, ListView
from .forms import LibrusForm
# from .models import Oceny
from account.models import Profile, Sprawdzian, PracaKlasowa
from .librus import LibrusOceny

from datetime import date, datetime

# DJANGO REST FRAMEWORK
from rest_framework.views import APIView
from rest_framework.response import Response


@login_required
def aktualizacja(request):

    if request.method == 'POST':
        form = LibrusForm(data=request.POST, instance=request.user.profile)
        if form.is_valid():
            username = form.cleaned_data['login']
            password = form.cleaned_data['password']

            lib = LibrusOceny()
            lib.connectToLibrus(username, password)
            oceny = lib.oceny_skon
            imie = lib.full_name
            szczesliwy_numerek = lib.numerek
            numerek_dzien = lib.numerek_dzien
            klasa = lib.klasa
            liczba_spr = len(lib.full_links)

            full_spr = lib.full_spr
            Sprawdzian.objects.filter(user=request.user).delete()
            this_day = date.today()
            for spr in full_spr:
                sprawdzian = Sprawdzian.objects.create(
                    user=request.user,
                    data=spr['Data'],
                    nr_lekcji=spr['Nr lekcji'],
                    nauczyciel=spr['Nauczyciel'],
                    rodzaj=spr['Rodzaj'],
                    przedmiot=spr['Przedmiot'],
                    opis=spr['Opis'],
                    data_dodania=spr['Data dodania']
                )
                # print(sprawdzian.data)
                # print(this_day)
                data_sprawdzianu = datetime.strptime(
                    sprawdzian.data, "%Y-%m-%d").date()
                if data_sprawdzianu > this_day:
                    pass
                else:
                    sprawdzian.delete()

            prace_kl = lib.prace
            PracaKlasowa.objects.filter(user=request.user).delete()
            for praca in prace_kl:
                praca_klasowa = PracaKlasowa.objects.create(
                    user=request.user,
                    data=praca['Data'],
                    nr_lekcji=praca['Nr lekcji'],
                    nauczyciel=praca['Nauczyciel'],
                    rodzaj=praca['Rodzaj'],
                    przedmiot=praca['Przedmiot'],
                    opis=praca['Opis'],
                    data_dodania=praca['Data dodania']
                )
                # print(praca_klasowa.data)
                data_pracy = datetime.strptime(
                    praca_klasowa.data, "%Y-%m-%d").date()
                if data_pracy > this_day:
                    pass
                else:
                    praca_klasowa.delete()

            oceny_display = ', '.join(oceny)
            srednia = lib.sredniaArytmetyczna(lib.oceny2)
            srednia = round(srednia, 2)

            post = form.save(commit=False)
            post.user = request.user
            post.imie = imie
            post.klasa = klasa
            post.oceny = oceny_display
            post.srednia = srednia
            post.szczesliwy_numerek = szczesliwy_numerek
            post.data_numerka = numerek_dzien
            post.liczba_spr = liczba_spr
            post.save()
            messages.success(
                request, 'Dane zostały zaktualizowane, dziękujemy!')
            context = {'form': form, }
            return redirect('home')
    else:
        form = LibrusForm(instance=request.user.profile)
    context = {'form': form}
    return render(request, 'librus/aktualizacja.html', context)


@method_decorator(login_required, name='dispatch')
class LibrusMain(TemplateView):
    template_name = 'librus/librus.html'

    def get_context_data(self, **kwargs):
        context = super(LibrusMain, self).get_context_data(**kwargs)
        context['section'] = 'home'
        return context


@method_decorator(login_required, name='dispatch')
class LibrusSprawdziany(ListView):
    template_name = 'librus/sprawdziany.html'
    model = Sprawdzian

    def get_context_data(self, **kwargs):
        context = super(LibrusSprawdziany, self).get_context_data(**kwargs)
        context['liczba_spr'] = Sprawdzian.objects.filter(
            user=self.request.user).count()
        this_day = date.today()
        first_test = Sprawdzian.objects.first().data

        context['do_testu'] = first_test - this_day
        context['section'] = 'sprawdziany'
        context['prace_list'] = PracaKlasowa.objects.filter(
            user=self.request.user)
        return context

    def get_queryset(self):
        object_list = Sprawdzian.objects.filter(user=self.request.user)

        return object_list


@method_decorator(login_required, name='dispatch')
class LibrusPraceKlasowe(ListView):
    template_name = 'librus/prace_klasowe.html'
    model = PracaKlasowa


class ChartData(APIView):
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


def custom_404(request):
    return HttpResponse('WITAM')


class Custom500Error(TemplateView):
    template_name = 'error/500.html'


def custom_500(request):
    return render(request, '500.html')
