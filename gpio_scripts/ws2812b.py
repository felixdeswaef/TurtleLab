import time
import board
import neopixel
from adafruit_led_animation.animation.blink import Blink
from adafruit_led_animation.animation.comet import Comet
from adafruit_led_animation.animation.chase import Chase
from adafruit_led_animation.animation.rainbow import Rainbow
from adafruit_led_animation.sequence import AnimationSequence
from adafruit_led_animation.color import *

pixel_pin = board.D18
num_pixels = 34
ORDER = neopixel.GRB

pixels = neopixel.NeoPixel(
    pixel_pin, num_pixels, brightness=0.5, auto_write=False, pixel_order=ORDER
)

blink = Blink(pixels, speed=0.1, color=WHITE)
comet = Comet(pixels, speed=0.1, color=PURPLE, tail_length=17, bounce=True)
chase = Chase(pixels, speed=0.1, size=4, spacing=6, color=AMBER)
rainbow = Rainbow(pixels, speed=0.1, period=3, step=5)

animations = AnimationSequence(blink, comet, chase, rainbow, advance_interval=5, auto_clear=True)

while True:
    animations.animate()