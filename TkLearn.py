import tkinter as tk

# 声名一个窗口
window = tk.Tk()
window.title("My Windows")
window.geometry('200x100')

var = tk.StringVar()

# 创建一个label
Tlabe = tk.Label(window, text='你好', bg='green', font=('Arial', 12),
                 width=15, height=2)
# 将label装进windows
Tlabe.pack()  # 直接装载
# Tlabe.place()  装到指定的点
on_hit = False
#声名点击的方法函数
def hit_me():
    global on_hit
    if on_hit == False:
        on_hit == True
        var.set('你点击了我')
    else:
        on_hit == False
        var.set('')



Tb = tk.Button(window, text='点我看看', width=15, height=2, command=hit_me)
Tb.pack()
# 主窗口不断循环更新运行
window.mainloop()
