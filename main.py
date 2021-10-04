
"""
toy.py

July 08, 2005
"""
import tkinter as Tk
import random as R
import math



TITLE_COLOER = '#FF6600'
COLOR = ['red', 'gold', 'blue']
TITLE_FONT = ('Helvetica', '20', 'bold')
CAPPING = [u'あさがお', u'おけ', u'けいと', u'とり', u'リス', u'スイカ', u'かき', u'きもの', u'のはら']
SQRT3 = math.sqrt(3)


class CanvasItem:
    canvas = None

    def make_binds(self):
        CanvasItem.canvas.tag_bind(self.id, '<1>', self.drag_start)
        CanvasItem.canvas.tag_bind(self.id, '<Button1-Motion>', self.dragging)

    def drag_start(self, event):
        self.x = event.x
        self.y = event.y

    def dragging(self, event):
        x1 = event.x
        y1 = event.y
        CanvasItem.canvas.move(self.id, x1-self.x, y1-self.y)
        self.x = x1
        self.y = y1


class CanvasOval(CanvasItem):
    def __init__(self, x0, y0, x1, y1, **key):
        self.id = CanvasItem.canvas.create_oval(x0, y0, x1, y1, **key)
        self.make_binds()

class CanvasRectangle(CanvasItem):
    def __init__(self, x0, y0, x1, y1, **key):
        self.id = CanvasItem.canvas.create_rectangle(x0, y0, x1, y1, **key)
        self.make_binds()

class CanvasTriangle(CanvasItem):
    def __init__(self, x, y, r, color):
        self.id = CanvasItem.canvas.create_polygon(str(x)+'c', str(y-r*SQRT3)+'c', str(x-r)+'c', str(y)+'c',
                                                   str(x+r)+'c', str(y)+'c', fill=color)
        self.make_binds()

class CanvasText(CanvasItem):
    def __init__(self, *pos, **key):
        self.id = CanvasItem.canvas.create_text(*pos, **key)
        self.make_binds()

class CanvasCircleNumber(CanvasItem):
    def __init__(self, x, y, num, session):
        s = session + str(num)
        self.circle = CanvasItem.canvas.create_oval('%fc' % (x-0.7), '%fc' % (y-0.7), '%fc' % (x+0.7), '%fc' % (y+0.7),
                                                    width=2, outline='red', fill='#FFFFF0', tag=s)
        self.number = CanvasItem.canvas.create_text(str(x)+'c', str(y)+'c', text=str(num),
                                                    font=('Helvetica', '14', 'bold'), tag=s)
        CanvasItem.canvas.tag_bind(s, '<1>', self.drag_start)
        CanvasItem.canvas.tag_bind(s, '<Button1-Motion>', self.dragging)

    def dragging(self, event):
        x1 = event.x
        y1 = event.y
        CanvasItem.canvas.move(self.circle, x1-self.x, y1-self.y)
        CanvasItem.canvas.move(self.number, x1-self.x, y1-self.y)
        self.x = x1
        self.y = y1


