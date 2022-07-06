import machine
import settings

import hardware_setup
from gui.core.writer import CWriter

# Font for CWriter
import gui.fonts.font10 as font
from gui.core.colors import *

ssd = hardware_setup.ssd

wri = CWriter(ssd, font, YELLOW, BLACK, verbose=False)

display = hardware_setup.disp

def show_recover_countdown(count):
    bgcolor = wri.bgcolor
    if (count != 5):
        bgcolor = RED
    display.print_centred(wri, ssd.width//2, ssd.height-20,
        'Hold boot {} seconds to recover.'.format(count), bgcolor=bgcolor)
    ssd.show()

def recover_menu():
    print("Recovering menu!")
    try:
        settings.remove('apps.autorun')
    except KeyError:
        # can happen when no apps.autorun is set
        pass
    settings.store()
    machine.reset()

def start_repl():
    print("Executing REPL!")
    settings.set('apps.autorun', 'frozen_apps.repl')
    settings.store()
    machine.reset()

def start(app, status=False):
    settings.set('apps.autorun', app)
    settings.store()
    machine.reset()
