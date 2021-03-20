from ui.main import MainUI
from time import sleep

def function():
    return "C:/Users/kosakae256/Documents/Kosakae-Deployment/EmoFace/data/image/pushphoto.png"

if __name__ == '__main__':
    Ui = MainUI(function)
    Ui.root.resizable(width=False, height=False)
    Ui.root.mainloop()