class Frame (Tk.Frame):
    def __init__(self, master=None):
        Tk.Frame.__init__(self, master)
        self.master.title("Toy")
        self.master.geometry("+20+20")
        self.cvs = Tk.Canvas(self, scrollregion=("0c", "0c",  "40c",  "40c"), width="20c", height="20c",
                                   relief=Tk.SUNKEN, borderwidth=2, bg='#FFEFD5')
        self.cvs.grid(row=0, column=0, sticky= Tk.N+Tk.E+Tk.W+Tk.S)

        xscroll = Tk.Scrollbar(self, orient=Tk.HORIZONTAL, command=self.cvs.xview)
        xscroll.grid(row=1, column=0, sticky=Tk.E+Tk.W)

        yscroll = Tk.Scrollbar(self, orient=Tk.VERTICAL, command=self.cvs.yview)
        yscroll.grid(row=0, column=1, sticky=Tk.N+Tk.S)

        self.cvs.config(xscrollcommand=xscroll.set, yscrollcommand=yscroll.set)
        self.grid_rowconfigure(0, weight=1, minsize=0)
        self.grid_columnconfigure(0, weight=1, minsize=0)
        # assign a CanvasItem class parameter
        CanvasItem.canvas=self.cvs
        # binding
        self.cvs.bind('<3>', self.draw_start)
        self.cvs.bind('<Button3-Motion>', self.drawing)
        self.cvs.bind('<Double-Button-1>', self.delete_line)
        # Display a 2x2 rectangular grid.
        self.cvs.create_line('0c', '20c', '40c', '20c', width=2)
        self.cvs.create_line('20c', '0c', '20c', '40c', width=2)
        # First Toy
        self.cvs.create_text('10c', '1.5c', text=u'色別に整理して、しまいましょう。\n左ボタンドラッグで動きます。', font=TITLE_FONT, fill=TITLE_COLOER)
        for i, c in enumerate(COLOR):
            self.cvs.create_line('%dc' % (i*6+1), '16c', '%dc' % (i*6+1), '19c', '%dc' % (i*6+6), '19c', '%dc' % (i*6+6), '16c', fill=c, width=3)
        for i in range(5):
            x=R.randint(200, 1800) * 0.01
            y=R.randint(300, 1500) * 0.01
            r=R.randint(30, 150) * 0.01
            c=R.randint(0,2)
            CanvasOval('%fc' % (x-r), '%fc' % (y-r), '%fc' % (x+r), '%fc' % (y+r), fill=COLOR[c], width=0)
            for i in range(5):
                x=R.randint(100, 1700) * 0.01
                y=R.randint(300, 1500) * 0.01
                w=R.randint(50, 150) * 0.01
                h=R.randint(50, 150) * 0.01
                c=R.randint(0,2)
                CanvasRectangle('%fc' % (x), '%fc' % (y), '%fc' % (x+w), '%fc' % (y+h), fill=COLOR[c], width=0)
        # Second Toy
        self.cvs.create_text('30c', '1.5c', text=u'三角形を大きい順に並べましょう。\n左ボタンドラッグで動きます。', font=TITLE_FONT, fill=TITLE_COLOER)
        for i in range(10):
            x=R.randint(2200, 3800) * 0.01
            y=R.randint( 300, 1950) * 0.01
            r=R.randint(3000, 20000) * 0.0001
            c=R.randint(0,2)
            CanvasTriangle(x, y, r, COLOR[c])
        # Third Toy
        self.cvs.create_text('10c', '21.5c', text=u'数字を順番に線で結びましょう。\n右ボタンドラッグで線が引けます。', font=TITLE_FONT, fill=TITLE_COLOER)
        self.cvs.create_text('10c', '22.8c', text=u'数字が重なっていたら、ドラッグして位置を少しずらしましょう。', font=('Helveticla', '12'))
        for i in range(12):
            x=R.randint(200, 1800) * 0.01
            y=R.randint(2400, 3600) * 0.01
            CanvasCircleNumber(x, y, i+1, 'third')
        # Fourth Toy
        self.cvs.create_text('30c', '21.5c', text=u'「しりとり」になるように単語を線で結びましょう。\n' u'右ボタンドラッグで線が引けます。', font=TITLE_FONT, fill=TITLE_COLOER)
        self.cvs.create_text('30c', '22.8c', text=u'単語が重なっていたら、ドラッグして位置を少しずらしましょう。', font=('Helveticla', '12'))
        for txt in CAPPING:
            x=R.randint(2200, 3800) * 0.01
            y=R.randint(2400, 3600) * 0.01
            r=R.randint(0,200)
            g=R.randint(0,200)
            b=R.randint(0,200)
            CanvasText(str(x)+'c', str(y)+'c', text=txt, font=('Helvetica', '18', 'bold'), fill='#%02X%02X%02X' % (r, g, b))
        ###
    def draw_start(self, event):
        self.x = self.cvs.canvasx(event.x, '0.2m')
        self.y = self.cvs.canvasy(event.y, '0.2m')
    def drawing(self, event):
        x1 = self.cvs.canvasx(event.x, '0.2m')
        y1 = self.cvs.canvasy(event.y, '0.2m')
        self.cvs.create_line(self.x, self.y, x1, y1, width=2, fill='#CC3300', tag='line')
        self.x = x1
        self.y = y1
    def delete_line(self, event):
        self.cvs.delete('line')
        ##-----------------------------------------------------
if __name__ == '__main__':
    f = Frame()
    f.pack(fill=Tk.BOTH, expand=1)
    f.mainloop()
