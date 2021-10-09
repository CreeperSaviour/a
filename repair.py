import tkinter as tk
from PIL import Image, ImageTk
import copy

"""
[a, b]はその座標でa,bに行かなければならない
"""

canvas = None
clicked_pos = (-1, -1)

result = []
img_t = []

def ImgSplit(im, XS, YS, scale=1.0):
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
    global clicked_pos, canvas
    x = (int)(ev.x / (width * scale / XS))
    y = (int)(ev.y / (height * scale / YS))
    # print('{}{}'.format((int)(x), (int)(y)))
    if clicked_pos == (-1, -1):
        clicked_pos = ((int)(x), (int)(y))
    else:
        x2, y2 = clicked_pos[0], clicked_pos[1]
        width, height = split_width * x + (split_width // 2), split_height * y + (split_height // 2)
        width_t, height_t = split_width * x2 + (split_width // 2), split_height * y2 + (split_height // 2)
        canvas.delete('img{}{}'.format(x, y))
        canvas.delete('img{}{}'.format(x2, y2))
        print('x, y, x2, y2', x, y, x2, y2)
        for i in range(YS):
            for j in range(XS):
                if result[i][j]["pos"] == (x, y):
                    x3, y3 = j, i
                if result[i][j]["pos"] == (x2, y2):
                    x4, y4 = j, i
        print('x3, y3, x4, y4', x3, y3, x4, y4)
        print('result[y3][x3]["rotate"]', result[y3][x3]["rotate"])
        print('result[y4][x4]["rotate"]', result[y4][x4]["rotate"])
        print(result)
        img_t.append(ImageTk.PhotoImage(imgs[y4*YS+x4].rotate(result[y4][x4]["rotate"] * 90)))
        canvas.create_image(width, height, image=img_t[-1], tag='img{}{}'.format(x, y))
        img_t.append(ImageTk.PhotoImage(imgs[y3*YS+x3].rotate(result[y3][x3]["rotate"] * 90)))
        canvas.create_image(width_t, height_t, image=img_t[-1], tag='img{}{}'.format(x2, y2))
        result[y3][x3]["pos"], result[y4][x4]["pos"] = result[y4][x4]["pos"], result[y3][x3]["pos"]
        
        print(result)
        # photo_image[y2*YS+x2], photo_image[y*YS+x] = photo_image[y*YS+x], photo_image[y2*YS+x2]
        clicked_pos = (-1, -1)

def right_click(ev, height, width, split_height, split_width, XS, YS, scale, imgs):
    global img_t, canvas
    x = (int)(ev.x / (width * scale / XS))
    y = (int)(ev.y / (height * scale / YS))
    x2, y2 = -1, -1
    for i in range(YS):
        for j in range(XS):
            if result[i][j]["pos"] == (x, y):
                x2, y2 = j, i
    # x2, y2 = result[y][x]["pos"]
    width, height = split_width * x + (split_width // 2), split_height * y + (split_height // 2)
    result[y2][x2]["rotate"] = (result[y2][x2]["rotate"] + 1) % 4
    canvas.delete('img{}{}'.format(x, y))
    print('x, y, x2, y2', x, y, x2, y2)
    img_t.append(ImageTk.PhotoImage(imgs[y2*YS+x2].rotate(result[y2][x2]["rotate"] * 90)))
    canvas.create_image(width, height, image=img_t[len(img_t)-1], tag='img{}{}'.format(x, y))
    # canvas.create_image(width, height, image=img_t[len(img_t)-1], tag='img{}{}'.format(x2, y2))


class Application(tk.Frame):
    def __init__(self, master, img_path, scale):
        super().__init__(master)
        global canvas

        self.img_path = img_path
        self.scale = scale

        self.master.title("画像の表示")
        # self.master.geometry("{}x{}".format(img.width, img.height))
        self.master.geometry("{}x{}".format(1200, 1000))

        canvas = tk.Canvas(self.master, width=(int)(1000), height=(int)(800))

        self.text = tk.Text(self.master, width=400, height=5)
        self.text.pack()
        self.button_load = tk.Button(self.master, text="読み込み", command=self.show_canvas)
        self.button_load.pack()

        canvas.pack()
        canvas.bind("<ButtonPress-1>", lambda ev: [left_click(ev, self.img.height, self.img.width, self.split_height, self.split_width, self.XS, self.YS, self.scale, self.imgs, self.photo_image)])
        canvas.bind("<ButtonPress-3>", lambda ev: [right_click(ev, self.img.height, self.img.width, self.split_height, self.split_width, self.XS, self.YS, self.scale, self.imgs)])
        
        self.button = tk.Button(self.master, text="Result", command=self.show_result)
        self.button_right = tk.Button(self.master, text="1行ずつ右にずらす", command=self.move_right)
        self.button_up = tk.Button(self.master, text="1列ずつ上にずらす", command=self.move_up)
        self.button.pack()
        self.button_right.pack()
        self.button_up.pack()


    def show_canvas(self):
        # in_data = "5 5\n[2, 3] [2, 2] [4, 4] [1, 0] [4, 2]\n[3, 2] [1, 4] [0, 3] [3, 4] [2, 0]\n[2, 4] [1, 3] [0, 4] [0, 0] [0, 1]\n[4, 1] [3, 1] [3, 0] [1, 1] [-1, -1]\n[1, 2] [3, 3] [0, 2] [2, 1] [4, 3]\n0 0 0 2 2\n0 2 3 0 2\n0 2 3 1 3\n0 2 0 2 0\n2 0 0 1 2"
        # in_data = "5 5\n[2, 3] [2, 2] [4, 4] [1, 0] [4, 2]\n[3, 2] [1, 4] [0, 3] [3, 4] [2, 0]\n[2, 4] [1, 3] [0, 4] [0, 0] [0, 1]\n[4, 1] [3, 1] [3, 0] [1, 1] [-1, -1]\n[1, 2] [3, 3] [0, 2] [2, 1] [4, 3]\n0 0 0 0 0\n0 0 1 0 3\n0 2 0 1 0\n0 2 0 2 0\n0 0 1 1 2"
        in_data = self.text.get("1.0", "end")
        self.XS, self.YS = read_data(in_data)

        self.img = Image.open(self.img_path)
        self.imgs, self.split_height, self.split_width = ImgSplit(self.img, self.XS, self.YS, scale)

        self.photo_image = []
        print(result)
        for y in range(self.YS):
            for x in range(self.XS):
                self.photo_image.append(ImageTk.PhotoImage(self.imgs[y*self.YS+x].rotate(result[y][x]["rotate"] * 90)))
        for y in range(self.YS):
            for x in range(self.XS):
                pos = result[y][x]["pos"]
                width = self.split_width * pos[0] + (self.split_width // 2)
                height = self.split_height * pos[1] + (self.split_height // 2)
                canvas.create_image(width, height, image=self.photo_image[y*self.YS+x], tag='img{}{}'.format(pos[0], pos[1]))

    def show_result(self):
        data = "{} {}".format(self.XS, self.YS)
        data += "\n"
        for y in range(self.YS):
            child_data = []
            for x in range(self.XS):
                child_data.append("[{}, {}]".format(result[y][x]["pos"][1], result[y][x]["pos"][0]))
            child_data = ' '.join(child_data)
            data += child_data + '\n'
        for y in range(self.YS):
            child_data = []
            for x in range(self.XS):
                child_data.append(str(result[y][x]["rotate"]))
            child_data = ' '.join(child_data)
            data += child_data + '\n'
        print(data)

    def move_right(self):
        for y in range(self.YS):
            for x in range(self.XS):
                result[y][x]["pos"] = ((result[y][x]["pos"][0] + 1) % self.XS, result[y][x]["pos"][1])
        for y in range(self.YS):
            for x in range(self.XS):
                canvas.delete('img{}{}'.format(x, y))
        for y in range(self.YS):
            for x in range(self.XS):
                pos = result[y][x]["pos"]
                width = self.split_width * pos[0] + (self.split_width // 2)
                height = self.split_height * pos[1] + (self.split_height // 2)
                canvas.create_image(width, height, image=ImageTk.PhotoImage(self.imgs[pos[1]*YS+pos[0]].rotate(result[y][x]["rotate"] * 90)), tag='img{}{}'.format(pos[0], pos[1]))

    def move_up(self):
        global img_t, result
        result_t = copy.deepcopy(result)
        for y in range(self.YS):
            for x in range(self.XS):
                result_t[y][x] = {"pos": (result[y][x]["pos"][0], (result[y][x]["pos"][1] - 1) % self.YS), "rotate": result[y][x]["rotate"]}
        result = result_t
        # tmp = []
        # for x in range(self.XS):
        #     tmp.append(result[0][x]["rotate"])
        # for y in range(self.YS - 1):
        #     for x in range(self.XS):
        #         result[y][x]["rotate"] = result[y + 1][x]["rotate"]
        #         for i in range(YS):
        #             for j in range(XS):
        #                 if result[i][j]["pos"] == (x, y):
        #                     x2, y2 = j, i
        # for x in range(self.XS):
        #     result[self.YS - 1][x]["rotate"] = tmp[x]
        for y in range(self.YS):
            for x in range(self.XS):
                canvas.delete('img{}{}'.format(x, y))
        for y in range(self.YS):
            for x in range(self.XS):
                pos = result[y][x]["pos"]
                width = self.split_width * pos[0] + (self.split_width // 2)
                height = self.split_height * pos[1] + (self.split_height // 2)
                # canvas.create_image(width, height, image=self.photo_image[y*self.YS+x], tag='img{}{}'.format(pos[0], pos[1]))
                img_t.append(ImageTk.PhotoImage(self.imgs[y*YS+x].rotate(result[pos[1]][pos[0]]["rotate"] * 90)))
                canvas.create_image(width, height, image=img_t[len(img_t) - 1], tag='img{}{}'.format(pos[0], pos[1]))

def read_data(data):
    global result
    split_data = data.split('\n')

    XS, YS = split_data[0].split(' ')
    XS, YS = int(XS), int(YS)
    POS = []
    ROTATE = []

    i = 1
    while i != int(YS) + 1:
        POS.append([])
        e = split_data[i].replace(', ', ',').replace('[', '').replace(']', '')
        e2 = e.split(' ')
        for e3 in e2:
            e3 = e3.split(',')
            POS[i-1].append(((int)(e3[1]), (int)(e3[0])))
        i += 1

    while i != int(YS) * 2 + 1:
        ROTATE.append([])
        e = split_data[i].split(' ')
        e = list(map(lambda x: int(x), e))
        for e2 in e:
            ROTATE[i-int(YS)-1].append(e2)
        i += 1

    result = [[None] * YS for i in range(XS)]
    for y in range(YS):
        for x in range(XS):
            if POS[y][x] == (-1, -1):
                continue
            c = {"pos": None, "rotate": None}
            c["pos"] = POS[y][x] # posにはその画像がもともとどこにいたか
            c["rotate"] = ROTATE[y][x]
            result[y][x] = c

    tmp = [[None] * YS for i in range(XS)]
    for y in range(YS):
        for x in range(XS):
            if POS[y][x] == (-1, -1):
                continue
            xt, yt = POS[y][x]
            tmp[yt][xt] = 0
    c = {"pos": None, "rotate": None}
    for y in range(YS):
        for x in range(XS):
            if tmp[y][x] == None:
                c["pos"] = (x, y)
    for y in range(YS):
        for x in range(XS):
            if POS[y][x] == (-1, -1):
                c["rotate"] = ROTATE[y][x]
                result[y][x] = c

    return XS, YS

if __name__ == "__main__":
    img_path = './getimg.png'
    scale = 0.3
    root = tk.Tk()
    app = Application(root, img_path, scale)
    app.mainloop()
