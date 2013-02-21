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
from distutils import cmd
from distutils.command.install_data import install_data as _install_data
from distutils.command.build import build as _build
from distutils.command.install import install as _install

import msgfmt
import os


# Build translation files
class build_trans(cmd.Command):
    description = 'Compile .po files into .mo files'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        po_dir = os.path.join(os.path.dirname(os.curdir), 'data/locale')
        for path, names, filenames in os.walk(po_dir):
            for f in filenames:
                if f.endswith('.po'):
                    lang = f[:-3]
                    src = os.path.join(path, f)
                    dest_path = os.path.join('build', 'locale',
                                             lang, 'LC_MESSAGES')
                    dest = os.path.join(dest_path, 'gnazar.mo')
                    if not os.path.exists(dest_path):
                        os.makedirs(dest_path)
                    if not os.path.exists(dest):
                        print 'Compiling %s' % src
                        msgfmt.make(src, dest)
                    else:
                        src_mtime = os.stat(src)[8]
                        dest_mtime = os.stat(dest)[8]
                        if src_mtime > dest_mtime:
                            print 'Compiling %s' % src
                            msgfmt.make(src, dest)


# Override build class to compile translation files
class build(_build):
    sub_commands = _build.sub_commands + [('build_trans', None)]

    def run(self):
        _build.run(self)


# Override install_data class to install translation files
class install_data(_install_data):

    def run(self):
        for lang in os.listdir('build/locale/'):
            lang_dir = os.path.join('..', 'locale', lang, 'LC_MESSAGES')
            lang_file = os.path.join('build', 'locale', lang,
                                     'LC_MESSAGES', 'gnazar.mo')
            self.data_files.append((lang_dir, [lang_file]))
        _install_data.run(self)


# installation steps
cmdclass = {
    'build': build,
    'build_trans': build_trans,
    'install_data': install_data
}


# data files
datas = [('', ['README', 'COPYING', 'AUTHORS', 'ChangeLog']),
         ('../applications', ['data/gnazar.desktop']),
         ('../icons/hicolor/32x32/apps',
          ['data/icons/hicolors/32x32/apps/gnazar.png']),
         ('../icons/hicolor/22x22/apps',
          ['data/icons/hicolors/22x22/apps/gnazar.png']),
         ('../icons/hicolor/22x22/apps',
          ['data/icons/hicolors/22x22/apps/gnazar-deactive.png']),
         ('../icons/hicolor/16x16/apps',
          ['data/icons/hicolors/16x16/apps/gnazar.png']),
         ('../locale/tr/LC_MESSAGES',
          ['build/locale/en/LC_MESSAGES/gnazar.mo']),
         ('../locale/en/LC_MESSAGES',
          ['build/locale/en/LC_MESSAGES/gnazar.mo'])]


# Call setup
setup(name='GNazar',
      version='0.2',
      description='GTK Nazar Aplication',
      author='Aşkın Yollu',
      author_email='askin@askin.ws',
      license='GNU General Public License, Version 2',
      url='http://askin.ws',
      packages=['GNazar'],
      data_files=datas,
      scripts=['gnazar'],
      cmdclass=cmdclass)
