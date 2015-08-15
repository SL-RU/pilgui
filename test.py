import lcd_interface as l
import time
from PIL import ImageFont, Image, ImageDraw

gui = l.GUI()
font = ImageFont.truetype('FreeSans.ttf', 12)


lb = l.Lable("l", "pilgui developed by SL_RU! YES! THIS THING IS WORKiNG! ДА! УРА! Даже РУССКИЙ!443321", [118, -1], gui, bgcolor=1, textcolor=0, font=font, lpos=[5,0])
gui.add_element(lb)

gui.draw()

font = ImageFont.truetype('FreeSans.ttf', 9)
lq = l.Lable("l", "Paul Rothman - It's Such a Good Night (OST Breaking Bad).mp3", [128, -1], gui, bgcolor=0, textcolor=1, font=font, lpos=[0,lb.size[1] + 5])
gui.add_element(lq)

while True:
    gui.draw()
