from machine import Pin, I2C
from i2c_lcd import I2cLcd
from time import sleep_ms
from servo import Servo

SERVO_PIN = 19
DT_PIN = 16
CLK_PIN = 17
SW_PIN = 18
LCD_ADDR = 0x27
LCD_COLS = 16
LCD_ROWS = 2
SERVO_STEPS = 10

lcd = I2cLcd(I2C(0), LCD_ADDR, LCD_ROWS, LCD_COLS)
servo = Servo(SERVO_PIN) # Uncalibrated servo min and max duty cycle values are 1802 and 7864
servo.update_settings(servo_pwm_freq= 50,
                         min_u16_duty=1690, 
                         max_u16_duty=7980,
                         min_angle=0, 
                         max_angle=180, 
                         pin=SERVO_PIN)

servo_value = 90
dt = False
clk = False
clk_old = False
button_pressed = False

encoder_dt = Pin(DT_PIN, Pin.IN)
encoder_clk = Pin(CLK_PIN, Pin.IN)
encoder_sw = Pin(SW_PIN, Pin.IN)

def button_handler(pin):
    global button_pressed
    button_pressed = True

def update_lcd(angle):
    lcd.move_to(0, 0)
    lcd.putstr("Servo Angle:\n")
    
    lcd.move_to(0, 1)
    lcd.putstr("  {:3d} degrees".format(angle))

def constrain_value(val, min_val, max_val):
  return min(max_val, max(min_val, val))

servo.move(servo_value)
update_lcd(servo_value)
encoder_sw.irq(trigger=Pin.IRQ_FALLING, handler=button_handler)

while True:
    dt = encoder_dt.value()
    clk = encoder_clk.value()

    if clk != clk_old and clk == False:
        if clk != dt:
            servo_value = constrain_value(servo_value + SERVO_STEPS, 0, 180)
        if clk == dt:
            servo_value = constrain_value(servo_value - SERVO_STEPS, 0, 180)
        servo.move(servo_value)
        update_lcd(servo_value)
    clk_old = clk

    if button_pressed:
        servo_value = 90
        servo.move(servo_value)
        update_lcd(servo_value)
        button_pressed = False

    sleep_ms(1)