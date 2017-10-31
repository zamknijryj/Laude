from __future__ import print_function
import argparse
import mechanicalsoup
from getpass import getpass
import re
import datetime


class LibrusOceny():
    def __init__(self):
        self.browser = browser = mechanicalsoup.StatefulBrowser(
            soup_config={'features': 'lxml'},
            #    raise_on_404=True,
            #    user_agent='MyBot/0.1: mysite.example.com/bot_info',
        )

        self.oceny = []
        self.oceny2 = []
        self.oceny_skon = []
        self.numerek = 0
        self.numerek_dzien = ''
        self.klasa = ''
        self.full_links = []
        self.full_spr = []
        self.prace = []
        self.wiadomosciText = []

    def connectToLibrus(self, username, password):

        self.browser.open("https://synergia.librus.pl")
        self.browser.follow_link("loguj")
        self.browser.select_form('.loginForm form')
        self.browser["login"] = username
        self.browser["passwd"] = password
        resp = self.browser.submit_selected()
        # check that we are connected
        page = self.browser.get_current_page()
        # print(page.title.text)
        self.getOceny()

    def getOceny(self):
        page3 = self.browser.open(
            "https://synergia.librus.pl/przegladaj_oceny/uczen")
        p = self.browser.get_current_page()
        title = p.find('h2', class_='inside')
        # print(title.text)
        x = p.findAll('span', class_='grade-box')
        # print(title.text)
        for t in x:
            self.oceny.append(t.text)

        self.replaceGrades()
        self.konfiguracjaOcen(self.oceny2)
        self.sredniaArytmetyczna(self.oceny2)
        self.ocenkiDoWyswietlenia()
        self.getLuckyNumber()
        self.sprawdziany()
        self.prace_klasowe()
        self.wiadomosci()

    def getUserName(self):
        info_page = self.browser.open('https://synergia.librus.pl/informacja')
        response = self.browser.get_current_page()
        table = response.find('table', class_='decorated big center form').find('tbody')
        line_imie = table.find('tr', class_='line1').find('td')

        return line_imie.text

    def numerUcznia(self):
        info_page = self.browser.open('https://synergia.librus.pl/informacja')
        response = self.browser.get_current_page()
        table = response.find('table', class_='decorated big center form').find('tbody')

        all_lines1 = table.findAll('tr', class_='line1')
        numrek_line = all_lines1[1].find('td')
        numerek = ''.join(numrek_line.text.split())

        return numerek

    def klasaUcznia(self):
        page4 = self.browser.open(
            "https://synergia.librus.pl/informacja")
        p = self.browser.get_current_page()
        klasa = p.find('tr', class_='line0').find('td').text
        klasa = ' '.join((klasa.split()))

        return klasa

    def ocenkiDoWyswietlenia(self):
        for ocena in self.oceny:
            ocena = ocena.replace('\n', '')
            self.oceny_skon.append(ocena)
        del self.oceny_skon[0]
        self.oceny_skon.remove('')
        self.oceny_skon = list(
            filter(lambda a: a != 'np' and a != 'T', self.oceny_skon))

    def replaceGrades(self):
        for ocena in self.oceny:
            ocena = ocena.replace('\n', '')
            ocena = ocena.replace('6-', '5.75')
            ocena = ocena.replace('5-', '4.75')
            ocena = ocena.replace('5+', '5.5')
            ocena = ocena.replace('4-', '3.75')
            ocena = ocena.replace('4+', '4.5')
            ocena = ocena.replace('3-', '2.75')
            ocena = ocena.replace('3+', '3.5')
            ocena = ocena.replace('2-', '1.75')
            ocena = ocena.replace('2+', '2.5')
            ocena = ocena.replace('1-', '0.75')
            ocena = ocena.replace('1+', '1.5')
            self.oceny2.append(ocena)

    def getLuckyNumber(self):
        page3 = self.browser.open(
            "https://synergia.librus.pl/uczen_index")
        p = self.browser.get_current_page()
        self.numerek_dzien = p.find('h2', class_='center').text
        self.numerek_dzien = [e for e in self.numerek_dzien.replace(
            '\n', ' ').split(' ') if e != '']
        self.numerek_dzien = ' '.join(self.numerek_dzien)

        self.numerek = p.find(
            "div", class_="szczesliwy-numerek").find("span").text

        try:
            self.numerek = int(self.numerek)
        except:
            pass

    def prace_klasowe(self):
        page3 = self.browser.open(
            "https://synergia.librus.pl/terminarz")
        p = self.browser.get_current_page()
        kalendarz = p.find('table', class_='kalendarz').findAll(
            'td', class_='center')

        x = []
        for prac_kl in kalendarz:
            prace_klasowa = prac_kl.findAll(
                'td', style='background-color: #FFD700; cursor: pointer;')

            for y in prace_klasowa:
                x.append(y['onclick'])

        linki2 = []
        base = 'https://synergia.librus.pl'
        full_links = []
        for cut in x:
            cut = cut.split("location.href='", 1)[1]
            cut = cut[:-1]
            linki2.append(cut)
            pelen_link = base + cut
            full_links.append(pelen_link)

        opisy = []
        te = []
        for link in self.full_links[:2]:
            page3 = self.browser.open(link)
            p = self.browser.get_current_page()
            tabelka = p.find(
                'table', class_='decorated small center').find('tbody')
            tab_text = tabelka.text
            # Clean the input data by splitting by row and removing blanks
            clean = [i.strip() for i in tab_text.split("\n") if i]

            # Assume the data is in pairs and group them in key,pair by using index
            # and index+1 in [0,2,4,6...]
            d = {clean[ind]: clean[ind + 1] for ind in range(0, len(clean), 2)}

        for link in full_links:
            page3 = self.browser.open(link)
            p = self.browser.get_current_page()
            tabelka = p.find(
                'table', class_='decorated small center').find('tbody')
            tab_text = tabelka.text
            clean = [i.strip() for i in tab_text.split("\n") if i]

            # Assume the data is in pairs and group them in key,pair by using index
            # and index+1 in [0,2,4,6...]
            d = {clean[ind]: clean[ind + 1] for ind in range(0, len(clean), 2)}
            if 'Przedmiot' in d:
                pass

            else:
                d.update({'Przedmiot': 'Język polski'})
            self.prace.append(d)

    def sprawdziany(self):
        now = datetime.datetime.now()

        page3 = self.browser.open(
            "https://synergia.librus.pl/terminarz")
        p = self.browser.get_current_page()
        kalendarz = p.find('table', class_='kalendarz').findAll(
            'td', class_='center')

        x = []
        for spr in kalendarz:

            # lista sprawdzianów
            sprawdzian = spr.findAll(
                'td', style='background-color: #7B68EE; cursor: pointer;')

            # jeden sprawdzian

            for y in sprawdzian:
                x.append(y['onclick'])

        linki2 = []
        base = 'https://synergia.librus.pl'

        for cut in x:
            cut = cut.split("location.href='", 1)[1]
            cut = cut[:-1]
            linki2.append(cut)
            pelen_link = base + cut
            self.full_links.append(pelen_link)

        for link in self.full_links:
            page3 = self.browser.open(link)
            p = self.browser.get_current_page()
            tabelka = p.find(
                'table', class_='decorated small center').find('tbody')
            tab_text = tabelka.text
            clean = [i.strip() for i in tab_text.split("\n") if i]

            # Assume the data is in pairs and group them in key,pair by using index
            # and index+1 in [0,2,4,6...]
            d = {clean[ind]: clean[ind + 1] for ind in range(0, len(clean), 2)}
            if 'Przedmiot' in d:
                pass

            else:
                d.update({'Przedmiot': 'Język polski'})
            self.full_spr.append(d)

    def wiadomosci(self):
        page3 = self.browser.open(
            "https://synergia.librus.pl/wiadomosci")
        p = self.browser.get_current_page()
        tabela = p.find('table', class_='decorated stretch').find(
            'tbody').findAll('td')

        linki_do_wiado = []
        for td in tabela:
            x = td.findAll('a')
            for y in x:
                linki_do_wiado.append(y['href'])

        linki_do_wiado = list(filter(
            lambda a: a != 'javascript:void(0); return false;', linki_do_wiado))

        base = 'https://synergia.librus.pl'
        wiadomosci_linki = []
        for link in linki_do_wiado:
            plen_link = base + link
            wiadomosci_linki.append(plen_link)

        # otwieranie linkow z wiadomosciami
        x = []
        y = []
        for link in wiadomosci_linki:
            page3 = self.browser.open(link)
            p = self.browser.get_current_page()
            wiadomosc = p.find('div', class_='container-message-content')
            y.append(wiadomosc.text)

        try:
            y.remove(' ')
        except:
            pass
        self.wiadomosciText = y

    def konfiguracjaOcen(self, oceny):
        try:
            del oceny[0]
        except IndexError:
            raise Exception("BŁĄD")
        try:
            oceny.remove('0')
            oceny.remove('')
            oceny.remove('-')
            oceny.remove('+')
            oceny.remove('bz')
        except:
            pass
        # show all without np , T, bz , = , -
        self.oceny2 = list(filter(lambda a: a != 'np' and a != 'T' and a != 'bz' and a != '+' and a != '-', oceny))
        self.oceny2 = list(map(float, self.oceny2))

    def sredniaArytmetyczna(self, oceny):
        liczba_ocen = len(oceny)
        wartos_ocen = sum(oceny)

        srednia = wartos_ocen / liczba_ocen

        return srednia
