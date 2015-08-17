from lib_oled96 import ssd1306
from PIL import Image
from smbus import SMBus
from time import sleep

def sum_pos(pos1, pos2):
    return [a+b for (a,b) in zip(pos1, pos2)]


class GUI(object):
    def __init__(self):
        self.i2cbus = SMBus(1)        # 1 = Raspberry Pi but NOT early REV1 board
        self.oled = ssd1306(self.i2cbus)   # create oled object, nominating the correct I2C bus, default address
        self.canvas = self.oled.canvas
        self.root = RootElement("root", [128, 64], self)
        self.cls()


    i2cbus = None
    oled = None
    canvas = None
    root = None

    def _display(self):
        self.oled.display()

    def cls(self):
        self.oled.cls()

    def draw(self):
        self.root.draw(self.canvas)
        self._display()

    def set_input_element(self, el):
        pass

    def add_element(self, el):
        self.root.add_child(el)    


class Element(object):
    def __init__(self, id, size, gui, lpos = [0,0]):
        self.id = id
        self.size = size
        self.localpos = lpos
        self.gui = gui
        

    id = ""
    type = "none" #element type
    gparent = None 
    children = list()
    localpos = [0, 0] #position relative to parent
    size = [20,20]
    focusable = False #is element focusable
    focused = False   #is element in focus
    is_input = False  #is element required in input
    input_type = ""   #what type of input is element required in
    gui = None
    

    def get_global_pos(self):
        if self.gparent is not None:
            return [a+b for (a,b) in zip(self.gparent.get_global_pos(), self.localpos)]
        else:
            return self.localpos

    def set_global_pos(self, pos):
        if self.gparent is not None:
            self.localpos = [a-b for (a,b) in zip(pos,self.gparent.get_global_pos())]
        else:
            self.localpos = pos

    def set_size(self, sz):
        self.size = sz        
            
    def add_child(self, child):
        print("id: " + str(self.id) + " adding child " + str(child.id))
        self.children.append(child)
        child.gparent = self

    def remove_child(self, child):
        self.children.remove(child)
        child.gparent = None

    def draw(self, canvas):
        """
        Calling by parent.
        canvas - ImageDraw element
        """    
        self.draw_self(canvas) 
        self.draw_children(canvas)

    def draw_self(self, canvas):
        """
        Here goes drawing function for this element.
        canvas - ImageDraw element, where you need to paint smth.
        """
        print("empty draw: " + self.id)
        
    def draw_children(self, canvas):
        for i in self.children:
            i.draw(canvas)

    def focus_next(self, f):
        pass

    def input(self, i):
        pass


class RootElement(Element):

    children = list()
    
    def get_global_pos(self):
        return [0,0]

    def set_global_pos(self, pos):
        pass

    def draw_self(self, canvas):
        canvas.rectangle([0,0] + self.size, fill = 0, outline = 0)


