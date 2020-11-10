import time, threading
import datetime
from socket import *   
from time import ctime  
from queue import Queue
import GlobalVar as g
from Charts import *


f = open("roomid.txt")
str1 = f.read()
lines = str1.split('\n')
mode=lines[4]
g.GlobalVar.SetMode(mode)

wind_room=0 #正在送风的房间数量
room=[0,0,0,0]
wind=[0,0,0,0]
class ROOM:
    def __init__(self):
        self.roomid =0    
        self.expect_temp = 25
        self.expect_wind = 'high'
        self.environ_temp=25
        self.current_wind='high'
        self.power=0
        self.fee=0
        self.ack=0
room[0]=ROOM()
room[1]=ROOM()
room[2]=ROOM()
room[3]=ROOM()
login=0
roomstate=[]

def TimeCut(Time_low,Time_high,datas):
    newdatas = []
    for data in datas:
        if data['time'].strftime("%Y-%m-%d") <= Time_high.strftime("%Y-%m-%d") and data['time'].strftime("%Y-%m-%d") >= Time_low.strftime("%Y-%m-%d"):
            newdatas.append(data)
    return newdatas

def Backstage():
    global wind_room
    global ROOM
    global wind
    global room
    global login
    while True:
        while g.GlobalVar.Oper_Back_buff.qsize() > 0:
            dict0 = g.GlobalVar.GetOperBack()
            print(dict0)
            if dict0['type']=='login':
                id=dict0['ID']
                Password=dict0['password']
                f = open("roomid.txt")
                str1= f.read()
                lines = str1.split('\n')
                if id==lines[5] and Password==lines[6]:
                    dict1={'result':'succeed'}
                    print(dict1)
                    g.GlobalVar.PutBackOper(dict1)
                    login=1
                else:
                    dict1={'result':'fail'}
                    g.GlobalVar.PutBackOper(dict1)
            elif dict0['type']=='ask':
                roomstate.reverse()
                roomId=dict0['roomID']
                if roomId==room[0].roomid and room[0].ack==1:
                 length = 0
                 while True:
                    dict4=roomstate[length]
                    if dict4['roomid']==roomId:
                        g.GlobalVar.PutBackOper(dict4)
                        break
                    else:
                        length=length+1
                if roomId==room[1].roomid and room[1].ack==1:
                  length = 0
                  while True:
                    dict4=roomstate[length]
                    if dict4['roomid']==roomId:
                        g.GlobalVar.PutBackOper(dict4)
                        break
                    else:
                        length=length+1
                if roomId==room[2].roomid and room[2].ack==1:
                  length = 0
                  while True:
                    dict4=roomstate[length]
                    if dict4['roomid']==roomId:
                        g.GlobalVar.PutBackOper(dict4)
                        break
                    else:
                        length=length+1
                if roomId==room[3].roomid and room[3].ack==1:
                  length = 0
                  while True:
                    dict4=roomstate[length]
                    if dict4['roomid']==roomId:
                        g.GlobalVar.PutBackOper(dict4)
                        break
                    else:
                        length=length+1
                if roomId!=room[0].roomid and roomId!=room[1].roomid and roomId!=room[2].roomid and roomId!=room[3].roomid:
                  dict4={'type':'failed'}
                  g.GlobalVar.PutBackOper(dict4)
            elif dict0['type']=='check':
                roomId=dict0['object']
                dict3={'type':'check','room_id':roomId}
                g.GlobalVar.PutBackCommu(dict3)
                if room[0].room_id==roomId:
                    room[0]=ROOM()
                    ack[0] = 0
                elif room[1].room_id == roomId:
                    room[1] = ROOM()
                    ack[1] = 0
                elif room[2].room_id == roomId:
                    room[2] = ROOM()
                    ack[2] = 0
                elif room[3].room_id == roomId:
                    room[3] = ROOM()
                    ack[3] = 0
            elif dict0.get('type')=='AskForm':
               Report = open('report.txt','r')
               str_report = Report.read()
               r_lines = str_report.split('\n')
               r_lines.pop()
               print(r_lines)
               datas = []
               for r_line in r_lines:
                 data = {}
                 lineList = r_line.split(' ')
                 data['state'] = lineList[0]
                 data['room_id'] = float(lineList[1])
                 data['expect_temp'] = float(lineList[2])
                 data['current_temp'] = float(lineList[3])
                 data['expect_wind'] = float(lineList[2])
                 if lineList[4] == 'low':
                   data['expect_wind'] = 1
                 elif lineList[4] == 'medium':
                   data['expect_wind'] = 2
                 elif lineList[4] == 'high':
                   data['expect_wind'] = 3
                 if lineList[5] == 'low':
                   data['current_wind'] = 1
                 elif lineList[5] == 'medium':
                   data['current_wind'] = 2
                 elif lineList[5] == 'high':
                   data['current_wind'] = 3
                 data['power'] = float(lineList[6])
                 data['fee'] = float(lineList[7])
                 data['time'] = datetime.datetime.strptime(lineList[8],"%Y-%m-%d-%H:%M")
                 datas.append(data)
               if dict0['FormKind']=='day':
                   today = datetime.date.today()
                   oneday = datetime.timedelta(days=1)
                   yesterday = today - oneday
                   datas = TimeCut(yesterday, today, datas)
                   print(datas)
                   DayCharts(datas)
               elif dict0['FormKind']=='week':
                   today = datetime.date.today()
                   weekday = datetime.datetime.now() - datetime.timedelta(days=7)
                   datas = TimeCut(weekday, today, datas)
                   WeekCharts(datas)
               elif dict0['FormKind']=='month':
                   today = datetime.date.today()
                   monthday = datetime.datetime.now() - datetime.timedelta(days=30)
                   datas = TimeCut(monthday, today, datas)
                   MonthCharts(datas)

        while g.GlobalVar.Commu_Back_buff.qsize() > 0 :
            dict2=g.GlobalVar.GetCommuBack()

            if dict2['type']=='login':
                roomId=dict2['room_id']
                f = open("roomid.txt")
                str1 = f.read()
                lines = str1.split('\n')
                if roomId!=room[1].roomid and roomId!=room[2].roomid and roomId!=room[3].roomid and roomId!=room[0].roomid:
                 if login==1 and roomId==lines[0] or roomId==lines[1] or roomId==lines[2] or roomId==lines[3] :
                      dict3={'type':'login_ack','room_id':roomId,'result':'succeed','mode':g.GlobalVar.GetMode()}
                      g.GlobalVar.PutBackCommu(dict3)
                      if room[0].roomid==0:
                          room[0].ack = 1
                          room[0].roomid=roomId
                      elif room[1].roomid==0:
                          room[1].ack = 1
                          room[1].roomid = roomId
                      elif room[2].roomid==0:
                          room[2].ack = 1
                          room[2].roomid = roomId
                      elif room[3].roomid==0:
                          room[3].ack = 1
                          room[3].roomid = roomId
                 elif login==0:
                      dict3 = {'type': 'login_ack', 'room_id': roomId, 'result': 'failed', 'mode': g.GlobalVar.GetMode()}
                      g.GlobalVar.PutBackCommu(dict3)
                else:
                      dict3 = {'type': 'login_ack', 'room_id': roomId, 'result': 'failed','mode':g.GlobalVar.GetMode()}
                      g.GlobalVar.PutBackCommu(dict3)

            elif dict2['type']=='wind_request':
                roomId = dict2['room_id']
                if wind[0]==1 and roomId==room[0].roomid:
                    dict3 = {'type': 'wind_request_ack', 'room_id': roomId, 'result': 'succeed'}
                    g.GlobalVar.PutBackCommu(dict3)
                    nowtime = time.strftime('%Y-%m-%d-%H:%M', time.localtime(time.time()))
                    room[0].expect_wind = room[0].current_wind = dict2['wind_power']
                    room[0].expect_temp = dict2['target_temp']
                    room[0].environ_temp = dict2['current_temp']
                    outfile = open('report.txt', 'a')
                    outfile.write('False ')
                    outfile.write(str(room[0].roomid))
                    outfile.write(' ')
                    outfile.write(str(room[0].expect_temp))
                    outfile.write(' ')
                    outfile.write(str(room[0].environ_temp))
                    outfile.write(' ')
                    outfile.write(str(room[0].expect_wind))
                    outfile.write(' ')
                    outfile.write(str(room[0].current_wind))
                    outfile.write(' ')
                    outfile.write(str(room[0].power))
                    outfile.write(' ')
                    outfile.write(str(room[0].fee))
                    outfile.write(' ')
                    outfile.write(str(nowtime))
                    outfile.write('\n')
                    outfile.write('True ')
                    outfile.write(str(room[0].roomid))
                    outfile.write(' ')
                    outfile.write(str(room[0].expect_temp))
                    outfile.write(' ')
                    outfile.write(str(room[0].environ_temp))
                    outfile.write(' ')
                    outfile.write(str(room[0].expect_wind))
                    outfile.write(' ')
                    outfile.write(str(room[0].current_wind))
                    outfile.write(' ')
                    outfile.write(str(room[0].power))
                    outfile.write(' ')
                    outfile.write(str(room[0].fee))
                    outfile.write(' ')
                    outfile.write(str(nowtime))
                    outfile.write('\n')
                    outfile.close()

                if wind[1]==1 and roomId==room[1].roomid:
                    dict3 = {'type': 'wind_request_ack', 'room_id': roomId, 'result': 'succeed'}
                    g.GlobalVar.PutBackCommu(dict3)
                    nowtime = time.strftime('%Y-%m-%d-%H:%M', time.localtime(time.time()))
                    room[1].expect_wind = room[1].current_wind = dict2['wind_power']
                    room[1].expect_temp = dict2['target_temp']
                    room[1].environ_temp = dict2['current_temp']
                    outfile = open('report.txt', 'a')
                    outfile.write('False ')
                    outfile.write(str(room[1].roomid))
                    outfile.write(' ')
                    outfile.write(str(room[1].expect_temp))
                    outfile.write(' ')
                    outfile.write(str(room[1].environ_temp))
                    outfile.write(' ')
                    outfile.write(str(room[1].expect_wind))
                    outfile.write(' ')
                    outfile.write(str(room[1].current_wind))
                    outfile.write(' ')
                    outfile.write(str(room[1].power))
                    outfile.write(' ')
                    outfile.write(str(room[1].fee))
                    outfile.write(' ')
                    outfile.write(str(nowtime))
                    outfile.write('\n')
                    outfile.write('True ')
                    outfile.write(str(room[1].roomid))
                    outfile.write(' ')
                    outfile.write(str(room[1].expect_temp))
                    outfile.write(' ')
                    outfile.write(str(room[1].environ_temp))
                    outfile.write(' ')
                    outfile.write(str(room[1].expect_wind))
                    outfile.write(' ')
                    outfile.write(str(room[1].current_wind))
                    outfile.write(' ')
                    outfile.write(str(room[1].power))
                    outfile.write(' ')
                    outfile.write(str(room[1].fee))
                    outfile.write(' ')
                    outfile.write(str(nowtime))
                    outfile.write('\n')
                    outfile.close()

                if wind[2]==1 and roomId==room[2].roomid:
                    dict3 = {'type': 'wind_request_ack', 'room_id': roomId, 'result': 'succeed'}
                    g.GlobalVar.PutBackCommu(dict3)
                    nowtime = time.strftime('%Y-%m-%d-%H:%M', time.localtime(time.time()))
                    room[2].expect_wind = room[2].current_wind = dict2['wind_power']
                    room[2].expect_temp = dict2['target_temp']
                    room[2].environ_temp = dict2['current_temp']
                    outfile = open('report.txt', 'a')
                    outfile.write('False ')
                    outfile.write(str(room[2].roomid))
                    outfile.write(' ')
                    outfile.write(str(room[2].expect_temp))
                    outfile.write(' ')
                    outfile.write(str(room[2].environ_temp))
                    outfile.write(' ')
                    outfile.write(str(room[2].expect_wind))
                    outfile.write(' ')
                    outfile.write(str(room[2].current_wind))
                    outfile.write(' ')
                    outfile.write(str(room[2].power))
                    outfile.write(' ')
                    outfile.write(str(room[2].fee))
                    outfile.write(' ')
                    outfile.write(str(nowtime))
                    outfile.write('\n')
                    outfile.write('True ')
                    outfile.write(str(room[2].roomid))
                    outfile.write(' ')
                    outfile.write(str(room[2].expect_temp))
                    outfile.write(' ')
                    outfile.write(str(room[2].environ_temp))
                    outfile.write(' ')
                    outfile.write(str(room[2].expect_wind))
                    outfile.write(' ')
                    outfile.write(str(room[2].current_wind))
                    outfile.write(' ')
                    outfile.write(str(room[2].power))
                    outfile.write(' ')
                    outfile.write(str(room[2].fee))
                    outfile.write(' ')
                    outfile.write(str(nowtime))
                    outfile.write('\n')
                    outfile.close()

                if wind[3]==1 and roomId==room[3].roomid:
                    dict3 = {'type': 'wind_request_ack', 'room_id': roomId, 'result': 'succeed'}
                    g.GlobalVar.PutBackCommu(dict3)
                    nowtime = time.strftime('%Y-%m-%d-%H:%M', time.localtime(time.time()))
                    room[3].expect_wind = room[3].current_wind = dict2['wind_power']
                    room[3].expect_temp = dict2['target_temp']
                    room[3].environ_temp = dict2['current_temp']
                    outfile = open('report.txt', 'a')
                    outfile.write('False ')
                    outfile.write(str(room[3].roomid))
                    outfile.write(' ')
                    outfile.write(str(room[3].expect_temp))
                    outfile.write(' ')
                    outfile.write(str(room[3].environ_temp))
                    outfile.write(' ')
                    outfile.write(str(room[3].expect_wind))
                    outfile.write(' ')
                    outfile.write(str(room[3].current_wind))
                    outfile.write(' ')
                    outfile.write(str(room[3].power))
                    outfile.write(' ')
                    outfile.write(str(room[3].fee))
                    outfile.write(' ')
                    outfile.write(str(nowtime))
                    outfile.write('\n')
                    outfile.write('True ')
                    outfile.write(str(room[3].roomid))
                    outfile.write(' ')
                    outfile.write(str(room[3].expect_temp))
                    outfile.write(' ')
                    outfile.write(str(room[3].environ_temp))
                    outfile.write(' ')
                    outfile.write(str(room[3].expect_wind))
                    outfile.write(' ')
                    outfile.write(str(room[3].current_wind))
                    outfile.write(' ')
                    outfile.write(str(room[3].power))
                    outfile.write(' ')
                    outfile.write(str(room[3].fee))
                    outfile.write(' ')
                    outfile.write(str(nowtime))
                    outfile.write('\n')
                    outfile.close()

                elif wind_room<3:
                       dict3={'type':'wind_request_ack','room_id':roomId,'result':'succeed'}
                       wind_room=wind_room+1
                       g.GlobalVar.PutBackCommu(dict3)
                       if  room[0].roomid==roomId:
                           print(room[0].roomid)
                           wind[0]=1
                           nowtime=time.strftime('%Y-%m-%d-%H:%M',time.localtime(time.time()))
                           room[0].expect_wind=room[0].current_wind=dict2['wind_power']
                           room[0].expect_temp=dict2['target_temp']
                           room[0].environ_temp=dict2['current_temp']
                           outfile = open('report.txt', 'a')
                           outfile.write('True ')
                           outfile.write(str(room[0].roomid))
                           outfile.write(' ')
                           outfile.write(str(room[0].expect_temp))
                           outfile.write(' ')
                           outfile.write(str(room[0].environ_temp))
                           outfile.write(' ')
                           outfile.write(str(room[0].expect_wind))
                           outfile.write(' ')
                           outfile.write(str(room[0].current_wind))
                           outfile.write(' ')
                           outfile.write(str(room[0].power))
                           outfile.write(' ')
                           outfile.write(str(room[0].fee))
                           outfile.write(' ')
                           outfile.write(str(nowtime))
                           outfile.write('\n')
                           outfile.close()
                           dict1 = {'roomid': roomId, 'wind_power': room[0].expect_wind, 'target_temp': room[0].expect_temp, 'current_temp': room[0].environ_temp,'power': room[0].power, 'bill': room[0].fee}
                           roomstate.append(dict1)
                       if room[1].roomid==roomId:
                          wind[1] = 1
                          nowtime = time.strftime('%Y-%m-%d-%H:%M', time.localtime(time.time()))
                          room[1].expect_wind = room[1].current_wind = dict2['wind_power']
                          room[1].expect_temp = dict2['target_temp']
                          room[1].environ_temp = dict2['current_temp']
                          outfile = open('report.txt', 'a')
                          outfile.write('True ')
                          outfile.write(str(room[1].roomid))
                          outfile.write(' ')
                          outfile.write(str(room[1].expect_temp))
                          outfile.write(' ')
                          outfile.write(str(room[1].environ_temp))
                          outfile.write(' ')
                          outfile.write(str(room[1].expect_wind))
                          outfile.write(' ')
                          outfile.write(str(room[1].current_wind))
                          outfile.write(' ')
                          outfile.write(str(room[1].power))
                          outfile.write(' ')
                          outfile.write(str(room[1].fee))
                          outfile.write(' ')
                          outfile.write(str(nowtime))
                          outfile.write('\n')
                          outfile.close()
                          dict1 = {'roomid': roomId, 'wind_power': room[1].expect_wind,'target_temp': room[1].expect_temp, 'current_temp': room[1].environ_temp,'power': room[1].power, 'bill': room[1].fee}
                          roomstate.append(dict1)

                       if room[2].roomid==roomId:
                          wind[2] = 1
                          nowtime = time.strftime('%Y-%m-%d-%H:%M', time.localtime(time.time()))
                          room[2].expect_wind = room[1].current_wind = dict2['wind_power']
                          room[2].expect_temp = dict2['target_temp']
                          room[2].environ_temp = dict2['current_temp']
                          outfile = open('report.txt', 'a')
                          outfile.write('True ')
                          outfile.write(str(room[2].roomid))
                          outfile.write(' ')
                          outfile.write(str(room[2].expect_temp))
                          outfile.write(' ')
                          outfile.write(str(room[2].environ_temp))
                          outfile.write(' ')
                          outfile.write(str(room[2].expect_wind))
                          outfile.write(' ')
                          outfile.write(str(room[2].current_wind))
                          outfile.write(' ')
                          outfile.write(str(room[2].power))
                          outfile.write(' ')
                          outfile.write(str(room[2].fee))
                          outfile.write(' ')
                          outfile.write(str(nowtime))
                          outfile.write('\n')
                          outfile.close()
                          dict1 = {'roomid': roomId, 'wind_power': room[2].expect_wind,'target_temp': room[2].expect_temp, 'current_temp': room[2].environ_temp,'power': room[2].power, 'bill': room[2].fee}
                          roomstate.append(dict1)

                       if room[3].roomid==roomId:
                          wind[3] = 1
                          nowtime = time.strftime('%Y-%m-%d-%H:%M', time.localtime(time.time()))
                          room[3].expect_wind = room[3].current_wind = dict2['wind_power']
                          room[3].expect_temp = dict2['target_temp']
                          room[3].environ_temp = dict2['current_temp']
                          outfile = open('report.txt', 'a')
                          outfile.write('True ')
                          outfile.write(str(room[3].roomid))
                          outfile.write(' ')
                          outfile.write(str(room[3].expect_temp))
                          outfile.write(' ')
                          outfile.write(str(room[3].environ_temp))
                          outfile.write(' ')
                          outfile.write(str(room[3].expect_wind))
                          outfile.write(' ')
                          outfile.write(str(room[3].current_wind))
                          outfile.write(' ')
                          outfile.write(str(room[3].power))
                          outfile.write(' ')
                          outfile.write(str(room[3].fee))
                          outfile.write(' ')
                          outfile.write(str(nowtime))
                          outfile.write('\n')
                          outfile.close()
                          dict1 = {'roomid': roomId, 'wind_power': room[3].expect_wind,'target_temp': room[3].expect_temp, 'current_temp': room[3].environ_temp,'power': room[3].power, 'bill': room[3].fee}
                          roomstate.append(dict1)
                else:
                        roomId=dict2['room_id']
                        dict3={'type':'wind_request_ack','room_id':roomId,'result':'failed'}
                        g.GlobalVar.PutBackCommu(dict3)
            elif dict2['type']=='stop_wind':
                    roomId=dict2['room_id']
                    dict3={'type':'stop_wind_ack','room_id':roomId}
                    g.GlobalVar.PutBackCommu(dict3)
                    wind_room=wind_room-1
                    roomstate.reverse()
                    length = 0
                    while True:
                        dict4 = roomstate[length]
                        if dict4['roomid'] == roomId:
                            g.GlobalVar.PutBackOper(dict4)
                            break
                        else:
                            length = length + 1
                    if room[0].roomid == roomId:
                        wind[0] = 0
                        nowtime = time.strftime('%Y-%m-%d-%H:%M', time.localtime(time.time()))
                        room[0].expect_wind = room[0].current_wind = dict4['wind_power']
                        room[0].expect_temp = dict4['target_temp']
                        room[0].environ_temp = dict4['current_temp']
                        outfile = open('report.txt', 'a')
                        outfile.write('False ')
                        outfile.write(str(room[0].roomid))
                        outfile.write(' ')
                        outfile.write(str(room[0].expect_temp))
                        outfile.write(' ')
                        outfile.write(str(room[0].environ_temp))
                        outfile.write(' ')
                        outfile.write(str(room[0].expect_wind))
                        outfile.write(' ')
                        outfile.write(str(room[0].current_wind))
                        outfile.write(' ')
                        outfile.write(str(room[0].power))
                        outfile.write(' ')
                        outfile.write(str(room[0].fee))
                        outfile.write(' ')
                        outfile.write(str(nowtime))
                        outfile.write('\n')
                        outfile.close()
                    if room[1].roomid == roomId:
                        wind[1] = 0
                        nowtime = time.strftime('%Y-%m-%d-%H:%M', time.localtime(time.time()))
                        room[1].expect_wind = room[1].current_wind = dict4['wind_power']
                        room[1].expect_temp = dict4['target_temp']
                        room[1].environ_temp = dict4['current_temp']
                        outfile = open('report.txt', 'a')
                        outfile.write('False ')
                        outfile.write(str(room[1].roomid))
                        outfile.write(' ')
                        outfile.write(str(room[1].expect_temp))
                        outfile.write(' ')
                        outfile.write(str(room[1].environ_temp))
                        outfile.write(' ')
                        outfile.write(str(room[1].expect_wind))
                        outfile.write(' ')
                        outfile.write(str(room[1].current_wind))
                        outfile.write(' ')
                        outfile.write(str(room[1].power))
                        outfile.write(' ')
                        outfile.write(str(room[1].fee))
                        outfile.write(' ')
                        outfile.write(str(nowtime))
                        outfile.write('\n')
                        outfile.close()
                    if room[2].roomid == roomId:
                        wind[2] = 0
                        nowtime = time.strftime('%Y-%m-%d-%H:%M', time.localtime(time.time()))
                        room[2].expect_wind = room[1].current_wind = dict4['wind_power']
                        room[2].expect_temp = dict4['target_temp']
                        room[2].environ_temp = dict4['current_temp']
                        outfile = open('report.txt', 'a')
                        outfile.write('Fales ')
                        outfile.write(str(room[2].roomid))
                        outfile.write(' ')
                        outfile.write(str(room[2].expect_temp))
                        outfile.write(' ')
                        outfile.write(str(room[2].environ_temp))
                        outfile.write(' ')
                        outfile.write(str(room[2].expect_wind))
                        outfile.write(' ')
                        outfile.write(str(room[2].current_wind))
                        outfile.write(' ')
                        outfile.write(str(room[2].power))
                        outfile.write(' ')
                        outfile.write(str(room[2].fee))
                        outfile.write(' ')
                        outfile.write(str(nowtime))
                        outfile.write('\n')
                        outfile.close()
                    if room[3].roomid == roomId:
                        wind[3] = 0
                        nowtime = time.strftime('%Y-%m-%d-%H:%M', time.localtime(time.time()))
                        room[3].expect_wind = room[3].current_wind = dict4['wind_power']
                        room[3].expect_temp = dict4['target_temp']
                        room[3].environ_temp = dict4['current_temp']
                        outfile = open('report.txt', 'a')
                        outfile.write('False ')
                        outfile.write(str(room[3].roomid))
                        outfile.write(' ')
                        outfile.write(str(room[3].expect_temp))
                        outfile.write(' ')
                        outfile.write(str(room[3].environ_temp))
                        outfile.write(' ')
                        outfile.write(str(room[3].expect_wind))
                        outfile.write(' ')
                        outfile.write(str(room[3].current_wind))
                        outfile.write(' ')
                        outfile.write(str(room[3].power))
                        outfile.write(' ')
                        outfile.write(str(room[3].fee))
                        outfile.write(' ')
                        outfile.write(str(nowtime))
                        outfile.write('\n')
                        outfile.close()
                        
            elif dict2['type']=='state_query_ack':
                    roomId=dict2['room_id']
                    if room[0].roomid == roomId:
                        room[0].expect_temp=dict2['target_temp']
                        room[0].environ_temp=dict2['current_temp']
                        room[0].expect_wind=dict2['wind_power']
                        dict1={'roomid':roomId,'wind_power':room[0].expect_wind,'target_temp':room[0].expect_temp,'current_temp':room[0].environ_temp,'power':room[0].power,'bill':room[0].fee}
                        roomstate.append(dict1)
                    if room[1].roomid == roomId:
                        room[1].expect_temp = dict2['target_temp']
                        room[1].environ_temp = dict2['current_temp']
                        room[1].expect_wind = dict2['wind_power']
                        dict1 = {'roomid':roomId,'wind_power': room[1].expect_wind, 'target_temp': room[1].expect_temp,'current_temp': room[1].environ_temp, 'power': room[1].power, 'bill':room[1].fee}
                        roomstate.append(dict1)
                    if room[2].roomid == roomId:
                        room[2].expect_temp = dict2['target_temp']
                        room[2].environ_temp = dict2['current_temp']
                        room[2].expect_wind = dict2['wind_power']
                        dict1 = {'roomid':roomId,'wind_power': room[2].expect_wind, 'target_temp': room[2].expect_temp,'current_temp': room[2].environ_temp, 'power': room[2].power, 'bill':room[2].fee}
                        roomstate.append(dict1)
                    if room[3].roomid == roomId:
                        room[3].expect_temp = dict2['target_temp']
                        room[3].environ_temp = dict2['current_temp']
                        room[3].expect_wind = dict2['wind_power']
                        dict1 = {'roomid':roomId,'wind_power': room[3].expect_wind, 'target_temp': room[3].expect_temp,'current_temp': room[3].environ_temp, 'power': room[3].power, 'bill':room[3].fee}
                        roomstate.append(dict1)

