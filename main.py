from get_face_attribute import get_face_attribute
from similarcheck import rSimilarEmoticon
from ui.main import MainUI
from time import sleep
import os
from src.texttoimage import texttoimage

kpath = "C:/Users/kosakae256/Documents/Kosakae-Deployment/EmoFace/data/image/pushphoto.png"
tpath = "C:/Users/takara2314/OneDrive/EmoFace/data/image/pushphoto.png"
path = os.path.dirname(os.path.abspath(__file__))

def function(filepath):
    print(filepath)
    os.chdir(f"{path}/models/")
    print(filepath)
    data = get_face_attribute(filepath)
    os.chdir(f"{path}/")
    emoticon = rSimilarEmoticon(data)
    textpath = texttoimage(emoticon)

    return textpath,emoticon

if __name__ == '__main__':
     Ui = MainUI(function)
     Ui.root.resizable(width=False, height=False)
     Ui.root.mainloop()

    #os.chdir("models")
    # models フォルダからみたファイルパスを指定
    #data = get_face_attribute("../data/image/sample.png")
    #os.chdir("/")

    # 後は焼くなり煮るなり好きにしやがれください
    #print(data)
