from get_face_attribute import get_face_attribute
from similarcheck import rSimilarEmoticon
from ui.main import MainUI
from time import sleep
import os

def function(filepath):
    print("aaa")
    data = get_face_attribute(filepath)
    emoticon = rSimilarEmoticon(data)
    print(emoticon)
    return "C:\\Users\\takara2314\\OneDrive\\EmoFace\\data\\image\\pushphoto.png"

if __name__ == '__main__':
     Ui = MainUI(function)
     Ui.root.resizable(width=False, height=False)
     Ui.root.mainloop()
"""
    print("Hello Valpusgo world!")
    os.chdir("models")
    # models フォルダからみたファイルパスを指定
    data = get_face_attribute("../data/image/sample.png")
    os.chdir("/")

    # 後は焼くなり煮るなり好きにしやがれください
    print(data)
"""
