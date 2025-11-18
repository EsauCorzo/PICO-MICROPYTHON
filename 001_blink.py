from machine import Pin
from time import sleep_ms

LED_PIN = "LED"
DELAY_VAL = 1000

led = Pin(LED_PIN, Pin.OUT)

while True:
    led.on()
    sleep_ms(DELAY_VAL)
    led.off()
    sleep_ms(DELAY_VAL)