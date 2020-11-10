import time, threading
from socket import *   
from time import ctime  
from queue import Queue
import GlobalVar as g

fee1=0
power1=0
Count=0
stopwind=1

def Backstage():
    global power1
    global fee1
    global Count
    global room
    global password
    global stopwind
    while True:
          while g.GlobalVar.Oper_Back_buff.qsize() > 0:
            dict0 = g.GlobalVar.GetOperBack() #判断从控机有没有登陆上系统
            if  dict0.__contains__('ID'):   #收到登陆请求
               room_id1 = dict0['roomID']
               ID1  = dict0['ID']
               dict1={'type':'login','room_id':room_id1,'id':ID1}
               if Count==0:
                   room = dict0['roomID']
                   password = dict0['ID']
                   g.GlobalVar.PutBackCommu(dict1) #将登陆信息传给主控机
               else:
                   f = open("password.txt")
                   str1 = f.read()
                   lines = str1.split(' ')
                   if dict0['roomID'] == lines[0] and dict0['ID'] == lines[1]:
                       mode1=g.GlobalVar.GetMode()
                       dict3 = {'type':'login_ack','result': 'succeed', 'mode': mode1}
                       g.GlobalVar.PutBackOper(dict3)
                       if g.GlobalVar.GetMode() == 'summer' and g.GlobalVar.GetExpect_Temp() < g.GlobalVar.GetEnviron_temp():
                           dick1 = {'type': 'wind_request', 'wind_power': g.GlobalVar.GetExpect_wind(), 'target_temp': g.GlobalVar.GetExpect_Temp(), 'current_temp': g.GlobalVar.GetEnviron_temp()}  # 传送风请求
                           print(dick1)
                           g.GlobalVar.PutBackCommu(dick1)
                       elif g.GlobalVar.GetMode() == 'winter' and g.GlobalVar.GetExpect_Temp() > g.GlobalVar.GetEnviron_temp():
                           dick1 = {'type': 'wind_request', 'wind_power': g.GlobalVar.GetExpect_wind(),'target_temp': g.GlobalVar.GetExpect_Temp(), 'current_temp': g.GlobalVar.GetEnviron_temp()}  # 传送风请求
                           print(dick1)
                           g.GlobalVar.PutBackCommu(dick1)
                   else:
                       dict3={'result':'failed'}
                       g.GlobalVar.PutBackOper(dict3)
            elif dict0.__contains__('temp'):  #收到送风请求
                temp1=dict0['temp']
                wind1=dict0['wind']
                if g.GlobalVar.GetMode()=='summer'and temp1<g.GlobalVar.GetEnviron_temp():
                  dick1={'type':'wind_request','wind_power':wind1,'target_temp':temp1,'current_temp':g.GlobalVar.GetEnviron_temp()}#传送风请求
                  print(dick1)
                  g.GlobalVar.PutBackCommu(dick1)
                elif g.GlobalVar.GetMode()=='winter' and temp1>g.GlobalVar.GetEnviron_temp():
                    dick1 = {'type': 'wind_request', 'wind_power': wind1, 'target_temp': temp1,'current_temp': g.GlobalVar.GetEnviron_temp()}  # 传送风请求
                    print(dick1)
                    g.GlobalVar.PutBackCommu(dick1)
                else:
                    g.GlobalVar.SetEnviron_wind(0)
            elif dict0.__contains__('state'):   #关机情况
                g.GlobalVar.SetState('close')
                if g.GlobalVar.GetEnviron_wind()==1:
                    dict1 = {'type': 'stop_wind'}
                    g.GlobalVar.PutBackCommu(dict1)
          while g.GlobalVar.Commu_Back_buff.qsize() > 0:# send message to the connection 
            dict2= g.GlobalVar.GetCommuBack()
            print(dict2)
            if dict2['type']=='login_ack':
              if dict2['result'] == 'succeed':
                 g.GlobalVar.SetState(1)
                 g.GlobalVar.SetEnviron_wind(0)
                 outfile = open('password.txt','w')
                 outfile.write(str(room))
                 outfile.write(' ')
                 outfile.write(str(password))
                 outfile.close()
                 Count=Count+1
                 mode1 = dict2['mode']
                 dict3 = {'type':'login_ack','result':'succeed','mode': mode1}  # 模式传给操作界面
                 g.GlobalVar.PutBackOper(dict3)
                 if g.GlobalVar.GetMode()=='summer'and g.GlobalVar.GetExpect_Temp()<g.GlobalVar.GetEnviron_temp():
                     dick1 = {'type': 'wind_request', 'wind_power': g.GlobalVar.GetExpect_wind(), 'target_temp':g.GlobalVar.GetExpect_Temp(),'current_temp': g.GlobalVar.GetEnviron_temp()}  # 传送风请求
                     print(dick1)
                     g.GlobalVar.PutBackCommu(dick1)
                 elif g.GlobalVar.GetMode()=='winter'and g.GlobalVar.GetExpect_Temp()>g.GlobalVar.GetEnviron_temp():
                     dick1 = {'type': 'wind_request', 'wind_power': g.GlobalVar.GetExpect_wind(), 'target_temp': g.GlobalVar.GetExpect_Temp(), 'current_temp': g.GlobalVar.GetEnviron_temp()}  # 传送风请求
                     print(dick1)
                     g.GlobalVar.PutBackCommu(dick1)
              else:
                  g.GlobalVar.SetState('close')
                  g.GlobalVar.SetEnviron_wind(0)  # 若连接失败
                  dict3 = {'type':'login_ack','result': 'failed'}
                  g.GlobalVar.PutBackOper(dict3)
            elif  dict2['type']=='connect':
                  dict3={'type':'connect'}
                  g.GlobalVar.PutBackOper(dict3)
            elif  dict2['type']=='wind_request_ack':
                    if dict2['result']=='succeed':
                        stopwind=0
                        g.GlobalVar.SetEnviron_wind(1)
                    else:
                        g.GlobalVar.SetEnviron_wind(0)
            elif  dict2['type']=='state_query':
                  dict1={'type':'state_query_ack','wind_power':g.GlobalVar.GetExpect_wind(),'target_temp':g.GlobalVar.GetExpect_Temp(),'current_temp':g.GlobalVar.GetEnviron_temp()}
                  g.GlobalVar.PutBackCommu(dict1)
            elif  dict2['type']=='bill':
                  power1=dict2['power']
                  fee1=dict2['money']
                  mode1=dict2['mode']
                  g.GlobalVar.SetMode(mode1)
                  g.GlobalVar.SetPower(power1)
                  g.GlobalVar.SetFee(fee1)
            elif dict2['type']=='stop_wind_ack':
                    g.GlobalVar.SetEnviron_wind(0)
            elif dict2['type']=='check':
                    g.GlobalVar.SetCheck(1)

