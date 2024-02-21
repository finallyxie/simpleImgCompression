#用opencv库制作一个图片压缩的可视化工具

import tkinter as tk
import os
from tkinter import filedialog
from tkinter import messagebox
from tkinter import Frame
import time
import random
from PIL import Image

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

        #创建图片压缩质量百分比标签
        self.label = tk.Label(self, text="压缩质量百分比(值越小压缩越高)")
        self.label.pack(padx=5, pady=5)
        
        #创建压缩质量百分比滑块
        self.scale = tk.Scale(self, from_=1, to=95, orient=tk.HORIZONTAL,length=280)
        self.scale.pack(padx=5, pady=5)
        #=创建压缩质量百分比滑块默认值
        self.scale.set(50)

        #创建图片尺寸调节输入框
        #单选 1:不调节  2:等比例压缩  3:自定义尺寸压缩
        #创建一个容器来包含单选按钮
        self.radio_frame = Frame(self)
        self.radio_frame.pack(padx=5, pady=5)
        #创建单选按钮
        self.radio_var = tk.IntVar()
        self.radio1 = tk.Radiobutton(self.radio_frame, text="不调节", variable=self.radio_var, value=1, command=self.hide_all)
        self.radio1.grid(row=0, column=0, padx=5, pady=5)
        self.radio2 = tk.Radiobutton(self.radio_frame, text="等比例压缩", variable=self.radio_var, value=2, command=self.hide_entry)
        self.radio2.grid(row=0, column=1, padx=5, pady=5)
        self.radio3 = tk.Radiobutton(self.radio_frame, text="自定义尺寸压缩", variable=self.radio_var, value=3, command=self.show_entry)
        self.radio3.grid(row=0, column=2, padx=5, pady=5)


        #默认选中不调节
        self.radio_var.set(1)

        #创建一个容器来占位包裹输入框
        self.radio2_frame = Frame(self)
        self.radio2_frame.pack(padx=5, pady=5)

        #创建所有输入框
        self.create_entry()
        self.create_entry2()



        # 创建压缩按钮
        self.compress_button = tk.Button(self, text="压缩", command=self.compress_image)
        self.compress_button.pack(padx=5, pady=5)

        self.hide_all()

        #创建打开文件夹按钮
        self.open_folder_button = tk.Button(self, text="打开文件夹")
        self.open_folder_button.pack(padx=5, pady=5)
        #隐藏打开文件夹按钮
        self.open_folder_button.pack_forget()

        #图片的后缀名
        self.file_ext = []
        #保存图片的原路径
        self.file_old_path = []
        
    def create_entry(self):
        #创建等比例压缩输入框
        self.radio2_label = tk.Label(self.radio2_frame, text="百分比: ")
        self.radio2_label.grid(row=0, column=0, padx=5, pady=5)
        self.radio2_entry = tk.Entry(self.radio2_frame)
        self.radio2_entry.grid(row=0, column=1,columnspan=2, padx=5, pady=5)
        self.radio2_label2 = tk.Label(self.radio2_frame, text="%")
        self.radio2_label2.grid(row=0, column=3, padx=5, pady=5)

    def create_entry2(self):
        #创建图片尺寸调节输入框
        self.width_label = tk.Label(self.radio2_frame, text="宽度")
        self.width_label.grid(row=1, column=0, padx=5, pady=5)
        self.width_entry = tk.Entry(self.radio2_frame)
        self.width_entry.grid(row=1, column=1,columnspan=2, padx=5, pady=5)
        self.width_label2 = tk.Label(self.radio2_frame, text="px")
        self.width_label2.grid(row=1, column=3, padx=5, pady=5)
        self.height_label = tk.Label(self.radio2_frame, text="高度")
        self.height_label.grid(row=2, column=0, padx=5, pady=5)
        self.height_entry = tk.Entry(self.radio2_frame)
        self.height_entry.grid(row=2, column=1,columnspan=2, padx=5, pady=5)
        self.height_label2 = tk.Label(self.radio2_frame, text="px")
        self.height_label2.grid(row=2, column=3, padx=5, pady=5)

    def show_entry(self):
        #隐藏等比例压缩输入框
        self.hide_all()
        #显示图片尺寸调节输入框
        self.create_entry2()
        

    def hide_entry(self):
        #隐藏图片尺寸调节输入框
        self.hide_all()
        #显示等比例压缩输入框
        self.create_entry()

    def hide_all(self):
        #隐藏图片尺寸调节输入框
        self.width_label.grid_forget()
        self.width_entry.grid_forget()
        self.width_label2.grid_forget()
        self.height_label.grid_forget()
        self.height_entry.grid_forget()
        self.height_label2.grid_forget()
        #隐藏等比例压缩输入框
        self.radio2_label.grid_forget()
        self.radio2_entry.grid_forget()
        self.radio2_label2.grid_forget()

    def upload_image(self):
        self.file_ext = []
        self.file_old_path = []
        # 创建文件选择对话框
        file_path = tk.filedialog.askopenfilenames(title='选择要上传的文件', filetypes=[('图片文件', '*.jpg;*.jpeg;*.png')],multiple=True)
        # 批量读取图片
        for path in file_path:
            #保存图片的原路径
            self.file_old_path.append(path)
            #保存文件的后缀名
            self.file_ext.append(os.path.splitext(path)[-1].lower())
            #如果不是图片进行提示并跳过此文件
            if self.file_ext[-1] not in [".jpg", ".jpeg", ".png"]:
                tk.messagebox.showerror("错误", "请选择图片文件")
                continue
        # 提示上传成功
        tk.messagebox.showinfo("提示", "图片上传成功")
        #界面展示已上传图片
        self.display.insert(0, "已上传图片")
        #如果打开文件夹按钮显示了隐藏打开文件夹按钮
        if self.open_folder_button.winfo_ismapped():
            self.open_folder_button.grid_forget()

    def compress_image(self):
        #按原路径循环检查是否上传了图片,图片格式为jpg或者png
        for i in range(len(self.file_old_path)):
            if self.file_ext[i] not in [".jpg", ".jpeg", ".png"]:
                tk.messagebox.showerror("错误", "请选择图片文件")
                return
        #新文件夹名称为年月日时分秒拼接随机数生成
        new_folder = time.strftime("%Y%m%d%H%M%S", time.localtime()) + str(random.randint(0, 100))
        #创建新文件夹
        os.mkdir(new_folder)
        for i in range(len(self.file_old_path)):
            # 读取上传的图片,因路径可能存在中文,使用PIL来读取图片
            image = Image.open(self.file_old_path[i])
            # 获取文件的文件名
            file_name = os.path.basename(self.file_old_path[i])
            # 如果选择不调节
            if self.radio_var.get() == 1:
                # 保存图片
                image.save(new_folder + "/" + file_name, quality=self.scale.get(), optimize=True)
            # 如果选择了等比例压缩
            if self.radio_var.get() == 2:
                # 获取原图大小
                width, height = image.size
                # 压缩图片,图片大小按比例缩放,压缩质量百分比由滑块控制
                image = image.thumbnail((int(width * float(self.radio2_entry.get()) / 100), int(height * float(self.radio2_entry.get()) / 100)))
                # 保存图片
                image.save(new_folder + "/" + file_name, quality=self.scale.get(), optimize=True)
            # 如果选择了自定义尺寸压缩
            if self.radio_var.get() == 3:
                # 压缩图片,图片大小按自定义尺寸缩放,压缩质量百分比由滑块控制
                image = image.resize((int(self.width_entry.get()), int(self.height_entry.get())))
                # 保存图片
                image.save(new_folder + "/" + file_name, quality=self.scale.get(), optimize=True)
                print("自定义尺寸压缩"+self.width_entry.get()+"X"+self.height_entry.get())
                
        # 提示压缩完成
        tk.messagebox.showinfo("提示", "图片压缩完成")
        #清空显示屏
        self.display.delete(0, "end")
        #滑块重置
        self.scale.set(50)
        #清空已上传图片
        self.file_ext = []
        self.file_old_path = []
        #重置单选按钮
        self.radio_var.set(1)
        #清空输入框
        self.width_entry.delete(0, "end")
        self.height_entry.delete(0, "end")
        self.radio2_entry.delete(0, "end")
        self.hide_all()
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

