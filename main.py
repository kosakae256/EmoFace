from ui.main import MainUI
from time import sleep

def function():
    return "C:\\Users\\takara2314\\OneDrive\\EmoFace\\data\\image\\pushphoto.png"

if __name__ == '__main__':
    Ui = MainUI(function)
    Ui.root.resizable(width=False, height=False)
    Ui.root.mainloop()
