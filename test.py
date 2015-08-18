import lcd_interface as l
import time
from PIL import ImageFont, Image, ImageDraw
from threading import Thread

# -*- coding: utf-8 -*-

gui = l.GUI()
font = ImageFont.truetype('FreeSans.ttf', 8)


lb = l.Lable("l", "pilgui developed by SL_RU! YES! THIS THING IS WORKiNG! ДА! УРА! Даже РУССКИЙ!443321", [118, -1], gui, bgcolor=1, textcolor=0, font=font, lpos=[5,0], static_lable=False)
gui.add_element(lb)

gui.draw()

font = ImageFont.truetype('FreeSans.ttf', 10)
lst = l.ListBox("b", [127, 64 - lb.size[1] - 3], gui, font=font, lpos=[0,lb.size[1] + 3])
gui.add_element(lst)

def draw_update():
    while True:
        gui.draw()

du = Thread(target=draw_update)
du.setDaemon(True)
du.start()

def inp():
    while True:
        i = input()
        if i is "q":
            gui.oled.onoff(0)
            break
        elif i is "8":
            lst.selected_id += 1
        elif i is "2":
            lst.selected_id = max(0, lst.selected_id - 1)
        else:  
            lst.add_item(None, i)

di = Thread(target=inp)
di.setDaemon(True)
di.start()
di.join()


gui.oled.onoff(0)