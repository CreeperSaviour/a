import numpy as np
import tkinter as tk
from PIL import Image, ImageTk

XS, YS = 3, 2

def ImgSplit(im):
    result = [[None] * XS for i in range(YS)]
    height = im.height / YS
    width = im.width / XS
    buff = []
    for h1 in range(YS):
        for w1 in range(XS):
            w2 = w1 * height
            h2 = h1 * width
            c = im.crop((w2, h2, width + w2, height + h2))
            result[h1][w1] = c
    return result

def callback(ev):
    for i in range(len(canvas)):
        for j in range(len(canvas[i])):
            if canvas[i][j] == ev.widget:
                print((i, j))

img = Image.open("./getimg.png")
imgs = ImgSplit(img)

print("img", type(img))
print("imgs", type(imgs[0][0]))

root = tk.Tk()
print("width, height", img.width, img.height)
root.geometry("{}x{}".format(img.width, img.height))

frame = tk.Frame(root, width=1280, height=1280)
frame.grid(row=0, column=0, sticky=(tk.N,tk.S,tk.E,tk.W))

colors = [["#fffafa", "#ffe4b5", "#e6e6fa"], ["#696969", "#778899", "#bebebe"]]
canvas = [[None] * len(colors[0]) for i in range(len(colors))]

# for i in range(len(canvas)):
#     for j in range(len(canvas[i])):
#         canvas[i][j] = tk.Canvas(frame, bg=colors[i][j])
#         canvas[i][j].create_image(0, 0, image=ImageTk.PhotoImage(imgs[i][j]))
#         canvas[i][j].grid(column=j, row=i)
#         canvas[i][j].bind("<ButtonPress-1>", callback)

new_canvas = tk.Canvas(frame, width=2000, height=2000)
# tmp = tk.Image(img)
tmp = ImageTk.PhotoImage(file="./getimg.png", width=1280)
new_canvas.create_image(0, 0, image=tmp)
new_canvas.grid(column=0, row=3)
root.mainloop()
