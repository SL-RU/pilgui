import lcd_interface as l
import time
from PIL import ImageFont, Image, ImageDraw
from threading import Thread
import hardware
         

gui = l.GUI()

#init gui
hardware.Init()

#here goes buttons pins. Customize ass you wish.
button_pins = [21, 19, 23, 26, 18, 13, 11, 16, 15]

#Led's pins.
#Customize as you wish
led_pins = [24, 22]

#init buttons
buttons = []
for i in range(len(button_pins)):
    buttons.append(hardware.GPIOButton(button_pins[i]))
#init leds
leds = []
for i in range(len(led_pins)):
    leds.append(hardware.GPIOLed(led_pins[i]))
#set leds
leds[0].set(False)
leds[1].set(False)
#set second led as indicator
hardware.SetIndLed(leds[1])



font = ImageFont.truetype('FreeSans.ttf', 10)
lst = l.ListBox("b", [128, 48], gui, font=font, lpos=[0,5])
gui.add_element(lst)


font = ImageFont.truetype('FreeSans.ttf', 10)
lb = l.Lable("l", "pilgui developed by SL_RU! YES! THIS THING IS WORKiNG! ДА! УРА! Даже РУССКИЙ!443321", [64, -1], gui, font=font, lpos=[64,53], static_lable=False, margin=0)
gui.add_element(lb)
lst.click_action = lambda x: lb.set_text(x[1])

tm = l.Lable("t", "3:55/44:34", [64, -1], gui, bgcolor=1, textcolor=0, font=font, lpos=[0,53], static_lable=True, margin=0)
gui.add_element(tm)

im = l.ImageView("bt", Image.open("bti.png"), gui)
gui.add_element(im)



def draw_update():
    while True:
        gui.draw()

du = Thread(target=draw_update)
du.setDaemon(True)
du.start()


thr_hardware = Thread(target=hardware.Update)
thr_hardware.setDaemon(True)
thr_hardware.start()

ev = [[lambda:gui.input("up"), lambda:gui.input("back")],
      [lambda:gui.input("ok"), lambda:gui.input("ok")],
      [lambda:gui.input("down"), lambda:gui.input("forw")],
      [lambda:gui.input("info"), lambda:gui.input("set")]]

for i in range(len(ev)):
    buttons[i].click = ev[i][0]
    buttons[i].press = ev[i][1]

def inp():
    while True:
        i = input()
        if i is "q":
            gui.oled.onoff(0)
            break
        else:  
            lst.add_item(None, i)

di = Thread(target=inp)
di.setDaemon(True)
di.start()
di.join()


gui.oled.onoff(0)