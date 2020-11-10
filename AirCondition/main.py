import time, threading
from queue import Queue
from timing import timing

# import other modules
from UI import Operating
from Controller import Backstage, BackstageDelays
from Connection import Communicating

Back_Commu_buff = Queue()  # interacted queue: AirCondition => Main Controller
Oper_Back_buff = Queue()   # interacted queue: Main Controller => AirCondition

temprature = 27

#create threading
threads = []
thread = threading.Thread(target=Operating)
threads.append(thread)
thread = threading.Thread(target=Backstage)
threads.append(thread)
thread = threading.Thread(target=BackstageDelays)
threads.append(thread)
thread = threading.Thread(target=Communicating)
threads.append(thread)
thread = threading.Thread(target=timing)
threads.append(thread)

if __name__ == '__main__':
    # start theading
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

