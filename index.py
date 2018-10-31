from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk

if __name__ == "__main__":
    root = Tk()
    root.geometry('430x650+40+30')
    root.title("数字图像处理软件——北大软微")


    # setting up a tkinter canvas with scrollbars
    #frame = Frame(root, bd=2, relief=SUNKEN) #Frame是一个容器，用来布局
    frame = Frame(root, bd=2, relief=SUNKEN)  # Frame是一个容器，用来布局
    frame.grid_rowconfigure(0, weight=1)
    frame.grid_columnconfigure(0, weight=1)
    xscroll = Scrollbar(frame, orient=HORIZONTAL)
    xscroll.grid(row=1, column=0, sticky=E + W)
    yscroll = Scrollbar(frame)
    yscroll.grid(row=0, column=1, sticky=N + S)
    canvas = Canvas(frame, bd=0, xscrollcommand=xscroll.set, yscrollcommand=yscroll.set)
    canvas.grid(row=0, column=0, sticky=N + S + E + W)
    xscroll.config(command=canvas.xview)
    yscroll.config(command=canvas.yview)
    frame.pack(fill=BOTH, expand=1)


    # function to be called when mouse is clicked
    def printcoords():
        File = filedialog.askopenfilename(parent=root, initialdir="C:/", title='Choose an image.')
        im = Image.open(File)
        im.resize((400,600))
        filename = ImageTk.PhotoImage(im)
        canvas.image = filename  # <--- keep reference of your image
        canvas.create_image(0, 0, anchor='nw', image=filename)


    Button(root, text='选择图片1', command=printcoords).pack()
    Button(root, text='选择图片2', command=printcoords).pack()
    Button(root, text='选择图片2', command=printcoords).pack()
    root.mainloop()
