#GlobalVar.py
from queue import Queue
import sys
import getpass

class GlobalVar():

    Back_Commu_buff = Queue()  # 后台线程和通信线程的信息交互队列
    Commu_Back_buff = Queue()   #通信线程传递给后台线程
    Back_Oper_buff = Queue()
    Oper_Back_buff = Queue()
    Oper_time_buff = Queue()
    login_state = 1
    fee = 0
    power =0
    mode = 'summer'
    expected_wind = 'medium'
    environment_wind=0#有没有送风
    ROOMID = 3322
    environment_temperature = 25
    f = open("temp.txt")
    str1 = f.read()
    lines = str1.split('\n')
    temp = lines[0]
    expected_temperature = int(temp)
    state='close'#开关机
    check=0
    count=0

    def PutBackCommu(dict):
        GlobalVar.Back_Commu_buff.put(dict)
    def GetBackCommu():                                 #读取Back_Commu队列
        return GlobalVar.Back_Commu_buff.get() 
    def GetCommuBack():
        return GlobalVar.Commu_Back_buff.get()
    def PutCommuBack(dict):
        GlobalVar.Commu_Back_buff.put(dict)
    def GetCheck():
        return GlobalVar.check

    def SetCheck(ch):
        GlobalVar.check=ch

    def PutOperBack(dict):                             #放入Oper_Back队列
        GlobalVar.Oper_Back_buff.put(dict)

    def GetBackOper():                                 #读取Back_Oper队列
        return GlobalVar.Back_Oper_buff.get()

    def GetOperBack():                                 #读取Oper_back队列
        return GlobalVar.Oper_Back_buff.get()

    def PutBackOper(a):
        GlobalVar.Back_Oper_buff.put(a)

    def GetState():                     #获取开关机状态
        return GlobalVar.state

    def SetState(S):                  #更改开关机状态
        GlobalVar.state=S

    def SetEnviron_wind(W):                           #有没有送风
        GlobalVar.environment_wind=W

    def GetEnviron_wind():                            #改变有没有送风状态
        return GlobalVar.environment_wind

    def SetRoomID(roomID):                             #修改房间号
        GlobalVar.ROOMID = roomID

    def GetRoomID():                                    #读取房间号
        return GlobalVar.ROOMID

    def GetEnviron_temp():                              #读取当前温度
        return GlobalVar.environment_temperature

    def SetEnviron_temp(e):                             #改变当前温度
        GlobalVar.environment_temperature=e

    def SetWind(windspeed):                              #改变当前风速
        GlobalVar.wind = windspeed

    def GetFee():                                        #读取费用
        return GlobalVar.fee

    def SetFee(f):                                       #修改费用
        GlobalVar.fee= f

    def GetPower():                                        #获取能量
        return GlobalVar.power

    def SetPower(P):                                        #修改能量
        GlobalVar.power=P

    def GetExpect_Temp():                                 #读取目标温度
        return GlobalVar.expected_temperature

    def SetExpect_Temp(d):                                #改变目标温度
        GlobalVar.expected_temperature = d

    def GetExpect_wind():                                 #读取目标风速
        return GlobalVar.expected_wind

    def SetExpect_wind(win):                              #改变目标风速
        GlobalVar.expected_wind = win

    def PutBackOper(a):                                   #放入Back_Oper队列
        GlobalVar.Back_Oper_buff.put(a)

    def GetMode():                                        #读取当前模式
        return GlobalVar.mode

    def SetMode(b):                                        #修改模式
        GlobalVar.mode = b

    def PutOper_time_buff(c):
        GlobalVar.Oper_time_buff.put(c)

    def GetOper_time_buff():
        return GlobalVar.Oper_time_buff.get()

    def GetLoginState():
        return GlobalVar.login_state

    def SetLoginState(f):
        GlobalVar.login_state = f

    def IncCount():
        GlobalVar.count = GlobalVar.count+1

    def GetCount():
        return  GlobalVar.count

