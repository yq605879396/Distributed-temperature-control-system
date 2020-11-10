from socket import *
from queue import Queue
import GlobalVar as G
import threading
import json


def Communicating():
    t1 = threading.Thread(target=tcplink, args=(), name='rec')
    t2 = threading.Thread(target=send, args=(), name='send')

    t1.start()
    t2.start()


address = '0.0.0.0'
port = 6666
buff_size = 1024
s = socket(AF_INET, SOCK_STREAM)
s.bind((address, port))
s.listen(5)     #最大连接数
conn_list = []  #已连接的address列表
conn_dt = {}    #已连接的address，socket字典
room_socket = {}#已知的socket和room的映射
socket_room = {}#已知的socket和room的映射


dataBuffer = ''
headerSize = 4
sn = 0

def data_handle(head, body, socket):
    global sn
    sn += 1
    print("receive!!第%s个数据包，长度为%s" % (str(sn), str(int(head))))
    message ={}

    if 'type' in body:
        message['type'] = body['type']
        if message['type'] == 'login':
            message['room_id'] = body['room_id']
            message['id'] = body['id']
            room_socket[body['room_id']] = socket
            socket_room[socket] = body['room_id']
            G.GlobalVar.PutCommuBack(message)
            #print('room_id = %s,and counterpart socket=', body['room_id'], room_socket[body['room_id']])
        elif message['type'] == 'wind_request':
            message['wind_power'] = body['wind_power']
            message['target_temp'] = body['target_temp']
            message['current_temp'] = body['current_temp']
            message['room_id'] = socket_room[socket]
            G.GlobalVar.PutCommuBack(message)
        elif message['type'] == 'stop_wind':
            message['room_id'] = socket_room[socket]
            G.GlobalVar.PutCommuBack(message)
        elif message['type'] == 'state_query_ack':
            message['wind_power'] = body['wind_power']
            message['target_temp'] = body['target_temp']
            message['current_temp'] = body['current_temp']
            message['room_id'] = socket_room[socket]
            G.GlobalVar.PutCommuBack(message)
        elif not  message['type']=='bill_ack':
            print('what is this type > <')
    else:
        print('wrong format of message!> <')
    print('  content:', message, 'socket=', socket, '/n')       

def receive(sock, addr):
    global dataBuffer
    while True:
        #try:
        data = sock.recv(buff_size).decode()
        # 把数据存入缓冲区，类似于push数据
        if data:
            print(data)
            dataBuffer += data
            while True:
                if len(dataBuffer) < headerSize:
                    # print("数据包（%s Byte）小于消息头部长度，跳出小循环" % len(dataBuffer))
                    break

                # 读取包头（正文长度）
                head = dataBuffer[:headerSize]
                bodySize = int(head)
                # 分包情况处理，跳出函数继续接收数据
                if len(dataBuffer) < headerSize + bodySize:
                    # print("数据包（%s Byte）不完整（总共%s Byte），跳出小循环" % (len(dataBuffer), headerSize + bodySize))
                    break
                # 读取消息正文的内容
                body = eval(dataBuffer[headerSize:headerSize + bodySize])  # 字符串转字典
                # 数据处理
                data_handle(head, body, sock)

                # 粘包情况的处理
                dataBuffer = dataBuffer[headerSize + bodySize:]  # 获取下一个数据包，类似于把数据pop出
            else:
                break

        '''      
        except:
            sock.close()
            print(addr, 'offline')
            _index = conn_list.index(addr)
            conn_dt.pop(addr)
            conn_list.pop(_index)
            break   
        '''

def tcplink():
    while True:
        clientsock, clientaddress=s.accept()
        if clientaddress not in conn_list:
            conn_list.append(clientaddress)
            conn_dt[clientaddress] = clientsock
        print('connect from:', clientsock, clientaddress)
        #print('conn_dt.keys are:', conn_dt.keys())
        #在这里创建线程，就可以每次都将socket进行保持
        t = threading.Thread(target=receive, args=(clientsock, clientaddress))
        t.start()


def send():
    while True:
        while G.GlobalVar.Back_Commu_buff.qsize() > 0:
            body = G.GlobalVar.GetBackCommu()
            if not body:
                break
            if 'type' in body and 'room_id' in body:
                message = {}
                message['type'] = body['type']
                if message['type'] == 'login_ack':
                    message['result'] = body['result']
                    message['mode'] = body['mode']
                elif message['type'] == 'wind_request_ack':
                    if body['result'] == 'succeed':
                        message['accept'] = 1
                    elif body['result'] == 'failed':
                        message['accept'] = 0
                    
                elif message['type'] == 'bill':
                    message['power'] = body['power']
                    message['money'] = body['money']
                    message['mode'] = body['mode']
                elif not message['type'] == 'stop_wind_ack' and not message['type'] == 'state_query' and not \
                        message['type'] == 'check':
                    print('what is this type > <')
                message = json.dumps(message)  # 字典->json
                message = message.replace(' ', '')  # 去空格
                message = str(len(message)).zfill(4) + message  # 添加报文长度
                room_socket[body['room_id']].sendall(message.encode('utf-8'))  # 发送信息
                print('send!!', message)




