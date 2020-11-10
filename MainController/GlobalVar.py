#GlobalVar.py
from queue import Queue
import sys
import getpass

class GlobalVar():

    Back_Commu_buff = Queue()  # 后台线程和通信线程的信息交互队列
    Commu_Back_buff = Queue()   #通信线程传递给后台线程
    Oper_Back_buff = Queue()
    Oper_time_buff = Queue()
    Back_Oper_buff = Queue()
    look_auth = 1

    re_fre = 10000     #刷新频率
    currentRoomID = 1234
    def PutOperBack(dict):
        print("b")                             #放入Oper_Back队列
        GlobalVar.Oper_Back_buff.put(dict)
        print(dict)

    def GetBackOper():                                 #读取Back_Oper队列
        return GlobalVar.Back_Oper_buff.get()
    
    def PutBackCommu(dict):
        GlobalVar.Back_Commu_buff.put(dict)
    def GetBackCommu():                                 #读取Back_Commu队列
        return GlobalVar.Back_Commu_buff.get() 
    def GetCommuBack():
        return GlobalVar.Commu_Back_buff.get()
    def PutCommuBack(dict):
        GlobalVar.Commu_Back_buff.put(dict)
    #def GetEnviron_temp():                              #读取当前温度
     #   return GlobalVar.environment_temperature

    #def SetWind(windspeed):                              #改变当前风速
     #   GlobalVar.wind = windspeed

    def PutBackOper(dick1):
        print("a")
        GlobalVar.Back_Oper_buff.put(dick1)
        print(dick1)

    def GetOperBack():
        return GlobalVar.Oper_Back_buff.get()
         

    def GetMode():                                        #读取当前模式
        return GlobalVar.mode

    def SetMode(b):                                        #修改模式
        GlobalVar.mode = b

    #def PutOper_time_buff(c):
        #GlobalVar.Oper_time_buff.put(c)

#    def GetOper_time_buff():
        #return GlobalVar.Oper_time_buff.get()

    def SetPower(e):
        GlobalVar.power = e


 #   def GetPower():
#        return GlobalVar.power

    def SetLoginID(f):
        GlobalVar.LoginID = f

    def GetLoginID():
        return GlobalVar.LoginID

    def SetFrequency(h):
        GlobalVar.re_fre = h

    def GetFrequency():
        return GlobalVar.re_fre

    def SetcurrentRoomID(i):
        GlobalVar.currentRoomID = i

    def GetcurrentRoomID():
        return GlobalVar.currentRoomID

    def SetLook(j):
        GlobalVar.look_auth = j

    def GetLook():
        return  GlobalVar.look_auth