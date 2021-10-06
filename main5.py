import tkinter as tk
from PIL import Image, ImageTk

XS, YS = 5, 5
canvas = None

clicked_pos = (-1, -1)

def ImgSplit(im, scale=1.0):
    im = im.resize(((int)(im.height * scale), (int)(im.width * scale)))
    height = im.height / YS
    width = im.width / XS

    buff = []
    for h1 in range(YS):
        for w1 in range(XS):
            w2 = w1 * height
            h2 = h1 * width
            c = im.crop((w2, h2, width + w2, height + h2))
            buff.append(c)

    return buff, height, width

def callback(ev, height, width, split_height, split_width, XS, YS, scale, photo_image):
    global clicked_pos
    print(ev.x, ev.y)
    x = ev.x // (width * scale / XS)
    y = ev.y // (height * scale / YS)
    print('{}{}'.format((int)(x), (int)(y)))
    if clicked_pos[0] == -1 and clicked_pos[1] == -1:
        clicked_pos = ((int)(x), (int)(y))
    else:
        width = split_width * j + (split_width // 2)
        height = split_height * i + (split_height // 2)
        canvas.create_image(width, height, image=photo_image[i*YS+j], tag='img{}{}'.format(j, i))
        canvas.delete('img{}{}'.format((int)(x), (int)(y)))

class Application(tk.Frame):
    def __init__(self, master = None):
        super().__init__(master)
        global canvas

        img = Image.open('./getimg.png')
        scale = 0.5
        imgs, split_height, split_width = ImgSplit(img, scale)

        self.master.title("画像の表示")
        self.master.geometry("{}x{}".format(img.width, img.height))

        canvas = tk.Canvas(self.master, width=img.width, height=img.height)

        self.photo_image = []
        for i in range(YS):
            for j in range(XS):
                self.photo_image.append(ImageTk.PhotoImage(imgs[i*YS+j]))

                width = split_width * j + (split_width // 2)
                height = split_height * i + (split_height // 2)
                canvas.create_image(width, height, image=self.photo_image[i*YS+j], tag='img{}{}'.format(j, i))
                print('{}{}'.format(i, j))
        canvas.pack()
        canvas.bind("<ButtonPress-1>", lambda ev: [callback(ev, img.height, img.width, split_height, split_width, XS, YS, scale, self.photo_image)])

if __name__ == "__main__":
    root = tk.Tk()
    app = Application(master = root)
    app.mainloop()