def BackstageDelays():
    global ROOM
    global wind
    global room
    while True:

        if room[0].roomid !=0  :
            dict3={'type':'bill','room_id':room[0].roomid,'power':room[0].power,'money':room[0].fee,'mode':g.GlobalVar.GetMode()}
            g.GlobalVar.PutBackCommu(dict3)
            dict2={'type':'state_query','room_id':room[0].roomid}
            g.GlobalVar.PutBackCommu(dict2)
        if room[1].roomid !=0 :
            dict3={'type':'bill','room_id':room[1].roomid,'power':room[1].power,'money':room[1].fee,'mode':g.GlobalVar.GetMode()}
            g.GlobalVar.PutBackCommu(dict3)
            dict2 = {'type': 'state_query', 'room_id': room[1].roomid}
            g.GlobalVar.PutBackCommu(dict2)
        if room[2].roomid !=0:
            dict3={'type':'bill','room_id':room[2].roomid,'power':room[2].power,'money':room[2].fee,'mode':g.GlobalVar.GetMode()}
            g.GlobalVar.PutBackCommu(dict3)
            dict2 = {'type': 'state_query', 'room_id': room[2].roomid}
            g.GlobalVar.PutBackCommu(dict2)
        if room[3].roomid !=0 :
            dict3={'type':'bill','room_id':room[3].roomid,'power':room[3].power,'money':room[3].fee,'mode':g.GlobalVar.GetMode()}
            g.GlobalVar.PutBackCommu(dict3)
            dict2 = {'type': 'state_query', 'room_id': room[3].roomid}
            g.GlobalVar.PutBackCommu(dict2)
        if wind[0] == 1:
            if room[0].expect_wind == 'low':
                room[0].power = room[0].power + 0.2
                room[0].fee = room[0].fee + 1.2
            elif room[0].expect_wind == 'medium':
                room[0].power = room[0].power + 0.3
                room[0].fee = room[0].fee + 1.6
            elif room[0].expect_wind == 'high':
                room[0].power = room[0].power + 0.4
                room[0].fee = room[0].fee + 2.1
            dict3 = {'type': 'bill', 'room_id': room[0].roomid, 'power': room[0].power, 'money': room[0].fee,
                     'mode': g.GlobalVar.GetMode()}
            g.GlobalVar.PutBackCommu(dict3)
        if wind[1] == 1:
            if room[1].expect_wind == 'low':
                room[1].power = room[1].power + 0.2
                room[1].fee = room[1].fee + 1.2
            elif room[1].expect_wind == 'medium':
                room[1].power = room[1].power + 0.3
                room[1].fee = room[1].fee + 1.6
            elif room[1].ecpect_wind == 'high':
                room[1].power = room[1].power + 0.4
                room[1].fee = room[1].fee + 2.1
            dict3 = {'type': 'bill', 'room_id': room[1].roomid, 'power': room[1].power, 'money': room[1].fee,
                     'mode': g.GlobalVar.GetMode()}
            g.GlobalVar.PutBackCommu(dict3)
        if wind[2] == 1:
            if room[2].expect_wind == 'low':
                room[2].power = room[2].power + 0.2
                room[2].fee = room[2].fee + 1.2
            elif room[2].expect_wind == 'medium':
                room[2].power = room[2].power + 0.3
                room[2].fee = room[2].fee + 1.6
            elif room[2].ecpect_wind == 'high':
                room[2].power = room[2].power + 0.4
                room[2].fee = room[2].fee + 2.1
            dict3 = {'type': 'bill', 'room_id': room[2].roomid, 'power': room[2].power, 'money': room[2].fee, 'mode': g.GlobalVar.GetMode()}
            g.GlobalVar.PutBackCommu(dict3)
        if wind[3] == 1:
            if room[3].expect_wind == 'low':
                room[3].power = room[3].power + 0.2
                room[3].fee = room[3].fee + 1.2
            elif room[3].expect_wind == 'medium':
                room[3].power = room[3].power + 0.3
                room[3].fee = room[3].fee + 1.6
            elif room[3].ecpect_wind == 'high':
                room[3].power = room[3].power + 0.4
                room[3].fee = room[3].fee + 2.1
            dict3 = {'type': 'bill', 'room_id': room[3].roomid, 'power': room[3].power, 'money': room[3].fee,'mode': g.GlobalVar.GetMode()}
            g.GlobalVar.PutBackCommu(dict3)
        time.sleep(5)
