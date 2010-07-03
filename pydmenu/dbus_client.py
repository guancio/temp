#!/usr/bin/python
import dbus
import sys
import gobject
import dbus.service
from dbus.mainloop.glib import DBusGMainLoop

DBusGMainLoop(set_as_default=True)
bus=dbus.SessionBus()

class DMenuClient(dbus.service.Object):
    def __init__(self):
        global bus
        bus_name = dbus.service.BusName('net.guancio.dmenuclient', bus=bus)
        dbus.service.Object.__init__(self, bus_name, '/net/guancio/dmenuclient')

    @dbus.service.method("net.guancio.dmenuclient")
    def get_result(self, result):
        global loop
        sys.stdout.write(result)
        loop.quit()

main_lines = sys.stdin.readlines()

client = DMenuClient()

helloservice = bus.get_object('net.guancio.dmenuservice', '/net/guancio/dmenuservice')
show = helloservice.get_dbus_method('show', 'net.guancio.dmenuservice')
show(main_lines)

loop = gobject.MainLoop()
loop.run()
