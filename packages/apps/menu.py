# Main menu for the Fri3dcamp badge

import hardware_setup
from gui.core.ugui import Screen, ssd

from gui.widgets.label import Label
from gui.widgets.buttons import Button, CloseButton
from gui.widgets.checkbox import Checkbox
from gui.core.writer import CWriter
from gui.widgets.menu import Menu

# Font for CWriter
import gui.fonts.freesans20 as font
from gui.core.colors import *

from settings import Settings

wri = CWriter(ssd, font, YELLOW, BLACK)

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

class SettingsScreen(Screen):

    def __init__(self):
        super().__init__()

        Label(wri, 10, 10, 'Settings')

        self.settings = Settings()
        row = 30+4
        column = 4
        for key, value in self.settings.items():
            label = Label(wri, row, column, key)
            if (type(value) == bool):
                Checkbox(wri, row, ssd.width-20, height=12, value=value, callback=self.settings_cb, args=(key,))

            row = row + label.height + 2
        
        CloseButton(wri)

    def settings_cb(self, widget, key):
        value = widget.value()
        self.settings.set(key, value)
    
    def on_hide(self):
        self.settings.store()

class MenuScreen(Screen):

    def __init__(self):
        super().__init__()

        def menu_cb(button, screen):
            Screen.change(screen)

        menuitems = (
            ('Run', menu_cb, (RunScreen,)),
            ('Install', menu_cb, (InstallScreen,)),
            ('Settings', menu_cb, (SettingsScreen,))
        )
        Menu(wri, args=menuitems)
        Label(wri, 100, 60, 'Enjoy Fri3d Camp!')

def run():
    print('Fri3d Camp menu is running.')
    print('Ctrl-C to get Python REPL.')

    Screen.change(MenuScreen)

run()