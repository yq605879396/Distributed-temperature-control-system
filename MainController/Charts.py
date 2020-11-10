from pyecharts import Line, Page, Line3D, Page, Style, Style 
import os,datetime
#from app.charts.constants import RANGE_COLOR, WIDTH, HEIGHT


def DayCharts(datas):
    page = Page()
    
    style = Style()

    data_winds = []
    data_temps = []
    data_fees = []

    zero_time = datetime.datetime.now()  + datetime.timedelta(minutes=5)

    for data in datas:
        data['isnew'] = True
        if zero_time.strftime("%Y-%m-%d %H:%M") > data['time'].strftime("%Y-%m-%d %H:%M"):
            zero_time = data['time']
    

    for data in datas:
        if data['state'] == 'True' and data['isnew'] :
            data_wind = []
            data_temp = []
            x = data['room_id']
            y = (data['time']-zero_time).seconds/60
            data_wind.append([x,y,data['expect_wind']])
            data_temp.append([x,y,data['expect_temp']])
            data['isnew'] = False
            for data_1 in datas:
                if(data_1['isnew'] and data_1['room_id']==data['room_id'] and data_1['state'] == 'False'):
                    x = data_1['room_id']
                    y = (data_1['time']-zero_time).seconds/60
                    data_wind.append([x,y,data['expect_wind']])
                    data_temp.append([x,y,data['expect_temp']])
                    data_1['isnew'] = False
                    break
            data_winds.append(data_wind)
            data_temps.append(data_temp)
    
    for data in datas:
        data['isnew'] = True

    for data in datas:
        if data['isnew'] :
            data_fee = []
            x = data['room_id']
            y = (data['time']-zero_time).seconds/60
            data_fee.append([x,y,data['fee']])
            data['isnew'] = False
            for data_1 in datas:
                if(data_1['isnew'] and data_1['room_id']==data['room_id'] ):
                    x = data_1['room_id']
                    y = (data_1['time']-zero_time).seconds/60
                    data_fee.append([x,y,data_1['fee']])
                    data_1['isnew'] = False
            data_fees.append(data_fee)


    chart = Line3D("3D 折线图-送风请求", **style.init_style)
    for data_wind in data_winds:
        chart.add("" , data_wind, is_visualmap=True,visual_range=[0, 30], xaxis3d_name='room_id',yaxis3d_name = 'minutes',zaxis3d_name = 'wind_speed',xaxis3d_max = 5,zaxis3d_max = 3)
    page.add(chart)

    chart = Line3D("3D 折线图-设定温度", **style.init_style)
    for data_temp in data_temps:
        chart.add("", data_temp, is_visualmap=True,visual_range=[0, 30], xaxis3d_name='room_id',yaxis3d_name = 'minutes',zaxis3d_name = 'expect_temperature',xaxis3d_max = 5,zaxis3d_max = 30)
    page.add(chart)

    chart = Line3D("3D 折线图-费用总和", **style.init_style)
    for data_fee in data_fees:
        chart.add("", data_fee, is_visualmap=True,visual_range=[0, 30], xaxis3d_name='room_id',yaxis3d_name = 'minutes',zaxis3d_name = 'costs',xaxis3d_max = 5)
    page.add(chart)

    page.render("./DayChart.html")
    os.system("DayChart.html")

def WeekCharts(datas):
    page = Page()
    
    style = Style()

    data_winds = []
    data_temps = []
    data_fees = []

    zero_time = datetime.datetime.now()  + datetime.timedelta(minutes=5)
    

    for data in datas:
        data['isnew'] = True
        if zero_time.strftime("%Y-%m-%d %H:%M") > data['time'].strftime("%Y-%m-%d %H:%M"):
            zero_time = data['time']
    

    for data in datas:
        if data['state'] == 'True' and data['isnew'] :
            data_wind = []
            data_temp = []
            x = data['room_id']
            y = (data['time']-zero_time).seconds/60
            data_wind.append([x,y,data['expect_wind']])
            data_temp.append([x,y,data['expect_temp']])
            data['isnew'] = False
            for data_1 in datas:
                if(data_1['isnew'] and data_1['room_id']==data['room_id'] and data_1['state'] == 'False'):
                    x = data_1['room_id']
                    y = (data_1['time']-zero_time).seconds/60
                    data_wind.append([x,y,data['expect_wind']])
                    data_temp.append([x,y,data['expect_temp']])
                    data_1['isnew'] = False
                    break
            data_winds.append(data_wind)
            data_temps.append(data_temp)
    
    for data in datas:
        data['isnew'] = True

    for data in datas:
        if data['isnew'] :
            data_fee = []
            x = data['room_id']
            y = (data['time']-zero_time).seconds/60
            data_fee.append([x,y,data['fee']])
            data['isnew'] = False
            for data_1 in datas:
                if(data_1['isnew'] and data_1['room_id']==data['room_id']):
                    x = data_1['room_id']
                    y = (data_1['time']-zero_time).seconds/60
                    data_fee.append([x,y,data_1['fee']])
                    data_1['isnew'] = False
            data_fees.append(data_fee)


    chart = Line3D("3D 折线图-送风请求", **style.init_style)
    for data_wind in data_winds:
        chart.add("" , data_wind, is_visualmap=True,visual_range=[0, 30], xaxis3d_name='room_id',yaxis3d_name = 'minutes',zaxis3d_name = 'wind_speed',xaxis3d_max = 5,zaxis3d_max = 3)
    page.add(chart)

    chart = Line3D("3D 折线图-设定温度", **style.init_style)
    for data_temp in data_temps:
        chart.add("", data_temp, is_visualmap=True,visual_range=[0, 30], xaxis3d_name='room_id',yaxis3d_name = 'minutes',zaxis3d_name = 'expect_temperature',xaxis3d_max = 5,zaxis3d_max = 30)
    page.add(chart)

    chart = Line3D("3D 折线图-费用总和", **style.init_style)
    for data_fee in data_fees:
        chart.add("", data_fee, is_visualmap=True,visual_range=[0, 30], xaxis3d_name='room_id',yaxis3d_name = 'minutes',zaxis3d_name = 'costs',xaxis3d_max = 5)
    page.add(chart)

    page.render("./WeekChart.html")
    os.system("WeekChart.html")

