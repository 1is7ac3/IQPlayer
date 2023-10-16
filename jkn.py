#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
#  AnimeFlv
#
#  Copyright 2017 1is7ac3 <isaac.qa13@gmail.com>
#  Autor: Isaac Quiroz
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.

import datetime
import os
import sys
import typing
from PyQt6 import QtCore
from PyQt6.QtWidgets import QWidget
import requests
from lxml import html
import PyQt6.QtWidgets as Qt

version = 'JKN 17.05.21 \n'


class Episode:
    def __init__(self, name, num, url):
        self.name = name
        self.num = num
        self.url = url


class Servidor:
    def __init__(self, url, namecap):
        self.url = url
        self.namecap = namecap


class Serie:
    def __init__(self, name, url, num, capi):
        self.name = name
        self.url = url
        self.num = num
        self.capi = capi


class MainWindows(Qt.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('IQplayer')


def clear():
    if os.name == "posix":
        os.system('clear')
    else:
        os.system('cls')
    return


def geturl(url):
    try:
        page = requests.get(url)
        if page.status_code == 200:
            page = page.content.decode('utf-8')
        else:
            raise ValueError(f'Error: {page.status_code}')
    except ValueError as ve:
        print(ve)
        return False
    page = html.fromstring(page)
    return page


def search_engine():
    search_url = 'https://animeflv.net'
    page = geturl(search_url)
    serie_links = page.xpath('//a[@class="fa-play"]/@href')
    serie_names = page.xpath('//a/strong[@class="Title"]/text()')
    serie_capi = page.xpath('//a/span[@class="Capi"]/text()')
    link_num = len(serie_links)
    if link_num != len(serie_names):
        print('[!] Error Faltan Enlaces!')
        return False
    # Crear lista Serie
    serielist = []
    for n in range(0, link_num):
        serie = Serie(serie_names[n], serie_links[n], n, serie_capi[n])
        serielist.append(serie)
    return serielist


def GetEpisodesLink(url):
    url = 'https://animeflv.net'+url
    page = geturl(url)
    rawLinks = page.xpath('//script[contains(., "video")]/text()')
    epNames = page.xpath('//div[@class="CapiTop"]/h1/text()')
    rawLinks = rawLinks[0].split('":"')
    stream = []

    for a in rawLinks:
        if "https:" in a:
            b = a.split('"')
            for c in b:
                if 'stream' in c:
                    stream.append(c)
                if 'embed' in c:
                    stream.append(c)

    seList = []
    for a in stream:
        servidor = Servidor(a, epNames[0])
        seList.append(servidor)
    return seList


def Download(stream, savePath, titleCapitulo):
    i = 0
    while i < len(stream):
        n = str(i)
        dl = 'youtube-dl -o "' + savePath + '/' + titleCapitulo + ' ' \
            + n + '.mp4''"' + ' ' + stream[i].url
        er = os.system(dl)
        if er == 0:
            i = len(stream)
        else:
            i += 1


def streaming(stream):
    i = 0
    while i < len(stream):
        n = str(i)
        dl = 'mpv ' + stream[i].url
        er = os.system(dl)
        if er == 0:
            i = len(stream)
        else:
            i += 1


def DisplayResult(results):
    while True:
        today = datetime.datetime.today().strftime('%H:%M del %d-%m-%Y')
        clear()
        print(version)
        print(f'Hora de actualizacion: {today}')
        print('Compruebe la serie que desea Descargar: ')
        app = Qt.QApplication(sys.argv)

        app.exec()
        for busque in results:
            n = str(busque.num)
            print('[', n, ']', busque.name)
        choice = input('\n Introduzca el numero de la serie a descargar: ')
        if choice.isdigit():
            choice = int(choice)
            if choice >= len(results):
                print('[!] Error!. El numero no esta en la lista.')
                input()
            else:
                return choice
        else:
            print('[!]Error! Introduzca un numero.')
            input()


# Función Principal
def main():
    # Mostrar Series Encontradas
    busque = search_engine()
    choice = DisplayResult(busque)
    # Mostrar Servidores de Descarga
    title = busque[choice].name
    servi = GetEpisodesLink(busque[choice].url)
    titleCapitulo = servi[0].namecap
    op = input('[D]escargar o [V]er: ')
    if op == 'v':
        print(title)

    # Ubicacion de Descarga
    # path = os.environ['HOME']+'/.Anime'
    # Nombre Carpeta
    # if not os.path.exists(path):
    #    os.mkdir(path)
    # folderName = title
    # savePath = os.path.join(path, folderName)
    # if not os.path.exists(savePath):
    #    os.mkdir(savePath)
    # Download(servi, savePath, titleCapitulo)


if __name__ == "__main__":
    while True:
        main()
