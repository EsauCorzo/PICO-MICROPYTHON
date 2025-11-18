from machine import Pin
from time import sleep_ms

LED_PIN = "LED"
BUTTON_PIN = 14

led = Pin(LED_PIN, Pin.OUT)
button = Pin(BUTTON_PIN, Pin.IN)
button_pressed = False

while True:
    if button.value():
        if not button_pressed:
            #led.value(not led.value())
            led.toggle()
            button_pressed = True  
    else:
        button_pressed = False  
    sleep_ms(10)