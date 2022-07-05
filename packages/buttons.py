# define buttons

from machine import Pin, Signal

# The only use button on the badge
BTN_BOOT = 0

boot_pin = Pin(BTN_BOOT)
boot_button = Signal(boot_pin, invert=True)

# The buttons on the GameOn addon
