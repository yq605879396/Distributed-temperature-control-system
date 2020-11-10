
from tkinter import *
from tkinter.messagebox import *
import time
from MainPage import *
from queue import Queue
import sys
import getpass
import GlobalVar as gl



class LoginPage(object):
    def __init__(self, master=None):
        self.root = master  # 定义内部变量root
        self.root.geometry('%dx%d' % (300, 180))  # 设置窗口大小
        self.roomID = StringVar()
        self.customerID= StringVar()
        self.createPage()

    def createPage(self):
        self.page = Frame(self.root)  # 创建Frame
        self.page.pack()
        Label(self.page).grid(row=0, stick=W)
        Label(self.page, text='Administrator ID: ').grid(row=1, stick=W, pady=10)
        Entry(self.page, textvariable=self.customerID).grid(row=1, column=1, stick=E)
        Label(self.page, text='Password: ').grid(row=2, stick=W, pady=10)
        Entry(self.page, textvariable=self.roomID,show='*').grid(row=2, column=1, stick=E)
        Button(self.page, text='Login', command=self.loginCheck).grid(row=3, stick=W, pady=10)
        Button(self.page, text='Cancel', command=self.loginCancel).grid(row=3, column=1, stick=E)

    def loginCheck(self):
        customer = self.customerID.get()
        ROOMID = self.roomID.get()
        gl.GlobalVar.SetLoginID(customer)
        dict = {'type': 'login','ID': customer, 'password': ROOMID}
        gl.GlobalVar.PutOperBack(dict)
        time.sleep(0.5)
       # dict = {'result': "succeed"}
       # gl.GlobalVar.PutBackOper(dict)
        dict = gl.GlobalVar.GetBackOper()
        if dict['result'] == 'succeed':
            self.page.destroy()
            MainPage(self.root)
        else:
            showinfo(title='Error', message='Wrong ID or Password！')


    def loginCancel(self):
        self.roomID.set('')
        self.customerID.set('')