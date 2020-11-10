
import time,threading
from queue import Queue
from UI import Operating
from Controller import Backstage,BackstageDelays
from Connection import Communicating


#从这里写全局变量
Back_Commu_buff = Queue()  #后台线程和通信线程的信息交互队列
Oper_Back_buff = Queue()   #用户操作线程和后台线程的信息交互队列

temprature = 27

#其他全局变量
threads = []

#创建线程
thread = threading.Thread(target=Operating)
threads.append(thread)

thread = threading.Thread(target=Backstage)
threads.append(thread)
thread = threading.Thread(target=BackstageDelays)
threads.append(thread)
thread = threading.Thread(target=Communicating)
threads.append(thread)


if __name__ == '__main__':
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

