
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
        self. customerID= StringVar()
        self.createPage()
    
    def createPage(self):
        self.page = Frame(self.root)  # 创建Frame
        self.page.pack()
        Label(self.page).grid(row=0, stick=W)
        Label(self.page, text='ID: ').grid(row=1, stick=W, pady=10)
        Entry(self.page, textvariable=self.customerID).grid(row=1, column=1, stick=E)
        Label(self.page, text='Room Number: ').grid(row=2, stick=W, pady=10)
        Entry(self.page, textvariable=self.roomID).grid(row=2, column=1, stick=E)
        Button(self.page, text='Login', command=self.loginCheck).grid(row=3, stick=W, pady=10)
        Button(self.page, text='Cancel', command=self.loginCancel).grid(row=3, column=1, stick=E)
    
    def loginCheck(self):
        if gl.GlobalVar.GetLoginState()==1:
            customer = self.customerID.get()
            ROOMID = self.roomID.get()
            flag = 0
            if len(customer) != 18:
                flag = 1
            else:
                for i in customer:
                    if (ord(i)<48) or (ord(i) > 57):
                        flag = 1
            if len(ROOMID) != 4:
                flag = 1
            else:
                for i in ROOMID:
                    if (ord(i)<48) or (ord(i) > 57 and ord(i)<65) or (ord(i)>90 and ord(i)<97 ) or (ord(i)>122):
                        flag = 1
            if flag == 0:                
                gl.GlobalVar.SetRoomID(ROOMID)
                dict = {'ID': customer, 'roomID': ROOMID}
                gl.GlobalVar.PutOperBack(dict)
                while gl.GlobalVar.Back_Oper_buff.qsize() == 0:
                    ajshda = 1
                dict = gl.GlobalVar.GetBackOper()
                if dict['type'] == 'login_ack':
                    if dict['result'] == 'succeed':
                        gl.GlobalVar.SetMode(dict['mode'])
                        gl.GlobalVar.SetLoginState(0)
                        tk1 = Tk()
                        tk1.title('MainPage')
                        MainPage(tk1)
                    else:
                        showinfo(title='error', message='Wrong room id or the main constoller is off')
                else:
                    showinfo(title='error', message='Failed to connect main controller')
            else:
                showinfo(title='error', message='Invalid input, please check')
        self.roomID.set('')
        self.customerID.set('')
    
    
    
    def loginCancel(self):
        self.roomID.set('')
        self.customerID.set('')

