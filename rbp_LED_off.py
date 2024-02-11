import array, time
from machine import Pin
import rp2

# WS2812 LED Ring Configuration
led_count = 16  # number of LEDs in ring light
PIN_NUM = 6  # pin connected to ring light

@rp2.asm_pio(sideset_init=rp2.PIO.OUT_LOW, out_shiftdir=rp2.PIO.SHIFT_LEFT, autopull=True, pull_thresh=24)
def ws2812():
    T1 = 2
    T2 = 5
    T3 = 3
    wrap_target()
    label("bitloop")
    out(x, 1) .side(0) [T3 - 1]
    jmp(not_x, "do_zero") .side(1) [T1 - 1]
    jmp("bitloop") .side(1) [T2 - 1]
    label("do_zero")
    nop() .side(0) [T2 - 1]
    wrap()

sm = rp2.StateMachine(0, ws2812, freq=8000000, sideset_base=Pin(PIN_NUM))

# Create an array of zero for each LED
pixels = array.array("I", [0 for _ in range(led_count)])

# Activate the state machine
sm.active(1)

# Fill the LED ring with black color
for i in range(led_count):
    pixels[i] = 0
sm.put(pixels, 8)
time.sleep_ms(100)