#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""IQplayer
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
"""

from datetime import datetime
from functools import partial
import os
import subprocess
from typing import Sequence, cast
from PySide6.QtGui import QPixmap
import requests
from lxml import html
from PIL import Image
from PySide6.QtWidgets import QApplication, QPushButton
from PIL.ImageQt import ImageQt
import ui_main

VERSION = "IQplayer 26.08.24"
WINDOW_TITLE_PREFIX = "IQPlayer"
GRID_COLS = 6
GRID_ROWS_PER_PAGE = 6
CARD_WIDTH = 150
CARD_HEIGHT = 150


class Episode:
    """Clase para almacenar los datos de un episodio"""

    def __init__(self, name: str, num: int, url: str):
        self.name = name
        self.num = num
        self.url = url


class Servidor:
    """Clase para almacenar los datos de un servidor de streaming"""

    def __init__(self, url: str, namecap: str):
        self.url = url
        self.namecap = namecap


class Serie:
    """Clase para almacenar los datos de una serie"""

    def __init__(self, name: str, url: str, num: int, cap: str, img: str):
        self.name = name
        self.url = url
        self.num = num
        self.cap = cap
        self.img = img


def clear():
    """Función para limpiar la pantalla de la terminal"""
    if os.name == "posix":
        subprocess.run(["clear"], check=False)
    else:
        subprocess.run(["cls"], check=False)
    return


def geturl(url: str):
    """Función para obtener el contenido de una URL y parsearlo como HTML"""
    try:
        page = requests.get(url, timeout=30)
        if page.status_code == 200:
            page = page.content.decode("utf-8")
        else:
            raise ValueError(f"Error: {page.status_code}")
    except ValueError as ve:
        print(ve)
        return False
    pages: html.HtmlElement = html.fromstring(page)
    return pages


def to_str(element: html.HtmlElement | bool | None, query: str) -> list[str]:
    """Extrae una lista de strings de forma segura y tipada."""
    if element is None:
        return []
    root = cast(html.HtmlElement, element)
    raw_result: list[object] = cast(list[object], root.xpath(query))
    return [item for item in raw_result if isinstance(item, str)]


def search_engine():
    """
    Función para buscar series en el sitio web de animeflv.net
    """
    search_url = "https://jkanime.net"
    page = geturl(search_url)
    q_link = '//div[@id="animes"]//div[@class="card ml-2 mr-2"]/a/@href'
    q_name = '//div[@id="animes"]//h5[@class="strlimit card-title"]/text()'
    q_cap = '//div[@id="animes"]//span[@class="badge badge-primary"]/text()'
    q_image = '//div[@id="animes"]//div[@class="d-thumb"]//img/@src'
    links = to_str(page, q_link)
    names = to_str(page, q_name)
    cap = to_str(page, q_cap)
    image = to_str(page, q_image)
    num_links = len(links)
    if num_links != len(names):
        print("[!] Error Faltan Enlaces!")
        return False
    # Crear lista Serie
    serie_list: list[Serie] = []
    for n in range(0, num_links):
        serie = Serie(names[n], links[n], n, cap[n], image[n])
        serie_list.append(serie)
    return serie_list


def get_episodes_link(url: str):
    """
    Función para obtener los enlaces de los episodios de una serie
    """
    page = geturl(url)
    links = to_str(page, '//script[contains(., "jkplayer")]/text()')
    names = to_str(page, '//div[@class="breadcrumb__links"]/h1/text()')
    links = links[0].split('":"')
    stream: list[str] = []

    for a in links:
        if "https:" in a:
            b = a.split('"')
            for c in b:
                if "/jkplayer/" in c:
                    stream.append(c)
    se_list: list[Servidor] = []
    for a in stream:
        servidor = Servidor(a, names[0])
        se_list.append(servidor)
    streaming(se_list)


def download(stream: Sequence[Servidor], save_path: str, title_capitulo: str):
    """
    Función para descargar videos de los servidores de streaming"""
    i = 0
    while i < len(stream):
        n = str(i)
        dl = (
            'yt-dlp -o "' + save_path + "/" + title_capitulo + " " + n + ".mp4"
            '"' + " " + stream[i].url
        )
        er = subprocess.run(dl, shell=True, check=False).returncode
        if er == 0:
            i = len(stream)
        else:
            i += 1


def streaming(stream: Sequence[Servidor]):
    """
    Función para reproducir videos en streaming
    """
    i = 0
    while i < len(stream):
        dl = ["mpv", stream[i].url]
        er = subprocess.run(dl, check=False, capture_output=True)
        if er.returncode == 0:
            i = len(stream)
        else:
            i += 1


def display_result_qt(results: Sequence[Serie], window: ui_main.MainWindow):
    """
    Función para mostrar los resultados en una ventana de PySide6
    """
    window.spinner.hide()
    layout = window.results_layout
    i = 0
    j = 0
    for busque in results:
        img_python = Image.open(requests.get(busque.img, stream=True, timeout=30).raw)
        size = (CARD_WIDTH, CARD_HEIGHT)
        img_resize = img_python.resize(size, Image.Resampling.LANCZOS)
        img_qt = QPixmap.fromImage(ImageQt(img_resize))
        btn = QPushButton()
        btn.setIcon(img_qt)
        btn.setIconSize(img_qt.size())
        btn.setFixedSize(CARD_WIDTH, CARD_HEIGHT + 30)
        btn.clicked.connect(partial(get_episodes_link, busque.url))
        layout.addWidget(btn, i, j)
        j += 1
        if j == GRID_COLS:
            i += 1
            j = 0


# Función Principal
def main():
    """
    Mostrar Series Encontradas
    """
    app = QApplication([])
    window_qt = ui_main.MainWindow()
    window_qt.setWindowTitle(WINDOW_TITLE_PREFIX + " - " + VERSION)
    window_qt.setGeometry(100, 100, 800, 600)
    window_qt.show()
    busque = search_engine()
    if busque:
        display_result_qt(busque, window_qt)
    app.exec()


if __name__ == "__main__":
    main()
