import tkinter
from PIL import Image, ImageTk

window = tkinter.Tk()
window.geometry("1000x1000")

def resize(img):
    height, width = img.height, img.width
    max_size = max(height, width)
    rate = 1.0
    if max_size >= 500:
        rate = 500 / max_size
    img = img.resize(((int)(height * rate), (int)(width * rate)))
    print(img.height, img.width)
    return img

img = Image.open('getimg.png')
img = resize(img)
img = ImageTk.PhotoImage(img)

img2 = Image.open('mountain10-4.png')
img2 = resize(img2)
img2 = ImageTk.PhotoImage(img2)

canvas = tkinter.Canvas(width=img.width() * 2, height=img.height() * 2)
canvas.grid(row=0, column=0)

for i in range(4):
    j = i // 2
    print(i % 2, j)
    canvas.create_image((i % 2) * img.height(), j * img.width(), image=img, anchor=tkinter.NW)

window.mainloop()