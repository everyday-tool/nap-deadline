import gi

gi.require_version('AppIndicator3', '0.1')
gi.require_version('Gtk', '3.0')

from gi.repository import AppIndicator3 as appindicator
from gi.repository import GObject as gobject
from gi.repository import Gtk as gtk
from threading import Thread
import signal
import time
import os

from logic import compute_time_left

class Indicator:

    app = 'Nap countdown'
    icon = 'semi-starred-symbolic'
    update_inteval = 30

    def __init__(self):
        # initialize app indicator
        self.indicator = appindicator.Indicator.new(self.app,
                                                    self.icon,
                                                    appindicator.IndicatorCategory.OTHER)
        self.indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
        self.indicator.set_menu(self.create_menu())
        hour, minute = compute_time_left()
        label = f'{hour}:{minute}'
        self.indicator.set_label(label, self.app)

        # initialize update thread
        self.update = Thread(target=self.show_time_left)

        # daemonize the thread to make the indicator stopable
        self.update.setDaemon(True)
        self.update.start()

    def create_menu(self):
        # initialize menu
        menu = gtk.Menu()

        # separator
        sep = gtk.SeparatorMenuItem()
        menu.append(sep)

        # quit
        item = gtk.MenuItem(label='Quit')
        item.connect('activate', self.stop)
        menu.append(item)

        # show menu
        menu.show_all()
        return menu

    def show_time_left(self):
        while 1:
            # sleep
            time.sleep(self.update_inteval)
            hour, minute = compute_time_left()
            label = f'{hour}:{minute}'
            gobject.idle_add(
                self.indicator.set_label,
                label,
                self.app,
                priority=gobject.PRIORITY_DEFAULT)

    def stop(self, source):
        gtk.main_quit()

def main():
    Indicator()
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    gtk.main()

if __name__ == '__main__':
    main()
