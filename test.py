import lcd_interface as l
import time
from PIL import ImageFont, Image, ImageDraw
from threading import Thread

gui = l.GUI()
font = ImageFont.truetype('FreeSans.ttf', 12)


lb = l.Lable("l", "pilgui developed by SL_RU! YES! THIS THING IS WORKiNG! ДА! УРА! Даже РУССКИЙ!443321", [118, -1], gui, bgcolor=1, textcolor=0, font=font, lpos=[5,0], static_lable=True)
gui.add_element(lb)

gui.draw()

font = ImageFont.truetype('FreeSans.ttf', 9)
lq = l.Lable("l", "Paul Rothman - It's Such a Good Night (OST Breaking Bad).mp3", [128, -1], gui, bgcolor=0, textcolor=1, font=font, lpos=[0,lb.size[1] + 5])
gui.add_element(lq)

def draw_update():
    while True:
        gui.draw()

du = Thread(target=draw_update)
du.setDaemon(True)
du.start()

def inp():
    while True:
        i = input()
        if i is not "q":
            lq.set_text(i)
        else:
            gui.oled.onoff(0)
            break

di = Thread(target=inp)
di.setDaemon(True)
di.start()
di.join()


gui.oled.onoff(0)