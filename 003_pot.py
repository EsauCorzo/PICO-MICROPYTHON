from machine import Pin, ADC
from time import sleep_ms

POT_PIN = 26
RESOLUTION = 10

pot = ADC(Pin(POT_PIN))

while True:
    pot_value = pot.read_u16()
    print("ADC Value:", pot_value >> (16 - RESOLUTION))
    sleep_ms(10)