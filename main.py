#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
#  IQplayer
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
import tkinter as tk
import urllib.request
from functools import partial

import requests
from lxml import html
from PIL import Image, ImageTk

version = 'IQplayer 17.05.21 \n'


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
    def __init__(self, name, url, num, capi, img):
        self.name = name
        self.url = url
        self.num = num
        self.capi = capi
        self.img = img


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
    serie_image = page.xpath('//a[@class="fa-play"]//img/@src')
    link_num = len(serie_links)
    if link_num != len(serie_names):
        print('[!] Error Faltan Enlaces!')
        return False
    # Crear lista Serie
    serie_list = []
    for n in range(0, link_num):
        serie = Serie(serie_names[n], serie_links[n], n, serie_capi[n], serie_image[n])
        serie_list.append(serie)
    return serie_list


def get_episodes_link(url):
    url = 'https://animeflv.net' + url
    page = geturl(url)
    raw_links = page.xpath('//script[contains(., "video")]/text()')
    ep_names = page.xpath('//div[@class="CapiTop"]/h1/text()')
    raw_links = raw_links[0].split('":"')
    stream = []

    for a in raw_links:
        if "https:" in a:
            b = a.split('"')
            for c in b:
                if 'stream' in c:
                    stream.append(c)
                if 'embed' in c:
                    stream.append(c)

    se_list = []
    for a in stream:
        servidor = Servidor(a, ep_names[0])
        se_list.append(servidor)
    streaming(se_list)


def download(stream, save_path, title_capitulo):
    i = 0
    while i < len(stream):
        n = str(i)
        dl = 'youtube-dl -o "' + save_path + '/' + title_capitulo + ' ' \
             + n + '.mp4''"' + ' ' + stream[i].url
        er = os.system(dl)
        if er == 0:
            i = len(stream)
        else:
            i += 1


def streaming(stream):
    i = 0
    while i < len(stream):
        dl = 'mpv ' + stream[i].url
        er = os.system(dl)
        if er == 0:
            i = len(stream)
        else:
            i += 1


def display_result(results):
    while True:
        today = datetime.datetime.today().strftime('%H:%M del %d-%m-%Y')
        clear()
        url = 'https://animeflv.net'
        root = tk.Tk()
        root.title(version)
        left_frame = tk.Frame(root, width=200, height=400)
        left_frame.grid(row=5, column=4, padx=10, pady=5)
        btn = []
        img = []
        j = 0
        i = 0
        for busque in results:
            # urllib.request.urlretrieve(url + busque.img, busque.name+'.jpg')
            # img.append(ImageTk.PhotoImage(file=busque.name+'.jpg'))
            img_python = (Image.open(requests.get(url + busque.img, stream=True).raw))
            img.append(ImageTk.PhotoImage(img_python))
            print(busque.url,busque.name,busque.img)
            btn.append(
                tk.Button(left_frame, text=busque.name, image=img[busque.num],
                          command=partial(get_episodes_link, busque.url)).grid(row=i, column=j))

            j += 1
            if j == 4:
                i += 1
                j = 0
        root.mainloop()


# Función Principal
def main():
    # Mostrar Series Encontradas
    busque = search_engine()
    display_result(busque)


if __name__ == "__main__":
    while True:
        main()
