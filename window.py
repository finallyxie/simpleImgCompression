#用opencv库制作一个图片压缩的可视化工具

import tkinter as tk
import cv2
import os
from tkinter import filedialog
from tkinter import messagebox
import time
import random

class Calculator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Simple Calculator")
        self.geometry("350x400")
        self.expression = ""
 
        # 创建显示屏
        self.display = tk.Entry(self, width=35, borderwidth=5)
        self.display.pack(padx=5, pady=5)

        #创建图片上传按钮
        self.upload_button = tk.Button(self, text="上传图片", command=self.upload_image)
        self.upload_button.pack(padx=5, pady=5)

        #创建压缩质量百分比滑块
        self.scale = tk.Scale(self, from_=0, to=100, orient=tk.HORIZONTAL, label="压缩质量百分比")
        self.scale.pack(padx=5, pady=5)
        #=创建压缩质量百分比滑块默认值
        self.scale.set(50)

        # 创建压缩按钮
        self.compress_button = tk.Button(self, text="压缩", command=self.compress_image)
        self.compress_button.pack(padx=5, pady=5)

        #创建打开文件夹按钮
        self.open_folder_button = tk.Button(self, text="打开文件夹")
        self.open_folder_button.pack(padx=5, pady=5)
        #隐藏打开文件夹按钮
        self.open_folder_button.pack_forget()

        #图片的后缀名
        self.file_ext = ""

    def upload_image(self):
        #检查是否有temp文件夹，没有则创建
        if not os.path.exists("temp"):
            os.mkdir("temp")
        #清空temp文件夹
        for file in os.listdir("temp"):
            os.remove(f"temp/{file}")
        # 创建文件选择对话框
        file_path = tk.filedialog.askopenfilename()
        # 读取图片
        image = cv2.imread(file_path)
        #保存文件的后缀名
        self.file_ext = os.path.splitext(file_path)[-1]
        #如果不是图片进行提示
        if self.file_ext not in [".jpg", ".png"]:
            tk.messagebox.showerror("错误", "请选择图片文件")
            return
        # 将图片保存为进temp文件夹并命名为image.+后缀名
        cv2.imwrite("temp/image"+self.file_ext, image)
        # 提示上传成功
        tk.messagebox.showinfo("提示", "图片上传成功")
        #界面展示已上传图片
        self.display.insert(0, "已上传图片")
        #如果打开文件夹按钮显示了隐藏打开文件夹按钮
        if self.open_folder_button.winfo_ismapped():
            self.open_folder_button.pack_forget()

    def compress_image(self):
        #检查是否上传了图片,图片格式为jpg或者png
        if not os.path.exists("temp/image.jpg") and not os.path.exists("temp/image.png"):
            tk.messagebox.showerror("错误", "请先上传图片")
            return
        # 读取上传的图片
        image = cv2.imread("temp/image"+self.file_ext)
        # 压缩图片质量不改变图片尺寸,压缩质量百分比由滑块控制
        cv2.imwrite("temp/compressed"+self.file_ext, image, [int(cv2.IMWRITE_JPEG_QUALITY), self.scale.get()])
        #保存图片至新文件夹下并命名为image.+后缀名
        #新文件夹名称为年月日时分秒拼接随机数生成
        new_folder = time.strftime("%Y%m%d%H%M%S", time.localtime()) + str(random.randint(0, 100))
        #创建新文件夹
        os.mkdir(new_folder)
        os.rename("temp/compressed"+self.file_ext, new_folder+"/compressed"+self.file_ext)
        # 提示压缩完成
        tk.messagebox.showinfo("提示", "图片压缩完成")
        #清空temp文件夹
        for file in os.listdir("temp"):
            os.remove(f"temp/{file}")
        #清空显示屏
        self.display.delete(0, "end")
        #滑块重置
        self.scale.set(50)
        #显示打开文件夹按钮
        self.open_folder_button = tk.Button(self, text="打开文件夹", command=lambda: os.startfile(new_folder))
        self.open_folder_button.pack(padx=5, pady=5)

if __name__ == "__main__":
    app = Calculator()
    app.mainloop()

#运行程序，点击上传图片按钮，选择一张图片，然后点击压缩按钮，程序会将图片压缩后保存为compressed.jpg。
#这样就实现了一个图片压缩的可视化工具。
#调用
#python window.py
#即可运行程序。        

