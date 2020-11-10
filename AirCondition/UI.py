from tkinter import *
from LoginPage import *
from MainPage import *
from StartPage import *

def Operating():
    root = Tk()
    root.title('Welcome to Distributed temperature control system')
    StartPage(root)
    root.mainloop()
