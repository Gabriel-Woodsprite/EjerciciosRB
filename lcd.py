import RPi.GPIO as GPIO
import time

# Configuración de pines
LCD_RS = 26
LCD_E  = 19
LCD_D4 = 13
LCD_D5 = 6
LCD_D6 = 5
LCD_D7 = 11

LCD_WIDTH = 16     # 16 caracteres
LCD_CHR = True
LCD_CMD = False

LCD_LINE_1 = 0x80  # Dirección DDRAM línea 1
LCD_LINE_2 = 0xC0  # Dirección DDRAM línea 2

def lcd_low_nibble(bits):
    GPIO.output(LCD_D4, bool(bits & 0x01))
    GPIO.output(LCD_D5, bool(bits & 0x02))
    GPIO.output(LCD_D6, bool(bits & 0x04))
    GPIO.output(LCD_D7, bool(bits & 0x08))
    lcd_toggle_enable()


def lcd_init():
    lcd_low_nibble(0x03)
    time.sleep(0.005)

    lcd_low_nibble(0x03)
    time.sleep(0.005)

    lcd_low_nibble(0x03)
    time.sleep(0.001)

    lcd_low_nibble(0x02)  # switch to 4-bit mode

    lcd_byte(0x28, LCD_CMD)  # Function set: 4-bit, 2 lines
    lcd_byte(0x0C, LCD_CMD)  # Display ON
    lcd_byte(0x06, LCD_CMD)  # Entry mode
    lcd_byte(0x01, LCD_CMD)  # Clear
    time.sleep(0.005)


def lcd_byte(bits, mode):
    GPIO.output(LCD_RS, mode)

    # High nibble
    GPIO.output(LCD_D4, bool(bits & 0x10))
    GPIO.output(LCD_D5, bool(bits & 0x20))
    GPIO.output(LCD_D6, bool(bits & 0x40))
    GPIO.output(LCD_D7, bool(bits & 0x80))
    lcd_toggle_enable()

    # Low nibble
    GPIO.output(LCD_D4, bool(bits & 0x01))
    GPIO.output(LCD_D5, bool(bits & 0x02))
    GPIO.output(LCD_D6, bool(bits & 0x04))
    GPIO.output(LCD_D7, bool(bits & 0x08))
    lcd_toggle_enable()

def lcd_toggle_enable():
    time.sleep(0.0005)
    GPIO.output(LCD_E, True)
    time.sleep(0.0005)
    GPIO.output(LCD_E, False)
    time.sleep(0.0005)

def lcd_string(message):
    message = message.ljust(16, " ")
    for i in message:
        lcd_byte(ord(i), LCD_CHR)

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(LCD_RS, GPIO.OUT)
GPIO.setup(LCD_E, GPIO.OUT)
GPIO.setup(LCD_D4, GPIO.OUT)
GPIO.setup(LCD_D5, GPIO.OUT)
GPIO.setup(LCD_D6, GPIO.OUT)
GPIO.setup(LCD_D7, GPIO.OUT)

lcd_init()

lcd_byte(LCD_LINE_1, LCD_CMD)
lcd_string("Callateeeeee")
lcd_byte(LCD_LINE_2, LCD_CMD)
lcd_string("Los Ojos")
