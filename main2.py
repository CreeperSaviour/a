import tkinter as tk
from PIL import Image, ImageTk

XS, YS = 5, 5

def ImgSplit(im, scale=1.0):
    height = im.height / YS
    width = im.width / XS

    buff = []
    for h1 in range(YS):
        for w1 in range(XS):
            w2 = w1 * height
            h2 = h1 * width
            c = im.crop((w2, h2, width + w2, height + h2))
            w3, h3 = int((width + w2) * scale), int((height + h2) * scale)
            c.resize((w3, h3))
            buff.append(c)
    return buff, height, width

class Application(tk.Frame):
    def __init__(self, master = None):
        super().__init__(master)

        img = Image.open('./getimg.png')
        imgs, split_height, split_width = ImgSplit(img, 0.5)

        self.master.title("画像の表示")       # ウィンドウタイトル
        self.master.geometry("{}x{}".format(img.width, img.height))     # ウィンドウサイズ(幅x高さ)

        self.canvas = []
        for i in range(len(imgs)):
            # Canvasの作成
            self.canvas.append(tk.Canvas(self.master))
            # Canvasを配置
            self.canvas[i].pack(expand = True, fill = tk.BOTH)

        self.photo_image = []
        for i in range(YS):
            for j in range(XS):
                # 画像ファイルを開く（対応しているファイルフォーマットはPGM、PPM、GIF、PNG）
                # self.photo_image = ImageTk.PhotoImage(file = "./tmp/split-0-0.png")
                self.photo_image.append(ImageTk.PhotoImage(imgs[i*YS+j]))

                # キャンバスのサイズを取得
                self.update() # Canvasのサイズを取得するため更新しておく
                canvas_width = self.canvas[i*YS+j].winfo_width()
                canvas_height = self.canvas[i*YS+j].winfo_height()

                # 画像の描画
                self.canvas[i*YS+j].create_image(
                        split_width * j + (split_width / 2),       # 画像表示位置(Canvasの中心)
                        split_height * i + (split_height / 2),
                        image=self.photo_image[i*YS+j]  # 表示画像データ
                        )

if __name__ == "__main__":
    root = tk.Tk()
    app = Application(master = root)
    app.mainloop()