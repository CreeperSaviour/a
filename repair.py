import tkinter as tk
from PIL import Image, ImageTk

canvas = None
clicked_pos = (-1, -1)

result = []
img_t = []

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

def left_click(ev, height, width, split_height, split_width, XS, YS, scale, imgs, photo_image):
    global clicked_pos
    x = (int)(ev.x / (width * scale / XS))
    y = (int)(ev.y / (height * scale / YS))
    # print('{}{}'.format((int)(x), (int)(y)))
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

def right_click(ev, height, width, split_height, split_width, XS, YS, scale, imgs):
    global img_t
    x = (int)(ev.x / (width * scale / XS))
    y = (int)(ev.y / (height * scale / YS))
    x2, y2 = result[y][x]["pos"]
    width, height = split_width * x + (split_width // 2), split_height * y + (split_height // 2)
    result[y][x]["rotate"] = (result[y][x]["rotate"] + 1) % 4
    canvas.delete('img{}{}'.format(x, y))
    img_t.append(ImageTk.PhotoImage(imgs[y2*YS+x2].rotate(result[y][x]["rotate"] * 90)))
    canvas.create_image(width, height, image=img_t[len(img_t)-1], tag='img{}{}'.format(x, y))

def show_result():
    print(result)

class Application(tk.Frame):
    def __init__(self, master, img_path, XS, YS, scale):
        super().__init__(master)
        global canvas

        img = Image.open(img_path)
        imgs, split_height, split_width = ImgSplit(img, scale)
        for i in range(YS):
            result.append([])
            for j in range(XS):
                c = {}
                c["pos"] = (j, i)
                c["rotate"] = 0
                result[i].append(c)

        self.master.title("画像の表示")
        self.master.geometry("{}x{}".format(img.width, img.height))

        canvas = tk.Canvas(self.master, width=(int)(img.width * scale), height=(int)(img.height * scale))

        self.photo_image = []
        for y in range(YS):
            for x in range(XS):
                self.photo_image.append(ImageTk.PhotoImage(imgs[y*YS+x]))

                width = split_width * x + (split_width // 2)
                height = split_height * y + (split_height // 2)
                canvas.create_image(width, height, image=self.photo_image[y*YS+x], tag='img{}{}'.format(x, y))
        canvas.pack()
        canvas.bind("<ButtonPress-1>", lambda ev: [left_click(ev, img.height, img.width, split_height, split_width, XS, YS, scale, imgs, self.photo_image)])
        canvas.bind("<ButtonPress-3>", lambda ev: [right_click(ev, img.height, img.width, split_height, split_width, XS, YS, scale, imgs)])

        self.button = tk.Button(self.master, text="Result", command=show_result)
        self.button.pack()

if __name__ == "__main__":
    img_path = './getimg.png'
    XS, YS = 5, 5
    scale = 0.5
    root = tk.Tk()
    app = Application(root, img_path, XS, YS, scale)
    app.mainloop()
