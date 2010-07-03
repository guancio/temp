#!/usr/bin/python

import clutter
import sys
import dbus
import dbus.service
from dbus.mainloop.glib import DBusGMainLoop


class DMenuService(dbus.service.Object):
    def __init__(self):
        self.bus = bus=dbus.SessionBus()
        bus_name = dbus.service.BusName('net.guancio.dmenuservice', bus)
        dbus.service.Object.__init__(self, bus_name, '/net/guancio/dmenuservice')

        # Configurations
        self.not_sel_bg_color = clutter.Color(0x00, 0x00, 0x00, 0xff)
        self.not_sel_fn_color = clutter.Color(0x8f, 0x8f, 0x8f, 0xff)
        self.sel_fn_color = clutter.Color(0xe0, 0xe0, 0xe0, 0xff)
        self.sel_bg_color = clutter.Color(0x5c, 0x6f, 0x99, 0xff)
        self.n_display_lines = 20
        self.animation_time = 100

        #Graphic States
        self.stage = None
        self.rect = None
        self.labels = []
        self.main_label = None
        self.selected = 0
        self.line_shift = 0
        

        #Search Status
        self.main_lines = []
        self.lines = []
        self.search_text = ""

        self.init_graphics()

    def init_graphics(self, ):
        """
        """
        self.stage = clutter.Stage()
        self.stage.set_size(400, 500)
        self.stage.set_color(self.not_sel_bg_color)

        self.rect = clutter.Rectangle()
        #rect.set_color(sel_bg_color)
        self.rect.set_color(self.not_sel_bg_color)
        self.rect.set_border_color(self.sel_bg_color)
        self.rect.set_border_width(1)
        self.rect.set_size(360, 20)
        self.rect.set_position(20, 10)
        self.stage.add(self.rect)
        self.rect.show()

        self.main_label = clutter.Text()
        self.main_label.set_position(20,10)
        self.main_label.set_color(self.not_sel_fn_color)
        self.main_label.set_font_name("Terminus 14")
        self.main_label.set_text("")
        self.stage.add(self.main_label)
        self.main_label.show()
        for x in range(self.n_display_lines):
            self.label = clutter.Text()
            self.label.set_position(20,10 + 20 + 20 * x)
            self.label.set_color(self.not_sel_fn_color)
            self.label.set_font_name("Terminus 14")
            self.stage.add(self.label)
            self.label.show()
            self.labels.append(self.label)


        self.stage.connect("key-press-event", self.key_press_handle)
        self.stage.connect("destroy", clutter.main_quit)
        self.stage.set_key_focus(None)

    def update_texts(self):
        for i in range(min(len(self.labels), len(self.lines))):
            self.labels[i].set_text(self.lines[self.line_shift + i])
        for i in range(len(self.labels) - len(self.lines)):
            self.labels[len(self.lines) + i].set_text("")
    
    def move_selection(self, direction):
        """
        """
        old_selected = self.selected
        if direction is None:
            self.selected = 0
            self.line_shift = 0
        else:
            self.selected += direction
        if self.selected >= len(self.labels):
            self.line_shift += self.selected - len(self.labels)
            self.selected = len(self.labels) - 1
            if self.line_shift + self.selected >= len(self.lines):
                self.line_shift = 0
                self.selected = 0
            self.update_texts()
        if self.selected < 0:
            self.line_shift += self.selected
            self.selected = 0
            if self.line_shift < 0:
                self.line_shift = len(self.lines) - len(self.labels) -1
                self.selected = len(self.labels)-1
            self.update_texts()
        self.rect.animate(clutter.LINEAR, self.animation_time,
                          "y", 10 + 20 + 20 * self.selected)
        self.labels[self.selected].animate(clutter.LINEAR,self.animation_time,
                                           "scale-x", 1.2,
                                           "color", self.sel_fn_color)
        if old_selected != self.selected:
            self.labels[old_selected].animate(clutter.LINEAR, self.animation_time,
                                              "scale-x", 1,
                                              "color", self.not_sel_fn_color)

    def key_press_handle(self, actor, event):
        """
        """
        print event.get_key_code()
        print event.get_key_symbol()
        key_code = event.get_key_code()
        key_char = chr(event.get_key_unicode())
        if key_code == 9:
            client = self.bus.get_object('net.guancio.dmenuclient', '/net/guancio/dmenuclient')
            get_result = client.get_dbus_method('get_result', 'net.guancio.dmenuclient')
            get_result("")

            self.stage.hide()
            return
        if key_code == 36:
            client = self.bus.get_object('net.guancio.dmenuclient', '/net/guancio/dmenuclient')
            get_result = client.get_dbus_method('get_result', 'net.guancio.dmenuclient')
            get_result(self.lines[self.line_shift + self.selected])

            self.stage.hide()
            return
        if key_code == 116:
            self.move_selection(1)
            return
        if key_code == 117:
            self.move_selection(len(self.labels))
            return
        if key_code == 111:
            self.move_selection(-1)
            return
        if key_code == 112:
            self.move_selection(-len(self.labels))
            return
        if key_code != 22 and key_char == "\x00":
            return
        if key_code == 22:
            self.search_text = self.search_text[:-1]
        else:
            self.search_text += key_char
        self.main_label.set_text(self.search_text)
        self.lines = [l for l in self.main_lines if l.find(self.search_text) >= 0]
        self.update_texts()
        self.move_selection(None)
        
            # stage.set_properties("rotation-center-y", clutter.Vertex(200, 250, 0))
            # if scaled:
            #     scaled = False
            #     stage.animate(clutter.LINEAR, 1000, "rotation-angle-y", 0)
            # else:
            #     scaled = True
            #     stage.animate(clutter.LINEAR, 1000, "rotation-angle-y", 180)
            # # sys.stdout.write(lines[line_shift + selected])
            # # clutter.main_quit()
            # return

    @dbus.service.method("net.guancio.dmenuservice")
    def show(self, variant):
        self.main_lines = variant
        self.lines = self.main_lines
        self.update_texts()
        self.move_selection(None)
        self.stage.show()
        return repr(self.main_lines)

if __name__ == '__main__':
    DBusGMainLoop(set_as_default=True)
    myservice = DMenuService()
    clutter.main()

