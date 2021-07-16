#!/usr/bin/env python3
# import
import RPi.GPIO as GPIO
import time
import random

# Define GPIO to LCD mapping
LCD_RS = 21
LCD_E = 20
LCD_D4 = 16
LCD_D5 = 12
LCD_D6 = 25
LCD_D7 = 24

# Define some device constants
LCD_WIDTH = 16  # Maximum characters per line
LCD_CHR = True
LCD_CMD = False

LCD_LINE_1 = 0x80  # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0  # LCD RAM address for the 2nd line

# Timing constants
E_PULSE = 0.0005
E_DELAY = 0.0005

# Main program block
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)  # Use BCM GPIO numbers
GPIO.setup(LCD_E, GPIO.OUT)  # E
GPIO.setup(LCD_RS, GPIO.OUT)  # RS
GPIO.setup(LCD_D4, GPIO.OUT)  # DB4
GPIO.setup(LCD_D5, GPIO.OUT)  # DB5
GPIO.setup(LCD_D6, GPIO.OUT)  # DB6
GPIO.setup(LCD_D7, GPIO.OUT)  # DB7



def main():
    # Initialise display
    lcd_init()

    while True:
        # Send some test
        lcd_string("Activity Tracker", LCD_LINE_1)
        lcd_string("Partner with L&R", LCD_LINE_2)
        time.sleep(3)

        x = 0
        while x < 30:

            rndn = random.randint(0,1)  # randint and random needs to be changed to getting the recognized label by the MLA
            if rndn == 0:
                lcd_byte(0x01, LCD_CMD)
                lcd_string("Idle", LCD_LINE_1)
            elif rndn == 1:
                lcd_byte(0x01, LCD_CMD)
                lcd_string("Walking", LCD_LINE_1)
            elif rndn == 2:
                lcd_byte(0x01, LCD_CMD)
                lcd_string("Running", LCD_LINE_1)
            time.sleep(10)
            x = x + 1
        break

def display_state(state):
    # Initialise display
    lcd_init()
    lcd_string("Activity Tracker", LCD_LINE_1)
    lcd_string("Partner with L&R", LCD_LINE_2)
    time.sleep(3)
    if state == 0:
        lcd_byte(0x01, LCD_CMD)
        lcd_string("Idle", LCD_LINE_1)
    elif state == 1:
        lcd_byte(0x01, LCD_CMD)
        lcd_string("Walking", LCD_LINE_1)
    elif state == 2:
        lcd_byte(0x01, LCD_CMD)
        lcd_string("Running", LCD_LINE_1)
    time.sleep(5)

def lcd_init():
    # Initialise display
    lcd_byte(0x33, LCD_CMD)  # 110011 Initialise
    lcd_byte(0x32, LCD_CMD)  # 110010 Initialise
    lcd_byte(0x06, LCD_CMD)  # 000110 Cursor move direction
    lcd_byte(0x0C, LCD_CMD)  # 001100 Display On,Cursor Off, Blink Off
    lcd_byte(0x28, LCD_CMD)  # 101000 Data length, number of lines, font size
    lcd_byte(0x01, LCD_CMD)  # 000001 Clear display
    time.sleep(E_DELAY)


def lcd_byte(bits, mode):
    # Send byte to data pins
    # bits = data
    # mode = True  for character
    #        False for command

    GPIO.output(LCD_RS, mode)  # RS

    # High bits
    GPIO.output(LCD_D4, False)
    GPIO.output(LCD_D5, False)
    GPIO.output(LCD_D6, False)
    GPIO.output(LCD_D7, False)
    if bits & 0x10 == 0x10:
        GPIO.output(LCD_D4, True)
    if bits & 0x20 == 0x20:
        GPIO.output(LCD_D5, True)
    if bits & 0x40 == 0x40:
        GPIO.output(LCD_D6, True)
    if bits & 0x80 == 0x80:
        GPIO.output(LCD_D7, True)

    # Toggle 'Enable' pin
    lcd_toggle_enable()

    # Low bits
    GPIO.output(LCD_D4, False)
    GPIO.output(LCD_D5, False)
    GPIO.output(LCD_D6, False)
    GPIO.output(LCD_D7, False)
    if bits & 0x01 == 0x01:
        GPIO.output(LCD_D4, True)
    if bits & 0x02 == 0x02:
        GPIO.output(LCD_D5, True)
    if bits & 0x04 == 0x04:
        GPIO.output(LCD_D6, True)
    if bits & 0x08 == 0x08:
        GPIO.output(LCD_D7, True)

    # Toggle 'Enable' pin
    lcd_toggle_enable()


def lcd_toggle_enable():
    # Toggle enable
    time.sleep(E_DELAY)
    GPIO.output(LCD_E, True)
    time.sleep(E_PULSE)
    GPIO.output(LCD_E, False)
    time.sleep(E_DELAY)


def lcd_string(message, line):
    # Send string to display

    message = message.ljust(LCD_WIDTH, " ")

    lcd_byte(line, LCD_CMD)

    for i in range(LCD_WIDTH):
        lcd_byte(ord(message[i]), LCD_CHR)

if __name__ == '__main__':

    try:
        main()
    except KeyboardInterrupt:
        pass
    finally:
        lcd_byte(0x01, LCD_CMD)
        lcd_string("Goodbye!", LCD_LINE_1)
        GPIO.cleanup()