from socket import *
from queue import Queue
import threading
import json
import time
import random
import GlobalVar as G


address = '192.168.126.1'  # the ip address of the server (controller)
port = 6666
buff_size = 1024
s = socket(AF_INET, SOCK_STREAM)
flag = 0

while(flag == 0):
    try:
        s.connect((address,port))
        flag = 1
    except Exception:
        print('Connection failed, please check if the server is runing.')
        message = {}
        message['type'] = 'connect'
        message['content'] = 'server'
        G.GlobalVar.PutBackCommu(message)
    time.sleep(2)

# for processing received data
dataBuffer = ''
headerSize = 4
sn = 0

def Communicating():
    t1 = threading.Thread(target=receive, args=(), name='recv')
    t2 = threading.Thread(target=send, args=(), name='send')

    t1.start()
    t2.start()
    
    
def data_handle(head, body):
    global sn
    sn += 1
    print("receive!! The %s th data pack, the length is %s" % (str(sn), str(int(head))))
    if 'type' in body:
        message = {}
        message['type'] = body['type']
        if message['type'] == 'login_ack':
            message['mode'] = body['mode']
            message['result'] = body['result']
            G.GlobalVar.PutCommuBack(message)   
        elif message['type'] == 'wind_request_ack':
            if body['accept'] == 0:
                message['result'] = 'failed'
            elif body['accept'] == 1:
                message['result'] = 'succeed'
            else:
                print('wrong format of accept in login_ack.\___@.@')
            G.GlobalVar.PutCommuBack(message)
        elif message['type'] == 'stop_wind_ack':
            G.GlobalVar.PutCommuBack(message)
        elif message['type'] == 'state_query':
            G.GlobalVar.PutCommuBack(message)
        elif message['type'] == 'bill':
            message['power'] = body['power']
            message['money'] = body['money']
            message['mode'] = body['mode']
            G.GlobalVar.PutCommuBack(message)
            ack_message ={}
            ack_message['type']='bill_ack'
            G.GlobalVar.PutBackCommu(ack_message)
        elif message['type'] == 'check':#断网啦
            G.GlobalVar.PutCommuBack(message)
            s.close()
        else:
            print('what is this type > <')
        print('  content:', message, '\n')
    else:
        print('wrong format of message!> <')

def receive():
    global dataBuffer
    while True:
        data = s.recv(buff_size).decode()
        if data:
            # 把数据存入缓冲区，类似于push数据
            dataBuffer += data
            while True:
                if len(dataBuffer) < headerSize:
                    #print("数据包（%s Byte）小于消息头部长度，跳出小循环" % len(dataBuffer))
                    break

                # 读取包头（正文长度）
                head = dataBuffer[:headerSize]
                bodySize = int(head)

                # 分包情况处理，跳出函数继续接收数据
                if len(dataBuffer) < headerSize + bodySize:
                    #print("数据包（%s Byte）不完整（总共%s Byte），跳出小循环" % (len(dataBuffer), headerSize + bodySize))
                    break

                # 读取消息正文的内容
                body = eval(dataBuffer[headerSize:headerSize + bodySize])  #转变成dic格式

                # 数据处理
                data_handle(head, body)

                # 粘包情况的处理
                dataBuffer = dataBuffer[headerSize + bodySize:]  # 获取下一个数据包，类似于把数据pop出

def send():
    while True:
        while  G.GlobalVar.Back_Commu_buff.qsize() > 0:
            body = G.GlobalVar.GetBackCommu()
            if not body:
                break
            message = {}
            if 'type' in body:
                message['type'] = body['type']
                if message['type'] == 'login':
                    message['room_id'] = body['room_id']
                    message['id'] = body['id']
                elif message['type'] == 'wind_request':
                    message['wind_power'] = body['wind_power']
                    message['target_temp'] = body['target_temp']
                    message['current_temp'] = body['current_temp']
                elif message['type'] == 'state_query_ack':
                    message['wind_power'] = body['wind_power']
                    message['target_temp'] = body['target_temp']
                    message['current_temp'] = body['current_temp']
                elif not message['type'] == 'bill_ack' and not message['type'] == 'stop_wind':
                    print('what is this type > <')
                message = json.dumps(message)  # 字典->json
                message = message.replace(' ', '')  # 去空格
                message = str(len(message)).zfill(4) + message  # 添加报文长度
                s.sendall(message.encode('utf-8'))  # 发送信息
                print('send!!', message)
            else:
                print('wrong format of message!> <')
                message = json.dumps(message)  # 字典->json
                message = message.replace(' ', '')  # 去空格
                message = str(len(message)).zfill(4) + message  # 添加报文长度
                s.sendall(message.encode('utf-8'))  # 发送信息
                print('send!!', message)


