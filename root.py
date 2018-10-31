from tkinter import *
import tkinter.messagebox as messagebox
import cv2 as cv
from PIL import Image
import copy
import numpy as np
import matplotlib.pyplot as plt
from pylab import array
from pylab import figure
from pylab import histogram
from pylab import subplot
from pylab import hist
from pylab import plot
from pylab import interp
from pylab import gray
from pylab import imshow
from pylab import show


class Application(Frame):  # 从Frame派生出Application类，它是所有widget的父容器
    def __init__(self, master=None):  # master即是窗口管理器，用于管理窗口部件，如按钮标签等，顶级窗口master是None，即自己管理自己
        Frame.__init__(self, master)
        self.pack()  # 将widget加入到父容器中并实现布局
        self.createWidgets()

    def createWidgets(self):
        self.helloLabel = Label(self, text='请输入图片路径')  # 创建一个标签显示内容到窗口
        self.helloLabel.pack()
        self.input = Entry(self)  # 创建一个输入框，以输入内容
        self.input.pack()

        self.nameButton_1 = Button(self, text='图像取反', command=self.image_1)
        self.nameButton_1.place()

        self.nameButton_2 = Button(self, text='图像缩放', command=self.image_2)
        self.nameButton_2.pack()

        self.nameButton_3 = Button(self, text='直方图均衡化', command=self.image_3)
        self.nameButton_3.pack()

        self.nameButton_4 = Button(self, text='幂次变换', command=self.image_4)
        self.nameButton_4.pack()

        self.quitButton = Button(self, text='退出', command=self.quit)  # 创建一个Quit按钮，实现点击即退出窗口
        self.quitButton.pack()

    def image_1(self):
        name = self.input.get()  # 获取输入的内容

        rgb_img = cv.imread(name, 1)

        reverse_img = 255 - rgb_img
        cv.imshow('reverse image', reverse_img)

    def image_2(self):
        name = self.input.get()

        img = cv.imread(name, 1)
        img_out = cv.resize(img, (500, 1000), interpolation=cv.INTER_LINEAR)
        cv.imshow("new image", img_out)

    def image_3(self):
        name = self.input.get()

        # 读取图像到数组中
        im = array(Image.open(name))

        # 获取通道
        r = im[:, :, 0]
        g = im[:, :, 1]
        b = im[:, :, 2]
        # 显示各个通道原始直方图，均值化之后的直方图以及累计分布函数
        figure()
        # 计算各通道直方图
        imhist_r, bins_r = histogram(r, 256, normed=True)
        imhist_g, bins_g = histogram(g, 256, normed=True)
        imhist_b, bins_b = histogram(b, 256, normed=True)

        subplot(331)
        hist(r.flatten(), 256)
        subplot(332)
        hist(g.flatten(), 256)
        subplot(333)
        hist(b.flatten(), 256)

        # 各通道累积分布函数
        cdf_r = imhist_r.cumsum()
        cdf_g = imhist_g.cumsum()
        cdf_b = imhist_b.cumsum()

        # 累计函数归一化（由0～1变换至0~255）
        cdf_r = cdf_r * 255 / cdf_r[-1]
        cdf_g = cdf_g * 255 / cdf_g[-1]
        cdf_b = cdf_b * 255 / cdf_b[-1]
        # 绘制累计分布函数

        subplot(334)
        plot(bins_r[:256], cdf_r)
        subplot(335)
        plot(bins_g[:256], cdf_g)
        subplot(336)
        plot(bins_b[:256], cdf_b)

        # 绘制直方图均衡化之后的直方图

        im_r = interp(r.flatten(), bins_r[:256], cdf_r)
        im_g = interp(g.flatten(), bins_g[:256], cdf_g)
        im_b = interp(b.flatten(), bins_b[:256], cdf_b)

        # 显示直方图图像
        subplot(337)
        hist(im_r, 256)
        subplot(338)
        hist(im_g, 256)
        subplot(339)
        hist(im_b, 256)
        # 显示原始通道图与均衡化之后的通道图
        figure()
        gray()

        # 原始通道图
        im_r_s = r.reshape([im.shape[0], im.shape[1]])
        im_g_s = g.reshape([im.shape[0], im.shape[1]])
        im_b_s = b.reshape([im.shape[0], im.shape[1]])

        # 均衡化之后的通道图
        im_r = im_r.reshape([im.shape[0], im.shape[1]])
        im_g = im_g.reshape([im.shape[0], im.shape[1]])
        im_b = im_b.reshape([im.shape[0], im.shape[1]])

        subplot(231)
        imshow(im_r_s)

        subplot(232)

        imshow(im_g_s)

        subplot(233)

        imshow(im_b_s)

        subplot(234)

        imshow(im_r)

        subplot(235)

        imshow(im_g)

        subplot(236)

        imshow(im_b)

        # 显示原始图像与均衡化之后的图像
        figure()

        # 均衡化之后的图像
        im_p = copy.deepcopy(im)

        im_p[:, :, 0] = im_r

        im_p[:, :, 1] = im_g

        im_p[:, :, 2] = im_b

        subplot(121)

        imshow(im)

        subplot(122)

        imshow(im_p)

        show()

    def image_4(self):
        name = self.input.get()

        def gamma(img, c, v):
            lut = np.zeros(256, dtype=np.float32)
            for i in range(256):
                lut[i] = c * i ** v
            output_img = cv.LUT(img, lut)
            output_img = np.uint8(output_img + 0.5)
            return output_img

        img_input = cv.imread(name, cv.IMREAD_GRAYSCALE)
        img_output = gamma(img_input, 0.00000005, 4.0)
        cv.imshow('output.jpg', img_output)


app = Application()
app.master.title("图像处理V1.0-伍汝杰")  # 窗口标题

app.mainloop()  # 主消息循环
