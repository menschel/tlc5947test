# tlc5947test
Python3 Driver for TLC5947 LED Driver Chip

## what works
Some basic test functions. Tested on Raspberry Pi 3 with Adafruit 1429 Breakout Board.

## some background
The Chip does not really work as you would expect from an SPI device. It doesn't have control registers but only an output latch register.
Multiple chips can be daisy-chained together by combining the dout of Chip #n with din of chip #n+1 thus concat the two latch registers together.
A separate pin is used to latch the previous written values to the output drivers.

## RPI pins used
'''
Vcc = 3.3V or 5V (RGB Leds need 3,2V thus 5V is the better choice)
GND 
SPI Clock (Pin 23) to CLK of TLC5947
SPI MOSI (Pin 19) to DIN of TLC5947
GPIO 25 (PIN 22) to LATCH of TLC5947
'''
## further info found
'''
https://pinout.xyz/pinout/spi
https://learn.adafruit.com/tlc5947-tlc59711-pwm-led-driver-breakout
'''

