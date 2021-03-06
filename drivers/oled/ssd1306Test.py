# Test the OLED shield featuring the SSD1306 display driver

import machine, time, ssd1306
import sys
from math import sin,cos,pi

print("Testing the ssd1306 OLED display")
print("Program written for the workshop on IoT at the")
print("African Internet Summit 2019")
print("Copyright: U.Raich")
print("Released under the Gnu Public License")
if sys.platform == "esp8266":
    print("Running on ESP8266")
    pinScl      =  5  #ESP8266 GPIO5 (D1
    pinSda      =  4  #ESP8266 GPIO4 (D2)
else:
    print("Running on ESP32") 
    pinScl      =  22  # SCL on esp32 
    pinSda      =  21  # SDA ON ESP32
    
addrOled    = 60  #0x3c

hSize       = 48  # Hauteur ecran en pixels | display heigh in pixels
wSize       = 64  # Largeur ecran en pixels | display width in pixels

oledIsConnected = False

# init ic2 object
i2c = machine.I2C(scl=machine.Pin(pinScl), sda=machine.Pin(pinSda)) #ESP8266 5/4

# Scan le bus i2c et verifie si le BME280 et l'ecran OLED sont connectes
# Scan i2c bus and check if BME2 and OLDE display are connected
print('Scan i2c bus...')
devices = i2c.scan()
if len(devices) == 0:
  print("No i2c device !")
else:
  print('i2c devices found:',len(devices))
  for device in devices: 
    if device == addrOled:
      oledIsConnected = True
      
def clear():
    oled.fill(0)

def testDrawLine():
    for i in range(0,wSize,4):
        oled.line(0,0,i,hSize-1,1)
        oled.show()
        time.sleep(0.1)
    for i in range(0,hSize,4):
        oled.line(0,0,wSize-1,hSize-i-4,1)
        oled.show()
        time.sleep(0.1)
        
def drawCircle(orig_x,orig_y,radius):
    for i in range(0,round(50*pi)+1):
        x = round(radius * cos(i/25)) + orig_x + wSize//2
        y = round(radius * sin(i/25)) + orig_y + hSize //2
        if x < wSize and y < hSize:
            oled.pixel(x,y,1)
        oled.show()
        
def testDrawRect():
    for i in range (0,hSize//2,2):
        oled.rect(i,i,wSize-2*i,hSize-2*i,1)
        oled.show()
        time.sleep(0.1)

def testFillRect():
    for i in range(0,hSize//2,3):
        oled.fill_rect(i,i,i*2,i*2,1)
        oled.show()
        time.sleep(0.1)
 
def drawSin():
    oled.hline(0,hSize//2,wSize,1)
    oled.vline(1,0,hSize,1)
    oled.show()
    for i in range(0,wSize):
        oled.pixel(i,round(-sin(2*pi*i/wSize)*hSize//2)+hSize//2,1)
        oled.show()
    oled.text("sin(x)",wSize//4,hSize//5,1)
    oled.show()
     
if oledIsConnected:
  oled = ssd1306.SSD1306_I2C(wSize, hSize, i2c, addrOled)
  oled.fill(0)
  testDrawLine()
  clear()
  testDrawRect()
  clear()
  testFillRect()
  clear()
  drawCircle(0,0,20)
  drawCircle(15,5,10)
  drawCircle(-10,-15,15)
  drawCircle(5,15,5)
  time.sleep(1)
  clear()
  drawSin()
   
else:
  print('! No i2c display')
time.sleep_ms(5000)
