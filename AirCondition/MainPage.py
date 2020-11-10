from tkinter import *
import sys
import GlobalVar as glo
from tkinter.messagebox import *

sys.setrecursionlimit(1000000)

class MainPage(object):
    current_expected_temperature = glo.GlobalVar.GetExpect_Temp()
    current_expected_wind = glo.GlobalVar.GetExpect_wind()
    def __init__(self, master = None):
        self.root = master  # 定义内部变量root
        self.root.geometry('%dx%d' % (500,620))  # 设置窗口大小
        self.count = 0
        self.createPage()

    def createPage(self):
        self.page = Frame(self.root)  # create Frame
        self.page.pack()
        Label(self.page, text='Welcome to Distributed temperature control system').grid(row=1,column=2, pady=50)
        Label(self.page, text='Room ID: ').grid(row=2, stick=W, pady=10)
        Label(self.page, text=glo.GlobalVar.GetRoomID()).grid(row=2, column=4, stick=E)
        Label(self.page, text='Current Temperature ').grid(row=3, stick=W, pady=10)
        Label(self.page, text=glo.GlobalVar.GetEnviron_temp()).grid(row=3, column=4, stick=E)
        Label(self.page, text='Target Temperature ').grid(row=4, stick=W, pady=10)
        temperature = Label(self.page, text=self.current_expected_temperature)
        temperature.grid(row=4, column=4, stick=E)
        Label(self.page, text='Current Fee ').grid(row=6, stick=W, pady=10)
        Label(self.page, text=glo.GlobalVar.GetFee()).grid(row=6, column=4, stick=E)
        Label(self.page, text='Current Energy ').grid(row=7, stick=W, pady=10)
        Label(self.page, text=glo.GlobalVar.GetPower()).grid(row=7, column=4, stick=E)
        Label(self.page, text='Current Mode').grid(row=8, stick=W, pady=10)
        Label(self.page, text=glo.GlobalVar.GetMode()).grid(row=8, column=4, stick=E)
        Label(self.page, text='Current Wind Speed ').grid(row=9, stick=W, pady=10)
        Label(self.page, text=self.current_expected_wind).grid(row=9, column=4, stick=E)
        Button(self.page, text='Increase', command=self.uptemprature).grid(row=5, stick=W, pady=10)
        Button(self.page, text='Decrease', command=self.downtemprature).grid(row=5, column=4, stick=E)
        Button(self.page, text='Low Speed', command=self.change_to_low).grid(row=10, stick=W)
        Button(self.page, text='Mid Speed', command=self.change_to_middle).grid(row=10, column=2)
        Button(self.page, text='High Speed', command=self.change_to_high).grid(row=10, column=4, pady=10)
        Button(self.page, text='Check', command=self.refreshsh).grid(row=11, stick = W)
        Button(self.page, text='Power Off', command=self.close).grid(row=11, column=4, pady=10)


    def uptemprature(self):
        if glo.GlobalVar.GetMode() == 'summer':
            if self.current_expected_temperature<25:
                self.current_expected_temperature = self.current_expected_temperature+1
                Label(self.page, text='    ').grid(row=4, column=4, stick=E)
                Label(self.page, text=self.current_expected_temperature).grid(row=4, column=4, stick=E)
                diction = {'temp': self.current_expected_temperature, 'wind': self.current_expected_wind}
                glo.GlobalVar.PutOper_time_buff(diction)
            else:
                showinfo(title='Warning', message='Stop！！！！！The highest temperature allowed is 25')
        else:
            if self.current_expected_temperature<30:
                self.current_expected_temperature = self.current_expected_temperature+1
                Label(self.page, text='    ').grid(row=4, column=4, stick=E)
                Label(self.page, text=self.current_expected_temperature).grid(row=4, column=4, stick=E)
                diction = {'temp': self.current_expected_temperature, 'wind': self.current_expected_wind}
                glo.GlobalVar.PutOper_time_buff(diction)
            else:
                showinfo(title='Warning', message='Stop！！！！！The highest temperature allowed is 30')

    def downtemprature(self):
        if glo.GlobalVar.GetMode() == 'summer':
            if self.current_expected_temperature>18:
                self.current_expected_temperature = self.current_expected_temperature-1
                Label(self.page, text='     ').grid(row=4, column=4, stick=E)
                Label(self.page, text=self.current_expected_temperature).grid(row=4, column=4, stick=E)
                diction = {'temp': self.current_expected_temperature, 'wind': self.current_expected_wind}
                glo.GlobalVar.PutOper_time_buff(diction)
            else:
                showinfo(title='Warning', message='Stop！！！！！The lowest temperature allowed is 18')
        else:
            if self.current_expected_temperature>25:
                self.current_expected_temperature = self.current_expected_temperature-1
                Label(self.page, text='    ').grid(row=4, column=4, stick=E)
                Label(self.page, text=self.current_expected_temperature).grid(row=4, column=4, stick=E)
                diction = {'temp': self.current_expected_temperature, 'wind': self.current_expected_wind}
                glo.GlobalVar.PutOper_time_buff(diction)
            else:
                showinfo(title='Warning', message='Stop！！！！！The lowest temperature allowed is 25')


    def change_to_low(self):
        self.current_expected_wind = 'low'
        Label(self.page, text='              ').grid(row=9, column=4, stick=E)
        Label(self.page, text=self.current_expected_wind).grid(row=9, column=4, stick=E)
        diction = {'temp': self.current_expected_temperature, 'wind': self.current_expected_wind}
        glo.GlobalVar.PutOper_time_buff(diction)

    def change_to_high(self):
        self.current_expected_wind = 'high'
        Label(self.page, text='            ').grid(row=9, column=4, stick=E)
        Label(self.page, text=self.current_expected_wind).grid(row=9, column=4, stick=E)
        diction = {'temp': self.current_expected_temperature, 'wind': self.current_expected_wind}
        glo.GlobalVar.PutOper_time_buff(diction)

    def change_to_middle(self):
        self.current_expected_wind = 'medium'
        Label(self.page, text='              ').grid(row=9, column=4, stick=E)
        Label(self.page, text=self.current_expected_wind).grid(row=9, column=4, stick=E)
        diction = {'temp': self.current_expected_temperature, 'wind': self.current_expected_wind}
        glo.GlobalVar.PutOper_time_buff(diction)

    def update(self):
        if glo.GlobalVar.GetCheck() == 1:
            glo.GlobalVar.SetLoginState(1)
            showinfo(title='Power Off', message=' The customer paid the bill, power off.')
            sys.exit()

        else:
            Label(self.page, text='                                  ').grid(row=6, column=4, stick=E)
            Label(self.page, text=glo.GlobalVar.GetFee()).grid(row=6, column=4, stick=E)
            Label(self.page, text='                                  ').grid(row=3, column=4, stick=E)
            Label(self.page, text=glo.GlobalVar.GetEnviron_temp()).grid(row=3, column=4, stick=E)
            Label(self.page, text='                          ').grid(row=7, column=4, stick=E)
            Label(self.page, text=glo.GlobalVar.GetPower()).grid(row=7, column=4, stick=E)
            self.root.after(1000, self.update)

    def refreshsh(self):
        if self.count == 0:
            self.count = self.count+1
            self.update()
        else:
            showinfo(title = 'Error', message = 'Refresh over frequency' )


    def close(self):
        self.page.destroy()
        showinfo(title='Power Off', message='The machine has been turn off')
        message = {'state': 'close'}
        glo.GlobalVar.PutOperBack(message)
        glo.GlobalVar.SetLoginState(1)

        self.root.destroy()