class Lable(Element):
    def __init__(self, id, txt, size, gui, bgcolor=None, textcolor=1, outlinecolor=None, margin=1, font = None, lpos = [0,0], static_lable = False):
        """
        txt - text to show
        size - max size of element. If some dimension is -1, then it will be autosetted.
        font - ImageFont object
        static_lable - if true - do not check text suitability and do not get running strip(much faster drawing)
        """
        self.id = id
        self.size = size
        self.localpos = lpos
        self.gui = gui
        self.bgcolor = bgcolor
        self.outlinecolor = outlinecolor
        self.textcolor = textcolor
        self.font = font
        self.margin = margin
        self.set_text(txt)
        self.static_lable = static_lable
        

    type = "lable" #element type
    focusable = False #is element focusable
    focused = False   #is element in focus
    is_input = False  #is element required in input
    bgcolor = None
    outlinecolor=None
    textcolor = 1
    font = None
    txt = ""
    margin = 1        #distance between border and text
    static_lable = False #do not check text suitability and do not get running strip
    children = list()
    
    _cur_pos = 0
    _max_len = -1
    _string_cache = dict()
    _new_txt = None
    _new_font = None
    _text_suitable = False
    _text_suitable_checked = False

    def set_size(self, size):
        self.size = size
        self._max_len = -1
        self._text_suitable = False
        self._text_suitable_checked = False

    def set_text(self, text):
        self._new_txt = text
        self._text_suitable = False
        self._text_suitable_checked = False
        self._cur_pos = 0

    def set_font(self, font):
        self._max_len = -1
        self._string_cache = dict()
        self._new_font = font
        self._text_suitable = False
        self._text_suitable_checked = False

    def _autoset_size(self, canvas):
        s = None
        if self.size[0] is -1:
            s = canvas.textsize(self.txt, self.font)
            self.size[0] = s[0] + self.margin*2
        if self.size[1] is -1:
            if s is None:    
                s = canvas.textsize(self.txt, self.font)
            self.size[1] = s[1] + self.margin*2

    def _count_string_size(self, canvas, string):
        if string in self._string_cache:
            return self._string_cache[string]
        else:
            a = canvas.textsize(string, self.font)[0]
            self._string_cache[string] = a
            return a
                
    def _get_string_to_show_HIGH_LEVEL(self, canvas):
        """
        THIS IS ARE VERY SLOW ALGORYTHM(but it doesn't makes mistakes'). USE THE FUNCTION BELOW!
        Some strings are wider then label size. In that case label becoming an running strip. This function counts an string, that need show right now.
        """
        if len(self.txt) == 0:
            return " "
        t = ""
        if self._cur_pos >= 0 and self._cur_pos  < len(self.txt):
            t += self.txt[self._cur_pos]
        else:
            self._cur_pos = 0
        d = True
        p = self._cur_pos
        tx = t
        while self._count_string_size(canvas, t) + self.margin*2 < self.size[0]:
            tx = t
            if(d):
                if p - 1 >= 0:
                    p-=1
                    t = self.txt[p]+t
                else:
                    d = False
                    p = self._cur_pos
            else:
                if p + 1 < len(self.txt):
                    p+=1
                    t += self.txt[p]
                else:
                    return self.txt
        return tx

    def _count_max_average_len(self, canvas):
        char = "w"
        t = char
        tx = ""
        while canvas.textsize(t, self.font)[0] + self.margin*2 < self.size[0]:
            tx = t
            t += char
        return len(tx)
            
    def _get_string_to_show_LOW_LOVEL(self, canvas):
        """
        Some strings are wider then label size. In that case label becoming an running strip. This function counts an string, that need show right now.
        """
        if len(self.txt) == 0:
            return " "
        t = ""
        if self._cur_pos >= 0 and self._cur_pos  < len(self.txt):
            t += self.txt[self._cur_pos]
        else:
            self._cur_pos = 0

        if self._max_len == -1:
            self._max_len = self._count_max_average_len(canvas)

        b = max(0, self._cur_pos - self._max_len)
        print("b: " + str(b))
        e = min(b + self._max_len, len(self.txt))
        print("e: " + str(e))
        t = self.txt[b:e]
        return t
        
    def _get_string_to_show(self, canvas):
        """Here you need choose one of them"""    
        return self._get_string_to_show_HIGH_LEVEL(canvas)
        
    def draw(self, canvas):
        #values can be changed from other thread
        if self._new_txt is not None:
            self.txt = self._new_txt
            self._new_txt = None
            self._cur_pos = 0
        if self._new_font is not None:
            self.font = self._new_font
            self._new_font = None

        #count dimensions with -1 value
        if self.size[0] is -1 or self.size[1] is -1:
            self._autoset_size(canvas)

        #draw background and border
        gp = self.get_global_pos()
        if (self.bgcolor is not None or self.outlinecolor is not None):
            canvas.rectangle(gp + sum_pos(gp, self.size), fill = self.bgcolor, outline=self.outlinecolor)

        t = self.txt
        if (not self._text_suitable or not self._text_suitable_checked) and not self.static_lable:
            t = self._get_string_to_show(canvas)
            if self._cur_pos == 0:
                self._cur_pos = max(len(t) - 5, 0)
            else:
                self._cur_pos += 2
                
            if not self._text_suitable_checked:
                if len(t) == len(self.txt):
                    self._text_suitable = True
                else:
                    if not t.endswith("     "):
                        t += "     "
        canvas.text(sum_pos(gp, [self.margin, self.margin]), t, fill=self.textcolor, font = self.font)

class ListBox(Element):
    def __init__(self, id, size, gui, font=None, select_action=None, click_action=None, direction=1, lpos = [0,0]):
        """
        Listbox element. Displaying items vertically. With order by priority.
        direction - if == -1, then up to bottom, if 1, then from bottom.
        select_action - function exec when select changed. In arguments: this_listbox_element, selected_item_id, selected_item_text
        click_action - function exec when select changed. In arguments: this_listbox_element, selected_item_id, selected_item_text
        
        """
        self.id = id
        self.size = size
        self.localpos = lpos
        self.gui = gui
        self.font = font
        self.select_action = select_action
        self.click_action = click_action



    font = None
    items = list()          #list with elements in list box:
                            #item in list is [id, element`s_text, priority]
    select_action = None    #event function execs when select changed. In arguments: this_listbox_element, selected_item_id, selected_item_text
    click_action = None     #event function execs when select changed. In arguments: this_listbox_element, selected_item_id, selected_item_text
    selected_id = 0
    children = list()
    _updated = True         #if something updated and need redraw 
    
    def add_item(self, id, text, priority=0):
        """
        returns array [id, text, priority]
        id must be unique! If you don't know wich to choose set None.'
        """
        mid = 0
        for i in self.items:
            if id is None:
                if isinstance(i[0], int):
                    mid = max(i[0], mid)
            else:
                if id == i[0]:
                    raise KeyError()
        if id is None:
            id = mid

        r = [id, text, priority]
        self.items.append(r)
        return r

    

    def draw_children(self, canvas):
        if len(self.children) == 0:
            lb = Lable(0, "0", [self.size[0]-2, -1], self.gui, bgcolor=0, outlinecolor=1, textcolor=1, font=self.font)
            self.add_child(lb)
            lb.draw(canvas)
            h = lb.size[1]
            count = int(self.size[1]/h)
            dist = (self.size[1] - count * h)/ count
            for i in range(1, count):
                lb = Lable(i, str(i), [self.size[0]-2, -1], self.gui, outlinecolor=1, bgcolor=0, textcolor=1, font=self.font, lpos=[0, dist + lb.localpos[1] + h])
                self.add_child(lb)
                lb.draw(canvas)
        else:
            ind = 0
            for i in self.children: 
                if ind < len(self.items):
                    i.set_text(self.items[ind][1])
                else:               
                    i.set_text(str(ind))
                i.draw(canvas)
                ind += 1

    def draw_self(self, canvas):
        gp = self.get_global_pos()
        canvas.rectangle(gp + sum_pos(gp, self.size), fill = 0, outline=1)
        canvas.rectangle([gp[0] + self.size[0]-2, gp[1]+6, gp[0] + self.size[0]-1, gp[1] + 23], fill = 0, outline=1)