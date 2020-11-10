from tkinter import *
from LoginPage import *
from MainPage import *
from RoomPage import *
from StartPage import *


def Operating():
    root = Tk()
    root.title('Distributed temperature control system')
    StartPage(root)
    root.mainloop()
