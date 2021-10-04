XS, YS = 5, 5

from PIL import Image
import os
import sys

from datetime import datetime

def ImgSplit(im):
    height = im.height / YS
    width = im.width / XS

    buff = []
    for h1 in range(YS):
        for w1 in range(XS):
            w2 = w1 * height
            h2 = h1 * width
            c = im.crop((w2, h2, width + w2, height + h2))
            buff.append(c)
    return buff

if __name__ == '__main__':
    im = Image.open('./getimg.png')
    # for ig in ImgSplit(im):
        # ig.save("./tmp/split.png" + datetime.now().strftime("%Y%m%d_%H%M%S%f_") +".png", "PNG")
    im = ImgSplit(im)
    for i in range(YS):
        for j in range(XS):
            im[i*YS+j].save("./tmp/split-" + str(i) + "-" + str(j) + ".png", "PNG")