# a new thread
def BackstageDelays():
    global power1
    global fee1
    global stopwind
    while True:
        if g.GlobalVar.GetEnviron_wind() == 1:
            current_temp=g.GlobalVar.GetEnviron_temp()
            wind = g.GlobalVar.GetExpect_wind()
            if g.GlobalVar.GetMode() == 'summer':
              if(g.GlobalVar.GetExpect_Temp ()< g.GlobalVar.GetEnviron_temp()):
                    stopwind=0
                    if wind == 'low':
                        current_temp = current_temp - 1
                        g.GlobalVar.SetEnviron_temp(current_temp)
                    elif wind == 'medium':
                        current_temp = current_temp - 1
                        if g.GlobalVar.GetExpect_Temp()==current_temp:
                            g.GlobalVar.SetEnviron_temp(current_temp)
                        else:
                            current_temp=current_temp-1
                            g.GlobalVar.SetEnviron_temp(current_temp)
                        print('ruirui')
                    elif wind == 'high':
                        current_temp = current_temp - 1
                        if g.GlobalVar.GetExpect_Temp()==current_temp:
                            g.GlobalVar.SetEnviron_temp(current_temp)
                        else:
                            current_temp=current_temp-1
                            if g.GlobalVar.GetExpect_Temp()==current_temp:
                                current_temp=current_temp-1
                                g.GlobalVar.SetEnviron_temp(current_temp)
                            else:
                                current_temp=current_temp-1
                                g.GlobalVar.SetEnviron_temp(current_temp)
              else:
                    if stopwind==0:
                        dict1 = {'type': 'stop_wind'}
                        g.GlobalVar.PutBackCommu(dict1)
                        stopwind=1
                        print('蛋蛋爱蕊蕊')
            elif g.GlobalVar.GetMode() == 'winter':
              if(g.GlobalVar.GetExpect_Temp() > g.GlobalVar.GetEnviron_temp()):
                    stopwind=0
                    if wind == 'low':
                        current_temp = current_temp + 1
                        g.GlobalVar.SetEnviron_temp(current_temp)
                    elif wind == 'medium':
                        current_temp = current_temp + 1
                        if g.GlobalVar.GetExpect_Temp() == current_temp:
                            g.GlobalVar.SetEnviron_temp(current_temp)
                        else:
                            current_temp = current_temp + 1
                            g.GlobalVar.SetEnviron_temp(current_temp)
                    elif wind == 'high':
                        current_temp = current_temp +1
                        if g.GlobalVar.GetExpect_Temp()==current_temp:
                            g.GlobalVar.SetEnviron_temp(current_temp)
                        else:
                            current_temp=current_temp+1
                            if g.GlobalVar.GetExpect_Temp()==current_temp:
                                current_temp=current_temp-1
                                g.GlobalVar.SetEnviron_temp(current_temp)
                            else:
                                current_temp=current_temp+1
                                g.GlobalVar.SetEnviron_temp(current_temp)
              else:
                  if stopwind == 0:
                      dict1 = {'type': 'stop_wind'}
                      g.GlobalVar.PutBackCommu(dict1)
                      stopwind = 1
        elif g.GlobalVar.GetEnviron_wind()==0 and g.GlobalVar.GetState()==1:
            environ_temp = g.GlobalVar.GetEnviron_temp()
            if g.GlobalVar.GetMode()== 'summer':
                if g.GlobalVar.GetExpect_Temp()  >= environ_temp:
                    environ_temp = environ_temp + 1
                    g.GlobalVar.SetEnviron_temp(environ_temp)
                else:
                    dict1 = {'type': 'wind_request', 'wind_power': g.GlobalVar.GetExpect_wind(),'target_temp': g.GlobalVar.GetExpect_Temp(),'current_temp' : g.GlobalVar.GetEnviron_temp()}  # 传送风请求
                    g.GlobalVar.PutBackCommu(dict1)
            else:
                if  g.GlobalVar.GetExpect_Temp()  <= environ_temp:
                    environ_temp = environ_temp - 1
                    g.GlobalVar.SetEnviron_temp(environ_temp)
                else:
                    dict1 = {'type': 'wind_request', 'wind_power': g.GlobalVar.GetExpect_wind(),'target_temp': g.GlobalVar.GetExpect_Temp(),'current_temp' : g.GlobalVar.GetEnviron_temp()}  # 传送风请求
                    g.GlobalVar.PutBackCommu(dict1)
        elif g.GlobalVar.GetState() == 'close':
            environ_temp = g.GlobalVar.GetEnviron_temp()
            if (g.GlobalVar.GetMode() == 'summer'):
                    environ_temp = environ_temp + 1
                    g.GlobalVar.SetEnviron_temp(environ_temp)
            else:
                    environ_temp = environ_temp - 1
                    g.GlobalVar.SetEnviron_temp(environ_temp)
        time.sleep(20)
