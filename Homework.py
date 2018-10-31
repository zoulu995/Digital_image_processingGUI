from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
import cv2
import os
import numpy as np


# 彩色图像直方图均衡化
def hisEqulColor(img):
    ycrcb = cv2.cvtColor(img, cv2.COLOR_BGR2YCR_CB)
    channels = cv2.split(ycrcb)
    print(len(channels))
    cv2.equalizeHist(channels[0], channels[0])
    cv2.merge(channels, ycrcb)
    cv2.cvtColor(ycrcb, cv2.COLOR_YCR_CB2BGR, img)
    return img


# 描绘伽马函数的图像
def gamma_plot(c, v):  # gamma_plot(0.00000005, 4.0)
    x = np.arange(0, 256, 0.01)  # 生成一个数组[0, 0.01, 0.02, ...,256]
    y = c * x ** v  # 伽马函数
    plt.plot(x, y, 'r', linewidth=1)
    plt.title('伽马变换函数')
    plt.xlim([0, 255]), plt.ylim([0, 255])
    plt.show()


# 返回经过伽马变换的图像
def gamma(img, c, v):
    lut = np.zeros(256, dtype=np.float32)  # np.zeros(shape,dtype):shape是形状，可以是256，可以是（256，256），dtype是np数据类型
    for i in range(256):
        lut[i] = c * i ** v
    output_img = cv2.LUT(img, lut)  # cv2.LUT(img,lut):img原始图像，lut是查询表
    output_img = np.uint8(output_img + 0.5)
    return output_img


class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.creatWidgets()

    def creatWidgets(self):
        self.SelecLable = Label(self, text='请选择图片：').grid(row=0, column=0, sticky=E)
        self.SelecBt = Button(self, text='选择', command=self.SelectImag).grid(sticky=W, row=0, column=1)
        self.FuncLable = Label(self, text='数字图像功能列表').grid(row=1, columnspan=2)
        self.Fun1Bt = Button(self, text='图像取反', command=self.image1).grid(row=2, column=0, sticky=E)
        self.Fun2Bt = Button(self, text='图像缩放', command=self.image2).grid(row=2, column=1, sticky=W)
        self.Fun3Bt = Button(self, text='直方图均衡', command=self.image3).grid(row=3, column=0, sticky=E)
        self.Fun4Bt = Button(self, text='幂次变换', command=self.image4).grid(row=3, column=1, sticky=W)
        self.ExitBt = Button(self, text='退出', command=self.quit).grid(row=4, columnspan=2)
        # self.Image = Canvas(self,bg='white',width=200,height=200).grid(row=5, columnspan=2)

    # 选择图像的button方法
    def SelectImag(self):
        self.File = filedialog.askopenfilename(parent=self, initialdir="C:/", title='选择一个图片.')
        print(self.File)
        self.im = Image.open(self.File)
        self.im.resize((200, 200))
        self.filename = ImageTk.PhotoImage(self.im)
        self.Image = self.filename  # <--- keep reference of your image
        self.ImagLable = Label(self, image=self.Image).grid(row=5, columnspan=2)
        # self.Image.create_image(0, 0, anchor='nw', image=self.filename)

    # 读取灰度图像
    def cv_imread0(self, filePath):
        cv_img = cv2.imdecode(np.fromfile(filePath, dtype=np.uint8),
                              0)  # imread('图像地址',1) 第二个参数可以是1，0，-1， 1是读彩色图片，0是灰度图片，-1是包含alph通道，就是透明度
        return cv_img

    # 读取RGB图像，并包括alph通道，就是透明度
    def cv_imread(self, filePath):
        cv_img = cv2.imdecode(np.fromfile(filePath, dtype=np.uint8),
                              -1)  # imread('图像地址',1) 第二个参数可以是1，0，-1， 1是读彩色图片，0是灰度图片，-1是包含alph通道，就是透明度
        return cv_img

    # 只读取RGB图像
    def cv_imread1(self, filePath):
        cv_img = cv2.imdecode(np.fromfile(filePath, dtype=np.uint8), 1)  # 这里的模式是采用彩色图像
        return cv_img

    # 图像取反
    def image1(self):
        print("image1:" + self.File)
        name = self.cv_imread1(self.File)
        if name == None:
            print("Error: could not load image")
            os._exit(0)
        rgb_img = name
        print(rgb_img)
        reverse_img = 255 - rgb_img
        cv2.imshow('reverse image', reverse_img)

    # 图像缩放
    def image2(self):
        print("image2:" + self.File)
        img = self.cv_imread1(self.File)
        if img == None:
            print("Error: could not load image")
            os._exit(0)

        height, width = img.shape[:2]  # 0,1不包括2

        # 缩小图像
        size = (int(width * 0.3), int(height * 0.5))
        shrink = cv2.resize(img, size, interpolation=cv2.INTER_AREA)  # resize('图片'，'图像大小'，'插值模式')  这里用于图像缩放的时候，类似与最近邻插值

        # 放大图像
        fx = 1.6
        fy = 1.2
        enlarge = cv2.resize(img, (0, 0), fx=fx, fy=fy, interpolation=cv2.INTER_CUBIC)  # cv2.INTER_CUBIC：4x4像素邻域的双三次插值

        # 显示
        cv2.imshow("src", img)
        cv2.imshow("shrink", shrink)
        cv2.imshow("enlarge", enlarge)

    # 直方图均衡化
    def image3(self):
        print("image1:" + self.File)
        image = self.cv_imread0(self.File)
        if image == None:
            print("Error: could not load image")
            os._exit(0)
        #     采用调用系统open-cv的方法
        # equ = cv2.equalizeHist(name)  #cv2.equalizeHist 直方图均衡化，只能对灰色图片使用
        # cv2.imshow('equ', equ)

        lut = np.zeros(256, dtype=image.dtype)  # 创建空的查找表

        hist, bins = np.histogram(image.flatten(), 256, [0, 256])
        cdf = hist.cumsum()  # 计算累积直方图
        cdf_m = np.ma.masked_equal(cdf, 0)  # 除去直方图中的0值
        cdf_m = (cdf_m - cdf_m.min()) * 255 / (cdf_m.max() - cdf_m.min())  # 等同于前面介绍的lut[i] = int(255.0 *p[i])公式
        cdf = np.ma.filled(cdf_m, 0).astype('uint8')  # 将掩模处理掉的元素补为0

        # 计算
        result2 = cdf[image]
        # result = cv2.LUT(image, cdf)

        # cv2.imshow("OpenCVLUT", result)
        cv2.imshow("NumPyLUT", result2)

    # 幂次变换
    def image4(self):
        print("image4:" + self.File)
        img_input = self.cv_imread1(self.File)
        if img_input == None:
            print("Error: could not load image")
            os._exit(0)
        cv2.imshow('imput', img_input)  # y = c * r ** v  伽马函数表达式
        gamma_plot(0.00000005, 4.0)  # 第一个参数是c，第二个参数是伽马的取值=4
        img_output = gamma(img_input, 0.00000005,4.0)
        cv2.imshow('output', img_output)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()


app = Application()
app.master.title("北大软微数字图像课——邹宇航")
app.master.geometry('800x600+500+70')
app.mainloop()
