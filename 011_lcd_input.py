from machine import I2C, Pin
from i2c_lcd import I2cLcd
import sys

lcd = I2cLcd(I2C(0), 0x27, 2, 16)
lcd.putstr("Ready...")

while True:
    try:
        input_data = input()
        input_data = input_data.strip()

        if input_data.startswith("1:"):
            lcd.move_to(0, 0)
            lcd.putstr(" " * 16)
            
            lcd.move_to(0, 0)
            lcd.putstr(input_data[2:18])  
        
        elif input_data.startswith("2:"):
            lcd.move_to(0, 1)
            lcd.putstr(" " * 16)
            
            lcd.move_to(0, 1)
            lcd.putstr(input_data[2:18])
            
        else:
            print("Invalid input. Use '1:message' or '2:message'.")
            
    except KeyboardInterrupt:
        print("\nExiting...")
        sys.exit()