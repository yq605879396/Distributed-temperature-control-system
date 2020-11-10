from tkinter import *
from tkinter.messagebox import *
from LoginPage import *
import sys
import getpass



class StartPage(object):
    def __init__(self, master=None):
        self.root = master  # 定义内部变量root
        self.root.geometry('%dx%d' % (300, 180))  # 设置窗口大小
        self.createPage()

    def createPage(self):
        self.page = Frame(self.root)  # 创建Frame
        self.page.pack()
        Button(self.page, text='Start', command=self.Start).grid(row=3, stick=W, pady=10)

    def Start(self):
        self.page.destroy()
        LoginPage(self.root)