import tkinter as tk
import tkinter.ttk as ttk
from tkinter import font
from PIL import Image,ImageTk
import os
import tkinter.filedialog
import pyperclip

path = os.path.dirname(os.path.abspath(__file__))
MAXIMAGEWIDTH = 550
MAXIMAGEHEIGHT = 300

class MainUI():
    def __init__(self,f):
        self.root = tk.Tk()
        self.root.title("tkinterによるGUI画面作成")
        self.root.geometry("1280x720")
        self.root.configure(bg='#ffffff')
        self.displayframe1()
        self.f = f

    def displayframe1(self):
        # メインフレームの作成と設置
        self.frame1 = tk.Frame(self.root,background='#ffffff')
        self.frame1.pack(padx=0,pady=25)
        # 各種ウィジェットの作成
        self.frame1font = font.Font(family='Times', size=60)
        self.frame1font2 = font.Font(family='Times', size=20)
        self.frame1Title = ttk.Label(self.frame1, text="EmoFace",font=self.frame1font,background='#ffffff')
        # 各種ウィジェットの設置
        self.frame1Title.grid(row=0, column=0)

        self.img = Image.open(f"{path}/../data/image/pushphoto.png")
        self.img = self.img.resize((MAXIMAGEWIDTH,MAXIMAGEHEIGHT),Image.NEAREST)
        self.ph = ImageTk.PhotoImage(self.img)
        self.frame1Image = ttk.Label(master=self.frame1, image=self.ph,borderwidth = 6,relief="ridge")
        self.frame1Image.grid(row=1, column=0,pady=(30,0))

        self.frame1Button = tk.Button(self.frame1, text="Choose Image",font=self.frame1font2,command=self.pushimage)
        self.frame1Button.grid(row=2, column=0,pady=(30,0))

    def displayframe2(self):
        self.frame2 = tk.Frame(self.root,background='#ffffff')
        self.frame2.pack(padx=0,pady=25)

        self.frame2font = font.Font(family='Times', size=60)
        self.frame2Title = ttk.Label(self.frame2, text="EmoFace",font=self.frame2font,background='#ffffff')

        self.frame2Title.grid(row=0, column=0)
        self.img = Image.open(f"{path}/../data/image/making.png")
        self.img = self.img.resize((MAXIMAGEWIDTH,MAXIMAGEHEIGHT),Image.NEAREST)
        self.ph = ImageTk.PhotoImage(self.img)
        self.frame2Image = tk.Label(master=self.frame2, image=self.ph,background = '#ffffff',borderwidth = 6,relief="ridge")
        self.frame2Image.grid(row=1, column=0,pady=(30,0))

    def displayframe3(self):
        self.frame3 = tk.Frame(self.root,background='#ffffff')
        self.frame3.pack(padx=0,pady=25)

        self.frame3font = font.Font(family='Times', size=60)
        self.frame3font2 = font.Font(family='Times', size=20)

        self.frame3Title = ttk.Label(self.frame3, text="EmoFace",font=self.frame3font,background='#ffffff')
        self.frame3Title.grid(row=0, column=0)

        self.img = Image.open(self.emofacepath)
        self.img = self.img.resize((MAXIMAGEWIDTH,MAXIMAGEHEIGHT),Image.NEAREST)
        self.ph = ImageTk.PhotoImage(self.img)
        self.frame3Image = tk.Label(master=self.frame3, image=self.ph,background = '#ffffff',borderwidth = 6,relief="ridge")
        self.frame3Image.grid(row=1, column=0,pady=(30,0))

        self.frame3Label = ttk.Label(self.frame3, text="Complete",font=self.frame3font,background='#ffffff')
        self.frame3Label.grid(row=2, column=0)

        self.frame3Button = tk.Button(self.frame3, text="Copy!",font=self.frame3font2,command=self.copytext)
        self.frame3Button.grid(row=3, column=0,pady=(15,0))

        self.frame3Button2 = tk.Button(self.frame3, text="Return Home",font=self.frame3font2,command=self.home)
        self.frame3Button2.grid(row=4, column=0,pady=(15,0))

    def pushimage(self):
        typ = [('Png Image','*.png'),('Jpeg Image','*.jpg')]
        self.selectfile_path = tk.filedialog.askopenfilename(filetypes=typ)
        self.img = Image.open(self.selectfile_path)
        self.img = self.img.resize((MAXIMAGEWIDTH,MAXIMAGEHEIGHT),Image.NEAREST)
        self.ph = ImageTk.PhotoImage(self.img)
        self.frame1Image["image"] = self.ph
        self.frame1Button2 = tk.Button(self.frame1, text="Create EmoFace",font=self.frame1font2,command=self.emocreate)
        self.frame1Button2.grid(row=3, column=0,pady=(15,0))

    def emocreate(self):
        self.frame1.destroy()
        self.displayframe2()
        #imageの形式は、path
        self.emofacepath,self.emoticon = self.f(self.selectfile_path)
        self.frame2.destroy()
        self.displayframe3()

    def copytext(self):
        pyperclip.copy("#hackday2021 ものづくりって楽しいね"+self.emoticon)
        self.frame3Button["text"] = "Copied!"

    def home(self):
        self.frame3.destroy()
        self.displayframe1()









if __name__ == '__main__':
    Ui = MainUI()
    Ui.root.resizable(width=False, height=False)
    Ui.root.mainloop()
