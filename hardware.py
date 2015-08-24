__author__ = 'SL_RU'

import RPi.GPIO as GPIO
import time
from threading import Thread

##Взаимодействие с gpio, блютус и прочим хардваре
IS_GPIO = True

def Init():
    global thread
    if(IS_GPIO):
        GPIO.setmode(GPIO.BOARD)
    thread = Thread(target=Update)
    thread.setDaemon(True)
    thread.start()
def Exit():
    if(IS_GPIO):
        GPIO.cleanup()
elements = []
def Update():
    global elements
    while True:
        for e in elements:
            e.Update()
        time.sleep(0.01)
def AddElement(el):
    global elements
    elements.append(el)
def RemoveElemment(el):
    global elements
    elements.remove(el)

ind_led = None
def PressIndicate():
    global ind_led
    if (ind_led is not None):
        ind_led.blink(0.1)

def SetIndLed(led):
    global ind_led
    ind_led = led
class GPIOButton(object):
    def __init__(self, pin):
        if(IS_GPIO):
            GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        self.pin = pin
        AddElement(self)
    pin = 0
    last_state = 0
    press_count = 0
    SHORT_press_count = 15
    LONG_press_count = 150
    DELAY_count=50
    delay_count=0
    def Update(self):
        if(self.delay_count > 0):
            self.delay_count -= 1
        else:
            st = False
            if(IS_GPIO):
                st = GPIO.input(self.pin)
                #print(st)
            if(st):
                self.press_count += 1
                if (self.press_count == self.SHORT_press_count):
                    PressIndicate()
                elif self.press_count > self.LONG_press_count:
                    PressIndicate()
            else:
                c = self.press_count
                self.press_count = 0
                if(c >= self.SHORT_press_count):
                    if(c > self.LONG_press_count):
                        if(self.press != None):
                            self.press()
                    else:
                        if(self.click != None):
                            self.click()
                    self.delay_count = self.DELAY_count
    press = None
    click = None

class GPIOLed(object):
    def __init__(self, pin):
        if(IS_GPIO):
            GPIO.setup(pin, GPIO.OUT, pull_up_down=GPIO.PUD_UP)
        self.pin = pin
        AddElement(self)

    pin = 0
    
    blink_dur = 0
    blink_start_time = -100

    def set(self, state):
        GPIO.output(self.pin, not state)

    def blink(self, dur):
        self.blink_dur = dur
        self.blink_start_time = time.time()

    def Update(self):
        if self.blink_dur > 0:
            if self.blink_start_time + self.blink_dur >= time.time():
                self.set(True)
            else:
                self.set(False)
                self.blink_dur = 0
