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

import pygtk
import gtk
from gettext import gettext as _
import pynotify
import time

class GNazar():
    def __init__(self):
        # create a new Status Icon
        self.gnazar = gtk.StatusIcon()
        self.gnazar.set_from_file("../icons/hi22-app-gnazar-deactive.png")
        self.gnazar.set_tooltip(_("GNazar - You are completely demilitarized..."))
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

        self._notification()

    '''
    show popup menu
    '''
    def show_menu(self, status_icon, button, activate_time):
        self.menu.popup(None, None, gtk.status_icon_position_menu, button, activate_time, status_icon)

    # random notification
    def _notification(self):
        while(True):
            time.sleep(5)
            print "Oboooo"
            self.notification()
            self._notification()

    '''
    show about
    '''
    def show_about(self, widget):
        print "Abooouuuuvvtt"
        about = gtk.AboutDialog()
        about.set_program_name("GNazar")
        about.set_version("0.1")
        about.set_copyright("(c) Aşkın Yollu")
        about.set_comments(_("GNazar is a useful part of the Pardus Linux"))
        about.set_website("http://www.askin.ws")
        about.set_logo(gtk.gdk.pixbuf_new_from_file("../icons/hi32-app-gnazar.png"))
        about.set_translator_credits("")
        about.set_artists("")
        about.run()
        about.destroy()

    # destroy callback
    def destroy(self, widget):
        gtk.main_quit()

    # popup callback
    def protect(self, widget):
        if self.status == False:
            dialog = gtk.MessageDialog(
                parent         = None,
                flags          = gtk.DIALOG_DESTROY_WITH_PARENT,
                type           = gtk.MESSAGE_INFO,
                buttons        = gtk.BUTTONS_OK,
                message_format = _("GNazar is starting to protect your Pardus Linux from harmful looks...")
                )
            dialog.set_title(_("GNazar Application"))
            dialog.connect('response', self.dialog_destroyer)
            dialog.show()
            self.status = True
            self.gnazar.set_tooltip(_("GNazar - No harmful look allowed!"))
            self.gnazar.set_from_file("../icons/hi22-app-gnazar.png")

    def release(self, widget):
        if self.status == True:
            dialog = gtk.MessageDialog(
                parent         = None,
                flags          = gtk.DIALOG_DESTROY_WITH_PARENT,
                type           = gtk.MESSAGE_WARNING,
                buttons        = gtk.BUTTONS_OK,
                message_format = _("GNazar is stopping to protect your Pardus Linux from harmful looks...")
                )
            dialog.set_title(_("GNazar Application"))
            dialog.connect('response', self.dialog_destroyer)
            dialog.show()
            self.status = False
            self.gnazar.set_tooltip(_("GNazar - You are completely demilitarized..."))
            self.gnazar.set_from_file("../icons/hi22-app-gnazar-deactive.png")

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
            self.gnazar.set_tooltip(_("GNazar - %s attacks received so far, %s are defated and %s are received...") %
                                    (self.total_attack, self.defated_attack, self.total_attack - self.defated_attack))
        notify = pynotify.Notification(title, body, icon)
        notify.set_urgency(pynotify.URGENCY_NORMAL)
        notify.set_timeout(pynotify.EXPIRES_NEVER)
        notify.show()

    def dialog_destroyer(self, dialog, widget):
        dialog.destroy()

if __name__ == "__main__":
    statusicon = GNazar()
    gtk.main()
    #threading.start_new_thread(gtk.main(), ())
    statusicon._notification()