def MonthCharts(datas):
    page = Page()
    style = Style()

    data_winds = []
    data_temps = []
    data_fees = []

    zero_time = datetime.datetime.now()  + datetime.timedelta(minutes=5)
    
    for data in datas:
        data['isnew'] = True
        if zero_time.strftime("%Y-%m-%d %H:%M") > data['time'].strftime("%Y-%m-%d %H:%M"):
            zero_time = data['time']
    
    for data in datas:
        if data['state'] == 'True' and data['isnew'] :
            data_wind = []
            data_temp = []
            x = data['room_id']
            y = (data['time']-zero_time).seconds/60
            data_wind.append([x,y,data['expect_wind']])
            data_temp.append([x,y,data['expect_temp']])
            data['isnew'] = False
            for data_1 in datas:
                if(data_1['isnew'] and data_1['room_id']==data['room_id'] and data_1['state'] == 'False'):
                    x = data_1['room_id']
                    y = (data_1['time']-zero_time).seconds/60
                    data_wind.append([x,y,data['expect_wind']])
                    data_temp.append([x,y,data['expect_temp']])
                    data_1['isnew'] = False
                    break
            data_winds.append(data_wind)
            data_temps.append(data_temp)
    
    for data in datas:
        data['isnew'] = True

    for data in datas:
        if data['isnew'] :
            data_fee = []
            x = data['room_id']
            y = (data['time']-zero_time).seconds/60
            data_fee.append([x,y,data['fee']])
            data['isnew'] = False
            for data_1 in datas:
                if(data_1['isnew'] and data_1['room_id']==data['room_id']):
                    x = data_1['room_id']
                    y = (data_1['time']-zero_time).seconds/60
                    data_fee.append([x,y,data_1['fee']])
                    data_1['isnew'] = False
            data_fees.append(data_fee)


    chart = Line3D("3D 折线图-送风请求", **style.init_style)
    for data_wind in data_winds:
        chart.add("" , data_wind, is_visualmap=True,visual_range=[0, 30], xaxis3d_name='room_id',yaxis3d_name = 'minutes',zaxis3d_name = 'wind_speed',xaxis3d_max = 5,zaxis3d_max = 3)
    page.add(chart)

    chart = Line3D("3D 折线图-设定温度", **style.init_style)
    for data_temp in data_temps:
        chart.add("", data_temp, is_visualmap=True,visual_range=[0, 30], xaxis3d_name='room_id',yaxis3d_name = 'minutes',zaxis3d_name = 'expect_temperature',xaxis3d_max = 5,zaxis3d_max = 30)
    page.add(chart)

    chart = Line3D("3D 折线图-费用总和", **style.init_style)
    for data_fee in data_fees:
        chart.add("", data_fee, is_visualmap=True,visual_range=[0, 30], xaxis3d_name='room_id',yaxis3d_name = 'minutes',zaxis3d_name = 'costs',xaxis3d_max = 5)
    page.add(chart)

    page.render("./MonthChart.html")
    os.system("MonthChart.html")

'''
datas = []
time = datetime.datetime.now()
data = {'state':True,'room_id':1,'expect_temp':23,'current_temp':24,'expect_wind':2,'current_wind':2,'power':1,'fee':20,'time':time}
datas.append(data)
data = {'state':True,'room_id':2,'expect_temp':21,'current_temp':23,'expect_wind':1,'current_wind':1,'power':0.8,'fee':10,'time':time}
datas.append(data)
time = time + datetime.timedelta(minutes=5)
data = {'state':False,'room_id':1,'expect_temp':23,'current_temp':23,'expect_wind':2,'current_wind':2,'power':1,'fee':27,'time':time}
datas.append(data)
time = time + datetime.timedelta(minutes=2)
data = {'state':False,'room_id':2,'expect_temp':21,'current_temp':21,'expect_wind':1,'current_wind':1,'power':0.8,'fee':13,'time':time}
datas.append(data)

time = time + datetime.timedelta(minutes=5)
data = {'state':True,'room_id':1,'expect_temp':21,'current_temp':23,'expect_wind':3,'current_wind':2,'power':1,'fee':27,'time':time}
datas.append(data)
data = {'state':True,'room_id':2,'expect_temp':17,'current_temp':21,'expect_wind':3,'current_wind':1,'power':0.8,'fee':13,'time':time}
datas.append(data)

time = time + datetime.timedelta(minutes=5)
data = {'state':False,'room_id':1,'expect_temp':21,'current_temp':21,'expect_wind':3,'current_wind':2,'power':1,'fee':33,'time':time}
datas.append(data)
data = {'state':False,'room_id':2,'expect_temp':17,'current_temp':19,'expect_wind':3,'current_wind':1,'power':0.8,'fee':20,'time':time}
datas.append(data)

print(datas)
DayCharts(datas)

'''