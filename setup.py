#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under GPL v2
# Copyright 2010, Aşkın Yollu <askin@askin.ws>
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#

from distutils.core import setup
import glob

# it is useless when i find a way to compile po files
'''
import os, shutil, sys
from distutils.command.build import build
from distutils.command.clean import clean

try:
    import pygtk
except:
    print "\033[31mWarning: You have to install PyGtk on your system\033[0m"

try:
    import pynotify
except:
    print "\033[31mWarning: You have to install PyNotify on your system\033[0m"

def compile_po(source, target):
    pass

def myclean(clean):
    shutil.rmtree('locale')

def __mybuild(build):
    os.mkdir('locale')
    langs = ['tr', 'en']
    for i lang in langs:
        compile_po('po/gnazar-%s.po' % lang, 'locale/%s/LC_MESSAGES/gnazar.mo' % lang)
'''

# setup
datas = [('', ['README', 'COPYING', 'AUTHORS', 'ChangeLog']),
         ('/usr/share/applications', ['data/gnazar.desktop']),
         ('/usr/share/icons/hicolor/32x32/apps', ['data/icons/hicolors/32x32/apps/gnazar.png']),
         ('/usr/share/icons/hicolor/22x22/apps', ['data/icons/hicolors/22x22/apps/gnazar.png']),
         ('/usr/share/icons/hicolor/22x22/apps', ['data/icons/hicolors/22x22/apps/gnazar-deactive.png']),
         ('/usr/share/icons/hicolor/16x16/apps', ['data/icons/hicolors/16x16/apps/gnazar.png']),
         ('locale', glob.glob('data/locale/*.*')),
         ('locale/tr/LC_MESSAGES', glob.glob('data/locale/tr/LC_MESSAGES/*.*')),
         ('locale/en/LC_MESSAGES', glob.glob('data/locale/en/LC_MESSAGES/*.*'))]

setup(name = 'GNazar',
      version = '0.1',
      description = 'GTK Nazar Aplication',
      author = 'Aşkın Yollu',
      author_email = 'askin@askin.ws',
      license = 'GNU General Public License, Version 2',
      url = 'http://askin.ws',
      packages = ['GNazar'],
      data_files = datas,
      scripts = ['gnazar'],
)


