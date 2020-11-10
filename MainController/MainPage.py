from tkinter import *
import sys
import GlobalVar as glo
import time
from RoomPage import *
from tkinter.messagebox import *
sys.setrecursionlimit(1000000)

class MainPage(object):
    def __init__(self, master = None):
        self.root = master  # 定义内部变量root
        self.root.geometry('%dx%d' % (500, 520))  # 设置窗口大小
        self.changeRate = StringVar()
        self.changeFrequency = StringVar()
        self.flag = 0
        self.createPage()

    def createPage(self):
        self.page = Frame(self.root)  # 创建Frame
        self.page.pack()
        Label(self.page, text='Welcome to Distributed temperature control system').grid(row=1,column=3, pady=50)
        Label(self.page, text='hello ').grid(row=2, stick=W, pady=10)
        Label(self.page, text=glo.GlobalVar.GetLoginID()).grid(row=2, column=3, stick=E)
        Label(self.page, text='Mode').grid(row=4, stick=W, pady=10)
        Label(self.page, text=glo.GlobalVar.GetMode()).grid(row=4, column=3, pady=10)
        #Button(self.page, text='切换', command=self.ChangeMode).grid(row=4, column=4, pady=10)
        #Label(self.page, text='目标温度 ').grid(row=3, stick=W, pady=10)
        #temperature = Label(self.page, text=glo.GlobalVar.GetExpect_Temp())
        #temperature.grid(row=3, column=4, stick=E)
        #Label(self.page, text='费率 ').grid(row=6, stick=W, pady=10)
        #Entry(self.page, textvariable=self.changeRate).grid(row=6, column=3, padx=2, pady=10)
        #Label(self.page, text=glo.GlobalVar.GetRate()).grid(row=6, column=3, pady = 10)
        #Button(self.page, text='重设', command=self.SetRa).grid(row=6, column=4, pady = 10)
        Label(self.page, text='Refresh Frequency').grid(row=7, stick=W, pady=10)
        Entry(self.page, textvariable=self.changeFrequency).grid(row=7, column=3, pady = 10)
        Label(self.page, text=glo.GlobalVar.GetFrequency()).grid(row=7, column=3, pady = 10)
        Button(self.page, text='Reset', command=self.Setfre).grid(row=7, column=4,pady = 10)
        Label(self.page, text='Room status').grid(row=8, stick=W, pady=10)
        Button(self.page, text='Room1', command=self.OneInformation).grid(row=9, stick=W, pady=10)
        Button(self.page, text='Room2', command=self.TwoInformation).grid(row=9, column=3, pady = 10)
        Button(self.page, text='Room3', command=self.ThreeInformation).grid(row=9, column=4, pady = 10)
        Button(self.page, text='Room4', command=self.FourInformation).grid(row=9, column=7, pady = 10)
        Button(self.page, text='Monthly report', command=self.monthForm).grid(row=11, stick=W, pady=10)
        Button(self.page, text='Weekly report', command=self.weekForm).grid(row=11, column=3, pady = 10)
        Button(self.page, text='Daily report', command=self.dayForm).grid(row=11, column=4, pady = 10)
        Button(self.page, text='Power off', command=self.close).grid(row=11, column=7, pady=10)

    def close(self):
        sys.exit()


    def OneInformation(self):
        lookau = glo.GlobalVar.GetLook()
        if lookau == 1:
            room = '0001'
            glo.GlobalVar.SetcurrentRoomID(room)
            dict = {'type': 'ask', 'roomID': room}
            glo.GlobalVar.PutOperBack(dict)
            time.sleep(2)
            tk = Tk()
            tk.title('Room')
            glo.GlobalVar.SetLook(0)
            RoomPage(tk)

    def TwoInformation(self):
        lookau = glo.GlobalVar.GetLook()
        if lookau == 1:
            room = '0002'
            glo.GlobalVar.SetcurrentRoomID(room)
            dict = {'type': 'ask', 'roomID': room}
            glo.GlobalVar.PutOperBack(dict)
            time.sleep(2)
            tk2 = Tk()
            tk2.title('Room')
            glo.GlobalVar.SetLook(0)
            RoomPage(tk2)

    def ThreeInformation(self):
        lookau = glo.GlobalVar.GetLook()
        if lookau == 1:
            room = '0003'
            glo.GlobalVar.SetcurrentRoomID(room)
            dict = {'type': 'ask', 'roomID': room}
            glo.GlobalVar.PutOperBack(dict)
            time.sleep(2)
            tk3 = Tk()
            tk3.title('Room')
            glo.GlobalVar.SetLook(0)
            RoomPage(tk3)

    def FourInformation(self):
        lookau = glo.GlobalVar.GetLook()
        if lookau == 1:
            room = '0004'
            glo.GlobalVar.SetcurrentRoomID(room)
            dict = {'type': 'ask', 'roomID': room}
            glo.GlobalVar.PutOperBack(dict)
            time.sleep(2)
            tk4 = Tk()
            tk4.title('Room')
            glo.GlobalVar.SetLook(0)
            RoomPage(tk4)


    def SetRa(self):
        count_a=count_o=count_s=count_z=count_y=0
        if self.flag == 0:
            Label(self.page, text='                   ').grid(row=6, column=3, padx=2, pady=10)
            Entry(self.page, textvariable=self.changeRate).grid(row=6, column=3,padx=2, pady=10)
            self.flag = 1
        else:
            rrate = self.changeRate.get()
            self.flag = 0
            for i in rrate:

                if (ord(i) >= 97 and ord(i) <= 122) or (ord(i) >= 65 and ord(i) <= 90):
                    count_a = count_a + 1
                elif ord(i) >= 48 and ord(i) <= 57:
                    count_z = count_z + 1
                elif ord(i) == 32:
                    count_s = count_s + 1
                elif ord(i) == 46:
                    print("1")
                    count_y = count_y+1
                else:
                    count_o = count_o + 1
            if count_a!=0 or count_y>=2 or count_o!=0:
                showinfo(title='Wrong input', message='Invalid input, please check.')

            else:
                glo.GlobalVar.SetRate(rrate)
            self.changeRate.set(' ')
            Label(self.page, text='                         ').grid(row=6, column=3, padx=2, pady=10)
            Label(self.page, text=glo.GlobalVar.GetRate()).grid(row=6, column=3, padx=2, pady=10)

    def Setfre(self):
        count_a = count_o = count_s = count_z = count_y = 0
        if self.flag == 0:
            Label(self.page, text='                   ').grid(row=7, column=3, padx=2, pady=10)
            Entry(self.page, textvariable=self.changeFrequency).grid(row=7, column=3, padx=2, pady=10)
            self.flag = 1
        else:
            ffre = self.changeFrequency.get()
            for i in ffre:

                if (ord(i) >= 97 and ord(i) <= 122) or (ord(i) >= 65 and ord(i) <= 90):
                    count_a = count_a + 1
                elif ord(i) >= 48 and ord(i) <= 57:
                    count_z = count_z + 1
                elif ord(i) == 32:
                    count_s = count_s + 1
                elif ord(i) == 46:
                    count_y = count_y + 1
                else:
                    count_o = count_o + 1
            if count_a != 0 or count_y >= 2 or count_o != 0:
                showinfo(title='Wrong input', message='Invalid input, please check.')

            else:
                glo.GlobalVar.SetFrequency(ffre)
            self.changeFrequency.set(' ')
            Label(self.page, text='                             ').grid(row=7, column=3, padx=2, pady=10)
            Label(self.page, text=glo.GlobalVar.GetFrequency()).grid(row=7, column=3, padx=2, pady=10)

    def ChangeMode(self):
        if glo.GlobalVar.GetMode() == 'summer':
            glo.GlobalVar.SetMode('winter')
            print(glo.GlobalVar.GetMode())
        else:
            glo.GlobalVar.SetMode('summer')
            print(glo.GlobalVar.GetMode())
        Label(self.page, text='               ').grid(row=4, column=3, pady=10)
        Label(self.page, text=glo.GlobalVar.GetMode()).grid(row=4, column=3, pady=10)

    def monthForm(self):
        dict = {'type': 'AskForm', 'FormKind': 'month', 'object': 'all'}
        glo.GlobalVar.PutOperBack(dict)

    def weekForm(self):
        dict = {'type': 'AskForm', 'FormKind': 'week', 'object': 'all'}
        glo.GlobalVar.PutOperBack(dict)

    def dayForm(self):
        dict = {'type': 'AskForm', 'FormKind': 'day', 'object': 'all'}
        glo.GlobalVar.PutOperBack(dict)


