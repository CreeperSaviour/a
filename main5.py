import tkinter as tk
from PIL import Image, ImageTk
import numpy as np

XS, YS = 5, 5
canvas = None

clicked_pos = (-1, -1)

result = []

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

def left_click(ev, height, width, split_height, split_width, XS, YS, scale, photo_image):
    global clicked_pos
    x = (int)(ev.x / (width * scale / XS))
    y = (int)(ev.y / (height * scale / YS))
    print('{}{}'.format((int)(x), (int)(y)))
    if clicked_pos[0] == -1 and clicked_pos[1] == -1:
        clicked_pos = ((int)(x), (int)(y))
    else:
        x2, y2 = clicked_pos[0], clicked_pos[1]
        width, height = split_width * x + (split_width // 2), split_height * y + (split_height // 2)
        width_t, height_t = split_width * x2 + (split_width // 2), split_height * y2 + (split_height // 2)
        canvas.delete('img{}{}'.format(x, y))
        canvas.delete('img{}{}'.format(x2, y2))
        canvas.create_image(width, height, image=photo_image[y2*YS+x2], tag='img{}{}'.format(x, y))
        canvas.create_image(width_t, height_t, image=photo_image[y*YS+x], tag='img{}{}'.format(x2, y2))
        photo_image[y2*YS+x2], photo_image[y*YS+x] = photo_image[y*YS+x], photo_image[y2*YS+x2]
        result[y][x], result[y2][x2] = result[y2][x2], result[y][x]
        clicked_pos = (-1, -1)
        print(result)

def right_click(ev, height, width, split_height, split_width, XS, YS, scale, imgs, photo_image):
    x = (int)(ev.x / (width * scale / XS))
    y = (int)(ev.y / (height * scale / YS))
    width, height = split_width * x + (split_width // 2), split_height * y + (split_height // 2)
    # print(type(imgs[y*YS+x]))
    # img = ImageTk.PhotoImage(imgs[y*YS+x].rotate(90).convert('RGB'))
    # print(type(img))
    # print(imgs[y*YS+x])
    # print(photo_image[y*YS+x])
    # img = np.array(imgs[y*YS+x])
    # np.rot90(img)
    # img = Image.fromarray(img)
    # img = ImageTk.PhotoImage(img.convert('RGB'))
    canvas.delete('img{}{}'.format(x, y))
    # canvas.create_image(width, height, image=img, tag='img{}{}'.format(x, y))
    canvas.create_image(800, 800, image=photo_image[y*YS+x])
    result[y][x]["rotate"] = (result[y][x]["rotate"] + 1) % 4
    print(result)

class Application(tk.Frame):
    def __init__(self, master = None):
        super().__init__(master)
        global canvas

        img = Image.open('./getimg.png')
        scale = 0.5
        imgs, split_height, split_width = ImgSplit(img, scale)

        for i in range(YS):
            result.append([])
            for j in range(XS):
                c = {}
                c["pos"] = '{}{}'.format(j, i)
                c["rotate"] = 0
                result[i].append(c)

        self.master.title("画像の表示")
        self.master.geometry("{}x{}".format(img.width, img.height))

        canvas = tk.Canvas(self.master, width=img.width, height=img.height)

        self.photo_image = []
        for y in range(YS):
            for x in range(XS):
                self.photo_image.append(ImageTk.PhotoImage(imgs[y*YS+x]))

                width = split_width * x + (split_width // 2)
                height = split_height * y + (split_height // 2)
                canvas.create_image(width, height, image=self.photo_image[y*YS+x], tag='img{}{}'.format(x, y))
        canvas.pack()
        canvas.bind("<ButtonPress-1>", lambda ev: [left_click(ev, img.height, img.width, split_height, split_width, XS, YS, scale, self.photo_image)])
        canvas.bind("<ButtonPress-3>", lambda ev: [right_click(ev, img.height, img.width, split_height, split_width, XS, YS, scale, imgs, self.photo_image)])

if __name__ == "__main__":
    root = tk.Tk()
    app = Application(master = root)
    app.mainloop()
