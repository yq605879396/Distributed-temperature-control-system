import time, threading
import sys

import GlobalVar as glob

def timing():
    while True:
        while glob.GlobalVar.Oper_time_buff.qsize()>0:  # 清空并执行用户命令
            if glob.GlobalVar.Oper_time_buff.qsize() == 1:
                dictionary = glob.GlobalVar.GetOper_time_buff()
                if dictionary['temp'] != glob.GlobalVar.GetExpect_Temp() or dictionary['wind'] != glob.GlobalVar.GetExpect_wind():
                    glob.GlobalVar.PutOperBack(dictionary)
                    a = dictionary['wind']
                    b = dictionary['temp']
                    glob.GlobalVar.SetExpect_wind(a)
                    glob.GlobalVar.SetExpect_wind(a)
                    glob.GlobalVar.SetExpect_Temp(b)
            else:
                glob.GlobalVar.GetOper_time_buff()

        time.sleep(2)


