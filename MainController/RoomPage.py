from tkinter import *
import sys
import GlobalVar as glo
from MainPage import *
from tkinter.messagebox import *

sys.setrecursionlimit(1000000)

class RoomPage(object):
    #current_expected_temperature = glo.GlobalVar.GetExpect_Temp()
    #current_expected_wind = glo.GlobalVar.GetExpect_wind()
    #wind = 2
    def __init__(self, master=NONE):
        self.root = master  # 定义内部变量root
        self.root.geometry('%dx%d' % (500, 520))  # 设置窗口大小
        self.counttttt = 0
        self.createPage()
        self.room = glo.GlobalVar.GetcurrentRoomID()
    
    def createPage(self):
        self.page = Frame(self.root)  # 创建Frame
        self.page.pack()
        #dict = {'wind_power': "high", 'target_temp': 25, 'current_temp': 28, 'power': 30, 'bill': 18}
        #glo.GlobalVar.PutBackOper(dict)
        while glo.GlobalVar.Back_Oper_buff.qsize() == 0:
            ajshda = 1
        dict = glo.GlobalVar.GetBackOper()
        if 'type' in dict.keys():
            if dict['type'] == 'failed':
                showinfo( message='Failed to connect the room')
                self.root.destroy()
        else:            
            Label(self.page, text='Welcome to Distributed temperature control system').grid(row=1,column=2, pady=50)
            Label(self.page, text='Room ID: ').grid(row=2, stick=W, pady=10)
            Label(self.page, text=glo.GlobalVar.GetcurrentRoomID()).grid(row=2, column=4, stick=E)
            Label(self.page, text='Current Temperature').grid(row=3, stick=W, pady=10)
            Label(self.page, text=dict['current_temp']).grid(row=3, column=4, stick=E)
            Label(self.page, text='Target Temperature ').grid(row=4, stick=W, pady=10)
            temperature = Label(self.page, text=dict['target_temp'])
            temperature.grid(row=4, column=4, stick=E)
            Label(self.page, text='Current Fee ').grid(row=6, stick=W, pady=10)
            Label(self.page, text=dict['bill']).grid(row=6, column=4, stick=E)
            Label(self.page, text='Current Energy ').grid(row=7, stick=W, pady=10)
            Label(self.page, text=dict['power']).grid(row=7, column=4, stick=E)
            Label(self.page, text='Current Mode').grid(row=8, stick=W, pady=10)
            Label(self.page, text=glo.GlobalVar.GetMode()).grid(row=8, column=4, stick=E)
            Label(self.page, text='Current Wind Speed ').grid(row=9, stick=W, pady=10)
            Label(self.page, text=dict['wind_power']).grid(row=9, column=4, stick=E)
            Button(self.page, text='Real Time Refresh', command=self.refreshsh).grid(row=11, stick=W)
            Button(self.page, text='Pay The Bill', command=self.count).grid(row=11, column=4, pady=10)
            Button(self.page, text='Return', command=self.close).grid(row=11, column=2, pady=10)

    def update(self):
        dict = {'type': 'ask', 'roomID': self.room}
        glo.GlobalVar.PutOperBack(dict)
        while glo.GlobalVar.Back_Oper_buff.qsize()==0:
            asaa = 1
        dict = glo.GlobalVar.GetBackOper()
        if 'type' in dict.keys():
            if dict['type'] == 'failed':
                showinfo(title = 'Error', message='Failed to connect the room')
                self.root.destroy()
        else:
            Label(self.page, text='             ').grid(row=3, column=4, stick=E)
            Label(self.page, text=dict['current_temp']).grid(row=3, column=4, stick=E)
            temperature = Label(self.page, text='              ')
            temperature.grid(row=4, column=4, stick=E)
            temperature = Label(self.page, text=dict['target_temp'])
            temperature.grid(row=4, column=4, stick=E)
            Label(self.page, text='               ').grid(row=6, column=4, stick=E)
            Label(self.page, text=dict['bill']).grid(row=6, column=4, stick=E)
            Label(self.page, text='               ').grid(row=7, column=4, stick=E)
            Label(self.page, text=dict['power']).grid(row=7, column=4, stick=E)
            Label(self.page, text='                 ').grid(row=9, column=4, stick=E)
            Label(self.page, text=dict['wind_power']).grid(row=9, column=4, stick=E)
            self.root.after(glo.GlobalVar.GetFrequency(), self.update)
    
    def refreshsh(self):
        if self.counttttt == 0:
            self.counttttt = self.counttttt+1
            self.update()
        else:
            showinfo(title = 'error',message = 'Refresh over frequency')
    
    def close(self):
        glo.GlobalVar.SetLook(1)
        self.root.destroy()
    
    def count(self):
        roo = glo.GlobalVar.GetcurrentRoomID()
        dict = {'type': 'check', 'object':roo}
        glo.GlobalVar.PutOperBack(dict)
        showinfo(title=roo, message='Paid successfully')
        self.root.destroy()

