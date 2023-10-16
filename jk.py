#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
#  Animeflv
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

import requests
import os
from lxml import html
import datetime
import jkn
import PySide2.QtWidgets  as qt
import sys
# Imprimir versión
version = 'FLV 09.10.23\n'


# Clase Serie
class Serie:
    def __init__(self, name, num, url):
        self.name = name
        self.num = num
        self.url = url


# Clase capitulo
class Servidor:
    def __init__(self, url, namecap):
        self.url = url
        self.namecap = namecap


def Clear():
    if os.name == "posix":
        os.system('clear')
    else:
        os.system('cls')
    return


# Funcion GetUrl verifica estado de la url
def GetUrl(Url):
    try:
        page = requests.get(Url)
        if page.status_code == 200:
            page = page.content.decode('utf-8')
        else:
            raise ValueError(f'Error: {page.status_code}')
    except ValueError as ve:
        print(ve)
        return False
    page = html.fromstring(page)
    return page


# Función Para la captura de los datos de la serie a descargar
def SearchInput(search):
    # Ciclo para la captura
    while True:
        # Imprime versión de la app
        today = datetime.datetime.today().strftime('%H:%M del %d-%m-%Y')
        print(f'Estas usando la version: {version}')
        print(f'Cuando son las {today} se procedera a ralizar la busqueda.\n')
        # Captura el nombre de la serie a buscar
        #search = input(
        #    'Introduzca el nombre de la serie que desea descargar: ')
        # Lanza la función de búsqueda
        bus = SearchEngine(search)
        # Revisa que la búsqueda halla obtenido resultados
        if bus != []:
            return bus
        # Si no encuentra resultados repite el ciclo
        else:
            print('[!]No se encontró, intente nuevamente \n')


# función de búsqueda
def SearchEngine(search):
    # Une el nombre de la búsqueda con la pagina
    searchUrl = 'https://animeflv.net/browse?q='+search
    print(f'Estamos realizando la busqueda de {search} en la pagina.\n')
    # Se revisa el estado de la pagina
    page = GetUrl(searchUrl)
    # Captura los enlaces de las diez primeras series
    Links = page.xpath('//article[@class="Anime alt B"]/a/@href')
    # Captura el nombre de las series desde la pagina web
    Names = page.xpath('//article[@class="Anime alt B"]//h3/text()')
    # Revisa que los nombres coincidan en numero con los enlaces
    linkNum = len(Links)
    if linkNum != len(Names):
        print('[!] Error Faltan Enlaces!')
        return False
    # Crear lista
    serieList = []
    # Guarda los datos obtenidos usando la clase Anime
    print('Por favor, espere se estan guardando los resultados de la busqueda')
    for n in range(0, linkNum):
        serie = Serie(Names[n], n, Links[n])
        serieList.append(serie)
    return serieList

# Función para descargar todos los capítulos
def GetAllCap(url, title):
    # Imprime versión
    print(version)
    urlFlv = 'https://animeflv.net'
    # Se obtiene nombre de usuario
    # Se crea variable con la dirección donde se va a guardar
    #path = os.environ['HOME'] + '/.Anime'
    #if not os.path.exists(path):
    #    os.mkdir(path)
    # Nombre de carpeta
    #folderName = title
    # se unen la ruta de descarga con la carpeta
    #savePath = os.path.join(path, folderName)
    # Se crea la capeta si no se existe
    #if not os.path.exists(savePath):
    #    os.mkdir(savePath)
    # Se verifica la url de los capítulos
    page = GetUrl(urlFlv + url)
    # se extrae los datos del numero de paginas
    pageLinks = page.xpath('//script[contains(., "[[")]/text()')
    pageLinks = pageLinks[0].split('= [[')
    pageLinks = pageLinks[1].split(',')
    i = int(input('Desde que capitulo desea iniciar: '))
    # Ciclo para descarga delos capítulos
    for n in range(i, int(pageLinks[0])):
        # Variable donde se convierte en texto para ser usado en la url
        # Se une la url con el numero del capitulo a descargar
        url2 = '/ver' + url.replace('/anime','') + '-' + str(n)
        print(url2)
        linkVideos = jkn.GetEpisodesLink(url2)
        jkn.streaming(linkVideos)
        # Verifica estado de la url
        #page = GetUrl(url2)
        # Extrae el enlace de descarga
        #rawLinks = page.xpath('//script[contains(., "video")]/text()')
        # Extrae el nombre del capitulo
        #epNames = page.xpath('//div[@class="breadcrumb__links"]/h1/text()')
        #rawLinks = rawLinks[0].split('src="')
        #for i in rawLinks:
        #    if 'jk.php?u=' in i:
         #       steam = i
         #   elif 'jkokru.php?u=' in i:
         #       okru = i
        #steam = steam.split('" width')
        #okru = okru.split('" width')
        #seList = []
        #servidor = Servidor(steam[0].replace('jk.php?u=', ''), epNames[0])
        #seList.append(servidor)
        #servidor2 = Servidor(okru[0].replace(
        #    'https://jkanime.net/jkokru.php?u=', 'https://ok.ru/videoembed/'),
        #    epNames[0])
        #seList.append(servidor2)
        #saveFile = os.path.join(savePath, seList[0].namecap)
        # lanza función download
        #Download(seList, saveFile)


def Download(capitulo, saveFile):
    # Variable para control ciclo
    i = 0
    while i < len(capitulo):
        n = str(i)
        dl = 'youtube-dl -o ''"'+saveFile+' '+n+'.mp4''"'+' '+capitulo[i].url
        # Llama el comando desde el terminal
        er = os.system(dl)
        if er != 0 and not os.path.isfile(saveFile+' '+n+'.mp4'):
            i += 1
        elif er != 0 and os.path.isfile(saveFile+' '+n+'.mp4'):
            er = os.system(dl)
        else:
            i = len(capitulo)


# Función principal
def main():
    # Llama la función para la entrada de la búsqueda
    app = qt.QApplication(sys.argv)

# Create a Qt widget, which will be our window.
    
    label  = qt.QLabel('_Hello')
    label.show()  # IMPORTANT!!!!! Windows are hidden by default.

# Start the event loop.
    app.exec_()

    buscar = search_input()
    # Llama la función para mostrar resultado de la búsqueda
    choice = jkn.DisplayResult(buscar)
    # Obtiene nombre de la serie para la carpeta
    title = buscar[choice].name
    # Llama la función para descargar todo los capítulos
    GetAllCap(buscar[choice].url, title)
# Ciclo para repetir todo


if __name__ == '__main__':
    while True:
        main()
