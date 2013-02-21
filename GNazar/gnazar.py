#!/usr/bin/env python
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

import pygtk
import gtk
import gettext
import pynotify
import time
import os
import sys
import locale
import random
import platform
gtk.gdk.threads_init()

#Translation stuff
localedir = "/usr/share/gnazar/locale"
gettext.bindtextdomain('gnazar', localedir)
gettext.textdomain('gnazar')
sharedirs = '/usr/share'

_ = gettext.gettext


class GNazar():
    def __init__(self):
        # create a new Status Icon
        self.gnazar = gtk.StatusIcon()
        self.gnazar.set_from_file(
            '%s/icons/hicolor/22x22/apps/gnazar-deactive.png' % sharedirs)
        self.gnazar.set_tooltip(
            _("GNazar - You are completely demilitarized..."))
        self.gnazar.set_visible(True)
        self.status = False

        # create menu
        self.menu = gtk.Menu()
        self.gnazar.connect("popup_menu", self.show_menu)

        # connect
        _quit = gtk.ImageMenuItem(gtk.STOCK_QUIT)
        _quit.connect("activate", self.destroy)
        _about = gtk.ImageMenuItem(gtk.STOCK_ABOUT)
        _about.connect("activate", self.show_about)
        _protect = gtk.ImageMenuItem(gtk.STOCK_OK)
        _protect.connect("activate", self.protect)
        _protect.set_label(_("Protect"))
        _release = gtk.ImageMenuItem(gtk.STOCK_CANCEL)
        _release.set_label(_("Release"))
        _release.connect("activate", self.release)

        # add to menu
        self.menu.add(_protect)
        self.menu.add(_release)
        self.menu.add(_about)
        self.menu.add(_quit)
        self.menu.show_all()

        # notification
        pynotify.init(_("GNazar Application"))

        # init attack
        self.total_attack = 0
        self.defated_attack = 0

        self.running = True

        import thread
        thread.start_new_thread(self._notification, ())

    def main(self):
        # gtk main
        gtk.main()

    '''
    show popup menu
    '''
    def show_menu(self, status_icon, button, activate_time):
        self.menu.popup(None, None, gtk.status_icon_position_menu,
                        button, activate_time, status_icon)

    # random notification
    def _notification(self):
        while(self.running):
            time.sleep(random.randrange(3600, 18000))
            #time.sleep(4) # testing
            self.notification()

    '''
    show about
    '''
    def show_about(self, widget):
        about = gtk.AboutDialog()
        about.set_program_name("GNazar")
        about.set_icon_from_file("%s/icons/hicolor/22x22/apps/gnazar.png"
                                 % sharedirs)
        about.set_version("0.1")
        about.set_copyright("(c) Aşkın Yollu")
        # FIXME: make it generic (mac, bsd, win etc..)
        dist_name = platform.dist()[0]
        about.set_comments(_("GNazar is a useful part of the %s" % dist_name))
        about.set_website("http://www.askin.ws")
        about.set_logo(gtk.gdk.pixbuf_new_from_file(
                "%s/icons/hicolor/32x32/apps/gnazar.png" % sharedirs))
        about.set_translator_credits(_("TRANSLATORS"))
        about.set_artists([_("THANKSFORICONS")])
        about.run()
        about.destroy()

    # destroy callback
    def destroy(self, widget):
        self.gnazar.set_visible(False)
        self.running = False
        gtk.main_quit()

    # popup callback
    def protect(self, widget):
        if self.status == False:
            dialog = gtk.MessageDialog(
                parent=None,
                flags=gtk.DIALOG_DESTROY_WITH_PARENT,
                type=gtk.MESSAGE_INFO,
                buttons=gtk.BUTTONS_OK,
                message_format=_("GNazar is starting to protect your "
                                 "computer from harmful looks...")
                )
            dialog.set_title(_("GNazar Application"))
            dialog.connect('response', self.dialog_destroyer)
            dialog.show()
            self.status = True
            self.gnazar.set_tooltip(_("GNazar - No harmful look allowed!"))
            self.gnazar.set_from_file("%s/icons/hicolor/22x22/apps/gnazar.png"
                                      % sharedirs)

    def release(self, widget):
        if self.status == True:
            dialog = gtk.MessageDialog(
                parent=None,
                flags=gtk.DIALOG_DESTROY_WITH_PARENT,
                type=gtk.MESSAGE_WARNING,
                buttons=gtk.BUTTONS_OK,
                message_format=_("GNazar is stopping to protect your computer"
                                 " from harmful looks...")
                )
            dialog.set_title(_("GNazar Application"))
            dialog.connect('response', self.dialog_destroyer)
            dialog.show()
            self.status = False
            self.gnazar.set_tooltip(
                _("GNazar - You are completely demilitarized..."))
            self.gnazar.set_from_file(
                "%s/icons/hicolor/22x22/apps/gnazar-deactive.png" % sharedirs)

    def notification(self):
        self.total_attack += 1
        if self.status == True:
            self.defated_attack += 1
            title = _("Nazar eliminated")
            body = _("Nazar Received and eliminated successfuly")
            icon = "gtk-apply"
        else:
            title = _("Nazar harmed")
            body = _("Nazar Received and it HARMED!")
            icon = "dialog-warning"
            self.gnazar.set_tooltip(
                _("GNazar - %s attacks received so far, %s"
                  " are defated and %s are received...") %
                (self.total_attack,
                 self.defated_attack,
                 self.total_attack - self.defated_attack))

        notify = pynotify.Notification(title, body, icon)
        notify.set_urgency(pynotify.URGENCY_NORMAL)
        notify.set_timeout(pynotify.EXPIRES_NEVER)
        notify.show()

    def dialog_destroyer(self, dialog, widget):
        dialog.destroy()


def main():
    si = GNazar()
    si.main()
