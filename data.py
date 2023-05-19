import serial
import time
#ser = serial.Serial('COM4', 9600) # replace with appropriate serial port
time.sleep(2)
def data(packet):# = ser.readline().decode().strip()):
    li = list(packet.split(","))
    return li


#packet = """1062,08:17:40,00004,F,ascent,00100.1,N,N,N,00023.6,00003.6,00101.1,
#           00:07:33,00100.1,17.5449,078.5718,00005,045.65,035.65,CXON"""
packet = """1062,00:00:50,166876,S,              IDLE,*****,N,N,N,*****,00.0,********,00:00:00,*******,*******,*******,00,359.62,-16.00,"""
global lis
lis = data(packet)
#ser.close()

def team_id(lis):
    cont = int(lis[0])
    return cont

def mission_time(lis):
    cont=[]
    cont1 = lis[1]
    cont1 = list(cont1.split(":"))
    for i in range(len(cont1)):
        a = cont1[i]
        a = int(a)
        cont+=[a]
    cont[0] = cont[0]*3600
    cont[1] = cont[1]*60
    cont = cont[0] + cont[1] + cont[2]
    return cont

def packet_count(lis):
    cont = int(lis[2])
    return cont

def mode(lis):
    cont = lis[3]
    return cont

def state(lis):
    cont = lis[4]
    return cont.strip()

def altitude(lis):
    cont = float(lis[5])
    return cont

def hs_deployed(lis):
    cont = lis[6]
    return cont

def pc_deployed(lis):
    cont = lis[7]
    return cont

def mast_raised(lis):
    cont = lis[8]
    return cont

def temperature(lis):
    cont = float(lis[9])
    return cont

def voltage(lis):
    cont = float(lis[10])
    return cont

def pressure(lis):
    cont = float(lis[11])
    return cont

def gps_time(lis):
    cont = lis[12]
    return cont

def gps_altitude(lis):
    cont = float(lis[13])
    return cont

def gps_latitude(lis):
    cont = float(lis[14])
    return cont

def gps_longitude(lis):
    cont = float(lis[15])
    return cont

def gps_sats(lis):
    cont = int(lis[16])
    return cont

def tilt_x(lis):
    cont = float(lis[17])
    return cont

def tilt_y(lis):
    cont = float(lis[18])
    return cont

def cmd_echo(lis):
    cont = lis[19]
    return cont


def corrupted_packet():
    a=""
    for i in range(18):
        a+="*"
        if a in lis:
            b = "yes"  
            break       
        else:
            b = "no"
    return b


