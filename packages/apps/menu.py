# Main menu for the Fri3dcamp badge

import uasyncio as asyncio

import hardware_setup
from gui.core.ugui import Screen, ssd, Window

from gui.widgets.label import Label
from gui.widgets.buttons import Button, CloseButton
from gui.widgets.checkbox import Checkbox
from gui.core.writer import CWriter
from gui.widgets.menu import Menu

# Font for CWriter
import gui.fonts.freesans20 as font
from gui.core.colors import *

import settings

wri = CWriter(ssd, font, YELLOW, BLACK, verbose=False)

class RunScreen(Screen):
    def __init__(self):
        super().__init__()

        Label(wri, 10, 10, 'Run')
        CloseButton(wri)

class InstallScreen(Screen):
    def __init__(self):
        super().__init__()

        Label(wri, 10, 10, 'Install')
        CloseButton(wri)

def settings_cb(widget, dict, key):
    value = widget.value()
    dict[key] = value

class SettingsScreen(Screen):

    def sub_settings_button(self, row, col, text, sub_settings):
        def fwd(button):
            Screen.change(SettingsScreen, args = ("Settings > " + text, sub_settings))

        Button(wri, row, col, callback = fwd, text='>>>')

    def __init__(self, text, settings_dict):
        super().__init__()

        CloseButton(wri)

        Label(wri, 10, 10, text)

        row = 30+4
        column = 4
        for key, value in settings_dict.items():
            label = Label(wri, row, column, key)
            if (type(value) == bool):
                Checkbox(wri, row, ssd.width-20, height=12, value=value, callback=settings_cb, args=(settings_dict, key))
            elif type(value) == dict:
                self.sub_settings_button(row, ssd.width-20, key, value)

            row = row + label.height + 2
    
    def on_hide(self):
        settings.store()

class MenuScreen(Screen):

    def __init__(self):
        super().__init__()

        def menu_cb(button, screen, *args):
            Screen.change(screen, args=args)

        menuitems = (
            ('Run', menu_cb, (RunScreen,)),
            ('Install', menu_cb, (InstallScreen,)),
            ('Settings', menu_cb, (SettingsScreen, 'Settings', settings.current_settings))
        )
        Menu(wri, args=menuitems)
        Label(wri, 100, (ssd.width//2)-(164//2), 'Enjoy Fri3d Camp!')

        if settings.get('wifi_enabled'):
            self.wifilbl = Label(wri, ssd.height-14, 10, ssd.width - 12)
            update = asyncio.create_task(self.update_wifi())
            self.reg_task(update, on_change=True)

    async def update_wifi(self):
        import wifi
        while(True):
            self.wifilbl.value('Wi-Fi: {}'.format(wifi.status()))
            await asyncio.sleep(1)

def run():
    print('Fri3d Camp menu is running.')
    print('Ctrl-C to get Python REPL.')

    Screen.change(MenuScreen)

run()