import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt, QObject, QThread, pyqtSignal, pyqtSlot
from digi.xbee.devices import XBeeDevice
from PyQt5 import *
from PyQt5 import QtWidgets
from PyQt5 import QtCore
import sys
from plot import graph
from map_plot import mapWidget
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from widget import namewidget
from datetime import datetime,timezone
from digi.xbee.devices import XBeeDevice
from digi.xbee.devices import *
import random
try:
        PORT = "COM5"  # Replace with your actual port
        BAUD_RATE = 9600  # Replace with your actual baud rate
        REMOTE_NODE_ID = "REMOTE_NODE_ID"  # Replace with the remote node ID
        DATA_TO_SEND = "hi"
except:
        pass
check_sim = 0
curstate = "Idle"
is_ascent, is_descent, is_heat_shield_deployed, is_landed, is_mast_raised, is_parachute_deployed,is_probe_deployed, is_rocket_separated = 0,0,0,0,0,0,0,0
corruptedPacketsValue =0 
global packet
simp = ""
try:
        device = XBeeDevice(PORT, BAUD_RATE)
        device.open()
except:
        pass
previous_state = None

# Worker thread for sending data
class SendDataThread(QThread):
        def __init__(self):
                super().__init__()
                global DATA_TO_SEND


        def run(self):
                global DATA_TO_SEND, device
                try:
                        data = DATA_TO_SEND
                        #print(data,1)
                        
                        remote  = RemoteXBeeDevice(device,XBee64BitAddress.from_hex_string("0013A20040AD19CA"))
                        device.send_data(remote,data)
                        #print(data,2)
                except:
                        pass
                        

                finally:
                        if device is not None and device.is_open():
                                DATA_TO_SEND = ""
                                #print("yo")


class ReceiveDataThread(QThread):
        data_received = pyqtSignal(str)

        def __init__(self):
                super().__init__()

        def run(self):
                global packet, device
                packet = ""
                try:

                        def data_receive_callback(xbee_message):
                                global packet

                                packet = xbee_message.data.decode()
                                self.data_received.emit(packet)
                                

                        device.add_data_received_callback(data_receive_callback)

                        input()
        
                except Exception as e:
                        MainWindow().onGettingData(f"Error receiving data: {e}")

                finally:
                        if device is not None and device.is_open():
                                pass


class MainWindow(QMainWindow):
    def upload_file(self,event):
        if event.button() == Qt.LeftButton:
                file_dialog = QFileDialog()
                file_dialog.exec_()

                # Retrieve the selected file(s)
                file_paths = file_dialog.selectedFiles()
                for file_path in file_paths:
                        #print(f"Selected file: {file_path}")
                        self.send_simulation(file_path)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Rocket Probe GUI")
        self.screen = app.primaryScreen() 
        self.size = self.screen.size()
        self.window_width, self.window_height=self.size.width(),self.size.height()-100
        #self.window_width, self.window_height = 900,700
        global height, width
        size = 50
        
        self.w , self.h =self.window_width, self.window_height
        width, height = self.w, self.h
        self.setMinimumSize(self.window_width, self.window_height)
        self.setStyleSheet('''
                QWidget {
                font-size:15px;
                }
        ''')

        def buttonfunc(name,fontsize):
            button_layout=QHBoxLayout()
            if name=="Telemetry":
                    self.button_name1= QtWidgets.QPushButton()
                    #self.button_name1.setCheckable(True)
                    self.button_name1.setText(name)
                    self.button_name1.setCheckable(True)
                    self.button_name1.setStyleSheet("QPushButton{color: #f5fcff; font: %spt  'Oswald';background-color: rgb(30,30,30); }" % fontsize)
                    button_layout.addWidget(self.button_name1)
                    self.y = True
                    self.button_name1.clicked.connect(self.telemetry_button)
            if name=="Calibration":
                    self.button_name2= QtWidgets.QPushButton()
                    self.button_name2.setText(name)
                    self.button_name2.setCheckable(True)
                    self.button_name2.setStyleSheet("QPushButton{color: #f5fcff; font: %spt  'Oswald';background-color: rgb(30,30,30); }" % fontsize)
                    button_layout.addWidget(self.button_name2)
                    self.button_name2.clicked.connect(self.calibration_button)
            if name=="Set Time UTC":
                    self.button_name3= QtWidgets.QPushButton()
                    self.button_name3.setText(name)
                    self.button_name3.setCheckable(True)
                    self.button_name3.setStyleSheet("QPushButton{color: #f5fcff; font: %spt  'Oswald';background-color: rgb(30,30,30); }" % fontsize)
                    button_layout.addWidget(self.button_name3)
                    self.button_name3.clicked.connect(self.set_time_utc_button)
            if name=="Set Time GPS":
                    self.button_name4= QtWidgets.QPushButton()
                    self.button_name4.setText(name)
                    self.button_name4.setCheckable(True)
                    self.button_name4.setStyleSheet("QPushButton{color: #f5fcff; font: %spt  'Oswald';background-color: rgb(30,30,30); }" % fontsize)
                    button_layout.addWidget(self.button_name4)
                    self.button_name4.clicked.connect(self.set_time_gps_button)
            if name=="Simulation-Enable":
                    self.button_name5= QtWidgets.QPushButton()
                    self.button_name5.setText(name)
                    self.button_name5.setCheckable(True)
                    self.button_name5.setStyleSheet("QPushButton{color: #f5fcff; font: %spt  'Oswald';background-color: rgb(30,30,30); }" % fontsize)
                    button_layout.addWidget(self.button_name5)
                    self.button_name5.clicked.connect(self.simulation_enabled_button)
            if name=="Simulation-Activate":
                    self.button_name6= QtWidgets.QPushButton()
                    self.button_name6.setCheckable(True)
                    self.button_name6.setText(name)
                    self.button_name6.setStyleSheet("QPushButton{color: rgb(200,200,200); font: %spt  'Oswald';background-color: rgb(10,10,10); }" % fontsize)
                    button_layout.addWidget(self.button_name6)
                    self.button_name6.clicked.connect(self.simulation_activate_button)
            if name=="Audio-Beacon":
                    self.button_name7= QtWidgets.QPushButton()
                    self.button_name7.setCheckable(True)
                    self.button_name7.setText(name)
                    self.button_name7.setStyleSheet("QPushButton{color: #f5fcff; font: %spt  'Oswald';background-color: rgb(30,30,30); }" % fontsize)
                    button_layout.addWidget(self.button_name7)
                    self.button_name7.clicked.connect(self.audio_beacon_button)
            if name=="Deploy-Nose":
                    self.button_name8= QtWidgets.QPushButton()
                    self.button_name8.setCheckable(True)
                    self.button_name8.setText(name)
                    self.button_name8.setStyleSheet("QPushButton{color: #f5fcff; font: %spt  'Oswald';background-color: rgb(30,30,30); }" % fontsize)
                    button_layout.addWidget(self.button_name8)
                    self.button_name8.clicked.connect(self.deploy_nose_button)
            if name=="Deploy-Para":
                    self.button_name9= QtWidgets.QPushButton()
                    self.button_name9.setCheckable(True)
                    self.button_name9.setText(name)
                    self.button_name9.setStyleSheet("QPushButton{color: #f5fcff; font: %spt  'Oswald';background-color: rgb(30,30,30); }" % fontsize)
                    button_layout.addWidget(self.button_name9)
                    self.button_name9.clicked.connect(self.deploy_para_button)
            if name=="Reset":
                    self.button_name10= QtWidgets.QPushButton()
                    self.button_name10.setCheckable(True)
                    self.button_name10.setText(name)
                    self.button_name10.setStyleSheet("QPushButton{color: #f5fcff; font: %spt  'Oswald';background-color: rgb(30,30,30); }" % fontsize)
                    button_layout.addWidget(self.button_name10)
                    self.button_name10.clicked.connect(self.reset_button)


            button_widget = QtWidgets.QWidget()
            button_widget.setLayout(button_layout)
            button_widget.setFixedHeight(60)
            return button_widget
                
        def dotAndState(state,height,fontsize):
            state_label=QLabel(state)
            layout=QGridLayout()
            if state == "Launch Wait":
                    self.dot1= QLabel("🔴")
                    self.dot1.setText("🔴")
                    self.dot1.setStyleSheet("QLabel{color: rgb(255,0,13); ; font: %spt  'Oswald'; background-color: rgb(30,30,30);}" % fontsize)
                    layout.addWidget(self.dot1,1,1,1,1)
            if state == "Descent":
                    self.dot2= QLabel("🔴")
                    self.dot2.setText("🔴")
                    self.dot2.setStyleSheet("QLabel{color: rgb(255,0,13); ; font: %spt  'Oswald'; background-color: rgb(30,30,30);}" % fontsize)
                    layout.addWidget(self.dot2,1,1,1,1)
            if state == "Ascent":
                    self.dot3= QLabel("🔴")
                    self.dot3.setText("🔴")
                    self.dot3.setStyleSheet("QLabel{color: rgb(255,0,13); ; font: %spt  'Oswald'; background-color: rgb(30,30,30);}" % fontsize)
                    layout.addWidget(self.dot3,1,1,1,1)
            if state == "HS Released":
                    self.dot4= QLabel("🔴")
                    self.dot4.setText("🔴")
                    self.dot4.setStyleSheet("QLabel{color: rgb(255,0,13); ; font: %spt  'Oswald'; background-color: rgb(30,30,30);}" % fontsize)
                    layout.addWidget(self.dot4,1,1,1,1)
            if state == "Rocket Separation":
                    self.dot5= QLabel("🔴")
                    self.dot5.setText("🔴")
                    self.dot5.setStyleSheet("QLabel{color: rgb(255,0,13); ; font: %spt  'Oswald'; background-color: rgb(30,30,30);}" % fontsize)
                    layout.addWidget(self.dot5,1,1,1,1)
            if state == "Landed":
                    self.dot6= QLabel("🔴")
                    self.dot6.setText("🔴")
                    self.dot6.setStyleSheet("QLabel{color: rgb(255,0,13); ; font: %spt  'Oswald'; background-color: rgb(30,30,30);}" % fontsize)
                    layout.addWidget(self.dot6,1,1,1,1)
            
            
            state_label.setStyleSheet("QLabel{color: #f5fcff; font: %spt  'Oswald';background-color: rgb(30,30,30); }" % fontsize)

            layout.addWidget(state_label,1,2,1,5)
            layout_widget = QtWidgets.QWidget()
            layout_widget.setLayout(layout)
            layout_widget.setFixedHeight(height)
            return layout_widget
        
        
        
##------logowidget start---------------------------------------------------------------
        self.logo = QLabel()
        logo_image = QPixmap('./Janus Logo.png')
        #logo_image = logo_image.scaled(int(0.12*self.w),int(0.33*self.h), QtCore.Qt.KeepAspectRatio)
        self.logo.setPixmap(logo_image)
        self.logo.setScaledContents(True)
        logo_layout = QHBoxLayout()
        logo_layout.setSpacing(0)
        logo_layout.addWidget(self.logo)
        self.logo_widget = QtWidgets.QWidget()
        self.logo_widget.setFixedWidth(int((230/1980)*self.w))
        self.logo_widget.setFixedHeight(int((70/880)*self.h))
        self.logo_widget.setLayout(logo_layout)
        self.logo_widget.setCursor(Qt.PointingHandCursor)
        self.logo_widget.mousePressEvent = self.upload_file
#-------logowidget ends----------------------------------------------------------------
        self.connector = namewidget()

        """self.painter = QPainter(self)
        self.painter.setRenderHint(QPainter.Antialiasing)
        self.painter.setBrush(QBrush(QColor('red')))
        self.painter.setPen(Qt.NoPen)
        self.size1 = min(int((230/1980)*self.w), int((70/880)*self.h))
        self.painter.drawEllipse(int(((230/1980)*self.w - self.size1) // 2), int(((70/880)*self.h - self.size1)) // 2, size, size)
        painter_layout = QVBoxLayout()
        painter_layout.addwidget(self.painter)
        self.painter_widget = QtWidgets.QWidget()
        self.painter_widget.setFixedWidth(int((60/1980)*self.w))
        self.painter_widget.setFixedHeight(int((60/880)*self.h))
        self.painter_widget.setLayout(painter_layout)"""
#-------bits logo starts-------------------------------------------------------------------
        self.logo2 = QLabel()
        logo2_image = QPixmap('./bits.png')
        #logo_image = logo_image.scaled(int(0.12*self.w),int(0.33*self.h), QtCore.Qt.KeepAspectRatio)
        self.logo2.setPixmap(logo2_image)
        self.logo2.setScaledContents(True)
        logo2_layout = QHBoxLayout()
        logo2_layout.setSpacing(0)
        logo2_layout.addWidget(self.logo2)
        self.logo2_widget = QtWidgets.QWidget()
        self.logo2_widget.setFixedWidth(int((60/1980)*self.w))
        self.logo2_widget.setFixedHeight(int((60/880)*self.h))
        self.logo2_widget.setLayout(logo2_layout)
#-------team id widget starts---------------------------------------------------------------------
        self.team_label = QLabel('TEAM ID:2027')
        self.team_label.setAlignment(QtCore.Qt.AlignCenter)
        team_layout = QVBoxLayout()
        team_layout.addWidget(self.team_label)
        self.team_widget = QtWidgets.QWidget()
        self.team_widget.setFixedWidth(int((220/1980)*self.w))
        self.team_widget.setFixedHeight(int((50/880)*self.h))
        self.team_widget.move(0,0)
        self.team_widget.setLayout(team_layout)
        self.team_widget.setStyleSheet("QLabel{color: #f5fcff; font: %spt  'Oswald'; background-color: rgb(15,15,15); }" %(int(((20/1980)/50)*size*self.w)))
#-------team id widget ends-----------------------------------------------------------------------
#-------logo plus team id combined widget starts----------------------------------------------------
        MENU1_layout = QGridLayout()
        MENU1_layout.setSpacing(0)
        #MENU1_layout.addWidget(self.logo2_widget,1,0,1,1,QtCore.Qt.AlignVCenter)
        MENU1_layout.addWidget(self.logo_widget,0,0,1,1,QtCore.Qt.AlignCenter)
        MENU1_layout.addWidget(self.team_widget,1,0,1,1,QtCore.Qt.AlignTop)
        self.MENU1_widget = QtWidgets.QWidget()
        self.MENU1_widget.setLayout(MENU1_layout)
        self.MENU1_widget.setFixedWidth(int((260/1980)*self.w))
        self.MENU1_widget.setFixedHeight(int((230/880)*self.h))
        #self.MENU1_widget.seftStyleSheet("QLabel{color: #f5fcff; font: %spt  'Oswald'; background-color: rgb(15,15,15); }" %(int((25/1980)*self.w)))
#-------logo plus team id combined widget ends---------------------------------------------------------------------------
#-------mission time widget starts---------------------------------------------------------------------------------------       
        self.MENU2_mission_time = QLabel('Mission Time: 00:00:00.00')
        self.MENU2_mission_time.setAlignment(QtCore.Qt.AlignCenter)
        
        self.time = 0
        self.timer2 = QTimer()
        self.timer2.setInterval(1000)
        self.timer2.start()
        self.timer2.timeout.connect(self.mission_time)
        MENU2_layout = QVBoxLayout()
        MENU2_layout.addWidget(self.MENU2_mission_time)
        
        self.MENU2_widget = QtWidgets.QWidget()
        self.MENU2_widget.setLayout(MENU2_layout)
        self.MENU2_widget.setFixedWidth(int((300/1980)*self.w))
        self.MENU2_widget.setFixedHeight(int((60/880)*self.h))
        self.MENU2_widget.setStyleSheet("QLabel{color: #f5fcff; font: %spt  'Oswald';background-color: rgb(30,30,30); } " %(int(((19/1980)/50)*size*self.w)))
#-------mission time widget ends----------------------------------------------------------------------------------------------
#-------state widget starts------------------------------------------------------------------------------------------------------
        self.state = QLabel("Current State: Ascent")
        self.state.setAlignment(QtCore.Qt.AlignCenter)
        state_layout = QVBoxLayout()
        state_layout.addWidget(self.state)
        self.state_widget = QtWidgets.QWidget()
        self.state_widget.setFixedWidth(int((400/1980)*self.w))
        self.state_widget.setFixedHeight(int((60/880)*self.h))
        self.state_widget.setStyleSheet("QLabel{color: #f5fcff; font: %spt  'Oswald';background-color: rgb(30,30,30); }" %(int(((19/1980)/50)*size*self.w)))
        self.state_widget.setLayout(state_layout)
#-------state widget ends---------------------------------------------------------------------------------------------------------
#-------mode widgets starts-------------------------------------------------------------------------------------------------------
        self.mode_name = QLabel("Mode: Flight")
        mode_layout = QVBoxLayout()
        mode_layout.addWidget(self.mode_name)
        self.mode_widget = QtWidgets.QWidget()
        self.mode_widget.setFixedWidth(int((280/1980)*self.w))
        self.mode_widget.setFixedHeight(int((60/880)*self.h))
        self.mode_name.setAlignment(QtCore.Qt.AlignCenter)
        self.mode_widget.setStyleSheet("QLabel{color: #f5fcff; font: %spt  'Oswald';background-color: rgb(30,30,30); }" %(int(((19/1980)/50)*size*self.w)))
        self.mode_widget.setLayout(mode_layout)
#-------mode widget ends------------------------------------------------------------------------------------------------------------
#-------states 1 widget starts, code in widget.py file-------------------------------------------------------------------------------
        states1_layout=QVBoxLayout()
        states1_layout.setSpacing(0)
        self.asc=dotAndState("Launch Wait",int((50/880)*self.h),int(((14/1980)/50)*size*self.w))
        states1_layout.addWidget(self.asc)
        states1_layout.addWidget(dotAndState("Descent", int((50/880)*self.h),int(((14/1980)/50)*size*self.w)))
        self.states1_widget = QtWidgets.QWidget()
        self.states1_widget.setFixedWidth(int((200/1980)*self.w))
        self.states1_widget.setFixedHeight(int((100/880)*self.h))
        self.states1_widget.setLayout(states1_layout)
        self.states1_widget.setStyleSheet("QWidget{background-color: rgb(30,30,30); }")
#-------state 1 widget ends-------------------------------------------------------------------------------------------------------------
#-------state 2 widget starts------------------------------------------------------------------------------------------------------------------
        states2_layout=QVBoxLayout()
        states2_layout.setSpacing(0)
        states2_layout.addWidget(dotAndState("Ascent", int((50/880)*self.h),int(((14/1980)/50)*size*self.w)))
        states2_layout.addWidget(dotAndState("HS Released", int((50/880)*self.h),int(((14/1980)/50)*size*self.w)))

        self.states2_widget = QtWidgets.QWidget()
        self.states2_widget.setFixedWidth(int((350/1980)*self.w))
        self.states2_widget.setFixedHeight(int((100/880)*self.h))
        self.states2_widget.setLayout(states2_layout)
        self.states2_widget.setStyleSheet("QWidget{background-color: rgb(30,30,30); }")
#-------state 2 widget ends-----------------------------------------------------------------------------------------------------------------------
#-------state 3 widget starts--------------------------------------------------------------------------------------------------------------
        states3_layout=QVBoxLayout()
        states3_layout.setSpacing(0)
        states3_layout.addWidget(dotAndState("Rocket Separation", int((50/880)*self.h),int(((14/1980)/50)*size*self.w)))
        states3_layout.addWidget(dotAndState("Landed", int((50/880)*self.h),int(((14/1980)/50)*size*self.w)))

        self.states3_widget = QtWidgets.QWidget()
        self.states3_widget.setFixedWidth(int((270/1980)*self.w))
        self.states3_widget.setFixedHeight(int((100/880)*self.h))
        self.states3_widget.setLayout(states3_layout)
        self.states3_widget.setStyleSheet("QWidget{background-color: rgb(30,30,30); }")
#-------state 3 widget ends----------------------------------------------------------------------------------------------------------------------------

#-------statesfull starts --------------------------------------------------------------------------------------------------------------------
        statesfull_layout=QHBoxLayout()
        statesfull_layout.setSpacing(0)
        statesfull_layout.addWidget(self.states1_widget)
        statesfull_layout.addWidget(self.states2_widget)
        statesfull_layout.addWidget(self.states3_widget)
        
        self.statesfull_widget = QtWidgets.QWidget()
        self.statesfull_widget.setLayout(statesfull_layout)
        self.statesfull_widget.setFixedWidth(int((950/1980)*self.w))
        self.statesfull_widget.setFixedHeight(int((120/880)*self.h))
        self.statesfull_widget.setStyleSheet("QWidget{background-color: rgb(30,30,30); }")
#-------statesfull ends ---------------------------------------------------------------------------------------------------------------
#-------state 4 widget ends----------------------------------------------------------------------------------------------------------------------------
#-------menu 3 starts with widget of mission time, mode and state---------------------------------------------------------------------------------------
        MENU3_layout = QGridLayout()
        MENU3_layout.addWidget(self.mode_widget,1,1,1,1,QtCore.Qt.AlignTop)
        MENU3_layout.addWidget(self.MENU2_widget,1,2,1,1,QtCore.Qt.AlignTop)
        MENU3_layout.addWidget(self.state_widget,1,3,1,1,QtCore.Qt.AlignTop)
        self.MENU3_widget = QtWidgets.QWidget()
        self.MENU3_widget.setLayout(MENU3_layout)  
        self.MENU3_widget.setFixedWidth(int((1050/1980)*self.w))
        self.MENU3_widget.setFixedHeight(int((80/880)*self.h))      
        self.MENU3_widget.setStyleSheet("QWidget{background-color: rgb(20,20,20); }")
#-------menu 3 ends------------------------------------------------------------------------------------------------------------------------
#-------menu 4 starts with widgets of menu3, states1 and states2----------------------------------------------------------------------------
        MENU4_layout = QGridLayout()
        MENU4_layout.setSpacing(0)
        MENU4_layout.addWidget(self.MENU3_widget,0,0,1,1,QtCore.Qt.AlignCenter)
        MENU4_layout.addWidget(self.statesfull_widget,1,0,1,1,QtCore.Qt.AlignCenter)
        #MENU4_layout.addWidget(self.states2_widget)
        self.MENU4_widget = QtWidgets.QWidget()
        self.MENU4_widget.setFixedWidth(int((1000/1980)*self.w))
        self.MENU4_widget.setFixedHeight(int((200/880)*self.h))
        self.MENU4_widget.setLayout(MENU4_layout)
#-------menu 4 ends---------------------------------------------------------------------------------------------------------------------------------
#-------menu 5 starts with widget of team id and logo along with menu 4------------------------------------------------------------------------------
        MENU5_layout = QGridLayout()
        MENU5_layout.setSpacing(0)
        MENU5_layout.addWidget(self.MENU1_widget,0,0,1,1,QtCore.Qt.AlignCenter)
        MENU5_layout.addWidget(self.MENU4_widget,0,1,1,6,QtCore.Qt.AlignCenter)
        MENU5_layout.addWidget(self.connector.nameline("",int(((60/1980)/50)*size*self.w),int(((60/880)/50)*size*self.h),int(((13/1980)/50)*size*self.w)),0,7,1,1,QtCore.Qt.AlignCenter)
        self.MENU5_widget = QtWidgets.QWidget()
        self.MENU5_widget.setFixedWidth(int((1350/1980)*self.w))
        self.MENU5_widget.setFixedHeight(int((220/880)*self.h))
        self.MENU5_widget.setLayout(MENU5_layout)
#-------menu 5 ends----------------------------------------------------------------------------------------------------------------------------
#-------button widget starts, code for which is in widget.py file------------------------------------------------------------------------------
        button_layout=QGridLayout()
        self.tel = buttonfunc("Telemetry",int((12/1980)*self.w))
        #print(self.tel.clicked.connect())
        button_layout.addWidget(self.tel,1,1,1,1)   
        button_layout.addWidget(buttonfunc("Calibration",int((12/1980)*self.w)),1,2,1,1)
        button_layout.addWidget(buttonfunc("Set Time UTC",int((12/1980)*self.w)),1,3,1,1)
        button_layout.addWidget(buttonfunc("Set Time GPS",int((12/1980)*self.w)),1,4,1,1)
        button_layout.addWidget(buttonfunc("Simulation-Enable",int((12/1980)*self.w)),1,5,1,1)
        button_layout.addWidget(buttonfunc("Simulation-Activate",int((12/1980)*self.w)),2,1,1,1)
        button_layout.addWidget(buttonfunc("Audio-Beacon",int((12/1980)*self.w)),2,2,1,1)
        button_layout.addWidget(buttonfunc("Deploy-Nose",int((12/1980)*self.w)),2,3,1,1)
        button_layout.addWidget(buttonfunc("Deploy-Para",int((12/1980)*self.w)),2,4,1,1)
        button_layout.addWidget(buttonfunc("Reset",int((12/1980)*self.w)),2,5,1,1)
        self.button_widget = QtWidgets.QWidget()
        self.button_widget.setLayout(button_layout)
        self.button_widget.setFixedWidth(int((1350/1980)*self.w))
        self.button_widget.setFixedHeight(int((100/880)*self.h))
        self.button_widget.setStyleSheet("QWidget{background-color: rgb(20,20,20); }")
#-------button widget ends---------------------------------------------------------------------------------------------------------------
#-------graph1 starts, code can be found in plot.py and widget.py--------------------------------------------------------------------
#-------graph pressure starts---------------------------------------------------------------------------------------------
        self.pressure_widget = namewidget()

        self.graphPressure1 = graph([
                {
                        "color": (245,252,255),
                        "name": "Pressure"
                }], True, 200, "", "Pressure ")
        graphPressure_Layout = QVBoxLayout()
        graphPressure_Layout.addWidget(self.pressure_widget.nameline("Pressure",int(((7/1980)/50)*size*self.w),int(((25/880)/50)*size*self.h),int(((13/1980)/50)*size*self.w)))
        graphPressure_Layout.addWidget(self.graphPressure1.graphWidget)
        self.graphPressure = QtWidgets.QWidget()
        self.graphPressure.setLayout(graphPressure_Layout)
        self.graphPressure.setFixedWidth(int((430/1980)*self.w))
        self.graphPressure.setFixedHeight(int((230/880)*self.h))
        self.graphPressure.setStyleSheet("QLabel{color: #f5fcff; font: 10pt  'Oswald';background-color: rgb(3,0,13); }")
#-------graph pressure ends---------------------------------------------------------------------------------------------------
#-------graph temperature starts----------------------------------------------------------------------------------------------
        self.temperature_widget = namewidget()
        self.graphTemperature1 = graph([
                {
                        "color": (245,252,255),
                        "name": "Temperature"
                }], True, 200, "", "Temperature ")
        graphTemperature_Layout = QVBoxLayout()
        graphTemperature_Layout.addWidget(self.temperature_widget.nameline("Temperature",int(((7/1980)/50)*size*self.w),int(((25/880)/50)*size*self.h),int(((13/1980)/50)*size*self.w)))
        graphTemperature_Layout.addWidget(self.graphTemperature1.graphWidget)
        self.graphTemperature = QtWidgets.QWidget()
        self.graphTemperature.setLayout(graphTemperature_Layout)
        self.graphTemperature.setFixedWidth(int((430/1980)*self.w))
        self.graphTemperature.setFixedHeight(int((230/880)*self.h))
        self.graphTemperature.setStyleSheet("QLabel{color: #f5fcff; font: 10pt  'Oswald';background-color: rgb(3,0,13); }")
#-------graph temperature ends-------------------------------------------------------------------------------------------------
#-------graph altitude starts---------------------------------------------------------------------------------------------------
        self.altitude_widget = namewidget()
        self.graphAltitude1 = graph([
                {
                        "color": (245,252,255),
                        "name": "Altitude"
                }], True, 200, "", "Altitude ")
        graphAltitude_Layout = QVBoxLayout()
        graphAltitude_Layout.addWidget(self.altitude_widget.nameline("Altitude",int(((7/1980)/50)*size*self.w),int(((25/880)/50)*size*self.h),int(((13/1980)/50)*size*self.w)))
        graphAltitude_Layout.addWidget(self.graphAltitude1.graphWidget)
        self.graphAltitude = QtWidgets.QWidget()
        self.graphAltitude.setLayout(graphAltitude_Layout)
        self.graphAltitude.setFixedWidth(int((430/1980)*self.w))
        self.graphAltitude.setFixedHeight(int((230/880)*self.h))
        self.graphAltitude.setStyleSheet("QLabel{color: #f5fcff; font: 12pt  'Oswald';background-color: rgb(3,0,13); }")
#-------graph altitude ends--------------------------------------------------------------------------------------------------------
#-------graph 1 widget making starts-------------------------------------------------------------------------------------------
        GRAPH1_layout = QGridLayout()
        GRAPH1_layout.addWidget(self.graphPressure,1,1,1,1,QtCore.Qt.AlignCenter)
        GRAPH1_layout.addWidget(self.graphTemperature,1,2,1,1,QtCore.Qt.AlignCenter)
        GRAPH1_layout.addWidget(self.graphAltitude,1,3,1,1,QtCore.Qt.AlignCenter)
        self.GRAPH1_widget = QtWidgets.QWidget()
        self.GRAPH1_widget.setLayout(GRAPH1_layout)
        #self.graphAltitude.setFixedWidth(int((1420/1980)*self.w))
        #self.graphAltitude.setFixedHeight(int((270/880)*self.h))
        self.GRAPH1_widget.setStyleSheet("background-color: rgb(30,30,30)")
#-------graph 1 widget making ends---------------------------------------------------------------------------------------------------
#-------graph2 widget starts, code can found on widget.py and plot.py-----------------------------------------------------------------------------------------
#-------graph voltage starts---------------------------------------------------------------------------------------------------------
        self.voltage_widget = namewidget()
        self.graphVoltage1 = graph([
                {
                        "color": (245,252,255),
                        "name": "Voltage"
                }], True, 200, "", "Voltage ")
        graphVoltage_Layout = QVBoxLayout()
        graphVoltage_Layout.addWidget(self.voltage_widget.nameline("Voltage",int((7/1980)*self.w),int((25/880)*self.h),int((13/1980)*self.w)))
        graphVoltage_Layout.addWidget(self.graphVoltage1.graphWidget)
        self.graphVoltage = QtWidgets.QWidget()
        self.graphVoltage.setFixedWidth(int((430/1980)*self.w))
        self.graphVoltage.setFixedHeight(int((230/880)*self.h))
        self.graphVoltage.setLayout(graphVoltage_Layout)
        self.graphVoltage.setStyleSheet("QLabel{color: #f5fcff; font: 10pt  'Oswald';background-color: rgb(3,0,13); }")
#-------graph voltage ends------------------------------------------------------------------------------------------------------------
#-------graph gps altitude starts-----------------------------------------------------------------------------------------------------
        self.gps_altitude_widget1 = namewidget()
        self.graphGPS_Altitude1 = graph([
                {
                        "color": (245,252,255),
                        "name": "GPS_Altitude"
                }], True, 200, "", "GPS_Altitude")
        graphGPS_Altitude_Layout = QVBoxLayout()
        graphGPS_Altitude_Layout.addWidget(self.gps_altitude_widget1.nameline("GPS Altitude",int(((7/1980)/50)*size*self.w),int(((25/880)/50)*size*self.h),int(((13/1980)/50)*size*self.w)))
        graphGPS_Altitude_Layout.addWidget(self.graphGPS_Altitude1.graphWidget)
        self.graphGPS_Altitude = QtWidgets.QWidget()
        self.graphGPS_Altitude.setFixedWidth(int((430/1980)*self.w))
        self.graphGPS_Altitude.setFixedHeight(int((230/880)*self.h))
        self.graphGPS_Altitude.setLayout(graphGPS_Altitude_Layout)
        self.graphGPS_Altitude.setStyleSheet("QLabel{color: #f5fcff; font: 10pt  'Oswald';background-color: rgb(3,0,13); }")
#-------graph gps altitude ends--------------------------------------------------------------------------------------------------------
#-------graph titl xy starts-----------------------------------------------------------------------------------------------------------
        self.tiltxy_widget = namewidget()
        self.graphTilt_XY1 = graph([
                {
                        "color": (245,252,255),
                        "name": "X-axis"
                },{
                "color": (245,252,255),
                        "name": "Y-axis"
        }], True, 200, "", "Tilt_XY ")
        graphTilt_XY_Layout = QVBoxLayout()
        graphTilt_XY_Layout.addWidget(self.tiltxy_widget.nameline("Tilt XY",int(((7/1980)/50)*size*self.w),int(((25/880)/50)*size*self.h),int(((13/1980)/50)*size*self.w)))
        graphTilt_XY_Layout.addWidget(self.graphTilt_XY1.graphWidget)
        self.graphTilt_XY = QtWidgets.QWidget()
        self.graphTilt_XY.setFixedWidth(int((430/1980)*self.w))
        self.graphTilt_XY.setFixedHeight(int((230/880)*self.h))
        self.graphTilt_XY.setLayout(graphTilt_XY_Layout)
        self.graphTilt_XY.setStyleSheet("QLabel{color: #f5fcff; font: 10pt  'Oswald';background-color: rgb(3,0,13); }")
#-------graph titlt xy ends------------------------------------------------------------------------------------------------------------
#-------graph 2 widget making starts---------------------------------------------------------------------------------------------------
        GRAPH2_layout = QGridLayout()
        GRAPH2_layout.addWidget(self.graphVoltage,1,1,1,1,QtCore.Qt.AlignCenter)
        GRAPH2_layout.addWidget(self.graphGPS_Altitude,1,2,1,1,QtCore.Qt.AlignCenter)
        GRAPH2_layout.addWidget(self.graphTilt_XY,1,3,1,1,QtCore.Qt.AlignCenter)
        self.GRAPH2_widget = QtWidgets.QWidget()
        self.GRAPH2_widget.setLayout(GRAPH2_layout)
        self.GRAPH2_widget.setStyleSheet("background-color: rgb(30,30,30)")
#-------graph 2 widget ends-------------------------------------------------------------------------------------------------------------
#-------graph widget starts--------------------------------------------------------------------------------------------------------------
        graph_layout = QGridLayout()
        graph_layout.addWidget(self.GRAPH2_widget,2,1,1,1,QtCore.Qt.AlignCenter)
        graph_layout.addWidget(self.GRAPH1_widget,1,1,1,1,QtCore.Qt.AlignCenter)
        self.graph_widget = QtWidgets.QWidget()
        self.graph_widget.setFixedWidth(int((1350/1980)*self.w))
        self.graph_widget.setFixedHeight(int((580/880)*self.h))
        self.graph_widget.setLayout(graph_layout)
#-------graph widget ends--------------------------------------------------------------------------------------------------------------------
#-------gps widget starts----------------------------------------------------------------------------------------------------------------
        self.map = mapWidget()
        self.lat, self.lon = 17.5449,78.5718
        self.map.setFixedWidth(int((450/1980)*self.w))
        self.map.setFixedHeight(int((280/880)*self.h))
        self.map.setStyleSheet("color: rgb(20,20,20)")
#-------gps widget ends-----------------------------------------------------------------------------------------------------------------------
#-------telemtry output from cansat widget starts----------------------------------------------------------------------------------------------------------
        tele_layout = QGridLayout()
        self.logOutput = QtWidgets.QTextEdit()
        self.logOutput.setReadOnly(True)
        self.logOutput.setStyleSheet("background-color: rgb(20,20,20) ;border: 0px ;color: white;font-family: 'Oswald'")
        self.logOutput.setLineWrapMode(QtWidgets.QTextEdit.NoWrap)

        tele_layout.addWidget(self.logOutput)

        self.tele_widget = QtWidgets.QWidget()
        self.tele_widget.setFixedWidth(int((450/1980)*self.w))
        self.tele_widget.setFixedHeight(int((130/880)*self.h))
        self.tele_widget.setStyleSheet("background-color: rgb(30,30,30)")
        self.tele_widget.setLayout(tele_layout)
#-------telemetry output from cansat widget ends-------------------------------------------------------------------------------------------------------------
#-------cmd textbox starts---------------------------------------------------------------------------------------------------------------
        self.tele_cmd_textbox =  QLineEdit()
        self.tele_cmd_textbox.setStyleSheet("background-color: rgb(20,20,20) ;border: 0px ;color: #149414;font-family: 'Oswald'")
        #self.tele_cmd_textbox.setFixedWidth(300)
        self.tele_cmd_textbox.returnPressed.connect(self.OnReturnPressed)
#-------cmd textbox ends-------------------------------------------------------------------------------------------------------------------
#------send button widget starts---------------------------------------------------------------------------------------------------------------
        self.send = QtWidgets.QPushButton()
        self.send.setText("SEND")
        self.send.setStyleSheet("QPushButton{color: #f5fcff; font: %spt  'Oswald';background-color: rgb(20,20,20); }"%int(((8/1980)/50)*size*self.w))
        self.send.setFixedWidth(int((70/1980)*self.w))
        self.send.setFixedHeight(int((15/880)*self.h))
#-------send button widget ends---------------------------------------------------------------------------------------------------------------------
#-------cmd text box plus send button widget starts------------------------------------------------------------------------------------------------
        tele_cmd_textbox_send_layout=QGridLayout()
        tele_cmd_textbox_send_layout.addWidget(self.tele_cmd_textbox,1,1,1,1)
        tele_cmd_textbox_send_layout.addWidget(self.send,1,2,1,1)
        self.tele_cmd_textbox_send_widget = QtWidgets.QWidget()
        self.tele_cmd_textbox_send_widget.setFixedWidth(int((400/1980)*self.w))
        self.tele_cmd_textbox_send_widget.setFixedHeight(int((45/880)*self.h))
        self.tele_cmd_textbox_send_widget.setLayout(tele_cmd_textbox_send_layout)
#-------cmd text box plus send button widget ends-----------------------------------------------------------------------------------------------------
#-------cmd output box from text box widget starts----------------------------------------------------------------------------------------------------
        self.cmdOutput = QtWidgets.QTextEdit()
        self.cmdOutput.setReadOnly(True)
        self.tele_cmd_textbox_send_widget.setFixedWidth(int((400/1980)*self.w))
        self.tele_cmd_textbox_send_widget.setFixedHeight(int((50/880)*self.h))
        self.cmdOutput.setStyleSheet("background-color: rgb(30,30,30) ;border: 0px ;color: #149414;font-family: 'Oswald'")
        self.cmdOutput.setLineWrapMode(QtWidgets.QTextEdit.NoWrap)
        font = self.cmdOutput.font()
        font.setFamily("Oswald")
        font.setPointSize(100)
#-------cmd output box from text box widget ends--------------------------------------------------------------------------------------------------------
#-------cmd textbox plus output box widget starts--------------------------------------------------------------------------------------------------------
        cmd_layout = QGridLayout()
        cmd_layout.addWidget(self.tele_cmd_textbox_send_widget,2,1,1,4)
        cmd_layout.addWidget(self.cmdOutput,1,1,1,5)
        self.cmd_widget = QtWidgets.QWidget()
        self.cmd_widget.setFixedWidth(int((450/1980)*self.w))
        self.cmd_widget.setFixedHeight(int((180/880)*self.h))
        self.cmd_widget.setStyleSheet("background-color: rgb(30,30,30)")
        self.cmd_widget.setLayout(cmd_layout)
#-------cmd textbox plus output box widget ends------------------------------------------------------------------------------------------------------------
#-------packet count widget starts---------------------------------------------------------------------------------------------------------
        self.packet_count=QLabel("Packet Count: 0")
        self.packet_count.setText("Packet Count: 0")
        self.packet_count.setAlignment(QtCore.Qt.AlignCenter)
        packet_count_layout = QHBoxLayout()
        #packet_count_layout.setSpacing(0)
        packet_count_layout.addWidget(self.packet_count)
        self.packet_count_widget = QtWidgets.QWidget()
        self.packet_count_widget.setFixedWidth(int((240/1980)*self.w))
        self.packet_count_widget.setFixedHeight(int((50/880)*self.h))
        self.packet_count_widget.setStyleSheet("QLabel{color: #f5fcff; font: %spt  'Oswald';background-color: rgb(30,30,30); }" %int(((13/1980)/50)*size*self.w))
        self.packet_count_widget.setLayout(packet_count_layout)
#-------packet count widget ends--------------------------------------------------------------------------------------------------------------
#-------corrupted packets widget starts--------------------------------------------------------------------------------------------------------------
        self.corrupted_packets = QLabel("Corrupted Packets: 0")
        self.corrupted_packets.setAlignment(QtCore.Qt.AlignCenter)
        corrupted_packets_layout = QHBoxLayout()
        #corrupted_packets_layout.setSpacing(0)
        corrupted_packets_layout.addWidget(self.corrupted_packets)
        self.corrupted_packets_widget = QtWidgets.QWidget()
        self.corrupted_packets_widget.setFixedWidth(int((240/1980)*self.w))
        self.corrupted_packets_widget.setFixedHeight(int((50/880)*self.h))
        self.corrupted_packets_widget.setStyleSheet("QLabel{color: #f5fcff; font: %spt  'Oswald';background-color: rgb(30,30,30); }" %int(((13/1980)/50)*size*self.w))
        self.corrupted_packets_widget.setLayout(corrupted_packets_layout)
#-------corrupted packet widget ends-----------------------------------------------------------------------------------------------------------------
#-------packet count and corrupted packet widget starts-------------------------------------------------------------------------------------------------
        tele_pac_name_layout = QGridLayout()
        tele_pac_name_layout.addWidget(self.packet_count_widget,1,1,1,1,QtCore.Qt.AlignCenter)
        tele_pac_name_layout.addWidget(self.corrupted_packets_widget,1,2,1,1,QtCore.Qt.AlignCenter)
        self.tele_pac_name_widget = QtWidgets.QWidget()
        self.tele_pac_name_widget.setFixedWidth(int((470/1980)*self.w))
        self.tele_pac_name_widget.setFixedHeight(int((50/880)*self.h))
        self.tele_pac_name_widget.setLayout(tele_pac_name_layout)
#-------packet count and corrupted packet widget ends---------------------------------------------------------------------------------------------------------
#-------full telemetry widget starts---------------------------------------------------------------------------------------------------------------------------
        telemet_layout = QGridLayout()
        self.telemet2_widget = namewidget()
        telemet_layout.addWidget(self.telemet2_widget.nameline("Telemetry",int(((7/1980)/50)*size*self.w),int(((30/880)/50)*size*self.h),int(((16/1980)/50)*size*self.w)),1,1,1,4)
        telemet_layout.addWidget(self.tele_pac_name_widget,2,0,1,4)
        telemet_layout.addWidget(self.tele_widget,3,1,5,1)
        telemet_layout.addWidget(self.cmd_widget,8,1,3,1)
        self.telemet_widget = QtWidgets.QWidget()
        self.telemet_widget.setFixedWidth(int((550/1980)*self.w))
        self.telemet_widget.setFixedHeight(int((440/880)*self.h))
        self.telemet_widget.setLayout(telemet_layout)
#-------telemetry widget ends--------------------------------------------------------------------------------------------------------------------------------------
#-------longitude, latitude , no. of gps widget starts---------------------------------------------------------------------------------------------------------------
        self.longitude = QLabel("Longitude: 00.0000°E")
        self.longitude.setAlignment(QtCore.Qt.AlignCenter)
        self.gps_time = QLabel("GPS Time: 0.0")
        self.gps_time.setAlignment(QtCore.Qt.AlignCenter)
        self.latitude = QLabel("Latitude: 00.0000°N")
        self.latitude.setAlignment(QtCore.Qt.AlignCenter)
        self.gps_location = QLabel("GPS Location")
        self.no_of_gps = QLabel("No. of GPS: 0")
        self.no_of_gps.setAlignment(QtCore.Qt.AlignCenter)

        gps_time_layout = QHBoxLayout()
        gps_time_layout.addWidget(self.gps_time)
        self.gps_time_widget = QtWidgets.QWidget()
        self.gps_time_widget.setFixedWidth(int((220/1980)*self.w))
        self.gps_time_widget.setFixedHeight(int((50/880)*self.h))
        self.gps_time_widget.setStyleSheet("QLabel{color: #f5fcff; font: %spt  'Oswald';background-color: rgb(30,30,30); }" %int(((13/1980)/50)*size*self.w))
        self.gps_time_widget.setLayout(gps_time_layout)

        no_of_gps_layout = QHBoxLayout()
        no_of_gps_layout.addWidget(self.no_of_gps)
        self.no_of_gps_widget = QtWidgets.QWidget()
        self.no_of_gps_widget.setFixedWidth(int((220/1980)*self.w))
        self.no_of_gps_widget.setFixedHeight(int((50/880)*self.h))
        self.no_of_gps_widget.setStyleSheet("QLabel{color: #f5fcff; font: %spt  'Oswald';background-color: rgb(30,30,30); }" %int(((13/1980)/50)*size*self.w))
        self.no_of_gps_widget.setLayout(no_of_gps_layout)


        latitude_layout = QHBoxLayout()
        latitude_layout.addWidget(self.latitude)
        self.latitude_widget = QtWidgets.QWidget()
        self.latitude_widget.setFixedWidth(int((220/1980)*self.w))
        self.latitude_widget.setFixedHeight(int((50/880)*self.h))
        self.latitude_widget.setStyleSheet("QLabel{color: #f5fcff; font: %spt  'Oswald';background-color: rgb(30,30,30); }" %int(((13/1980)/50)*size*self.w))
        self.latitude_widget.setLayout(latitude_layout)

        longitude_layout = QHBoxLayout()
        longitude_layout.addWidget(self.longitude)
        self.longitude_widget = QtWidgets.QWidget()
        self.longitude_widget.setFixedWidth(int((220/1980)*self.w))
        self.longitude_widget.setFixedHeight(int((50/880)*self.h))
        self.longitude_widget.setStyleSheet("QLabel{color: #f5fcff; font: %spt  'Oswald';background-color: rgb(30,30,30); }"%int(((13/1980)/50)*size*self.w))
        self.longitude_widget.setLayout(longitude_layout)
#-------longitude and latitude widget---------------------------------------------------------------------------------------------------
        line2_layout = QGridLayout()
        line2_layout.addWidget(self.gps_time_widget,0,1,1,1)
        line2_layout.addWidget(self.no_of_gps_widget,0,2,1,1)
        self.line2_widget = QtWidgets.QWidget()
        self.line2_widget.setFixedWidth(int((500/1980)*self.w))
        self.line2_widget.setFixedHeight(int((50/880)*self.h))
        self.line2_widget.setLayout(line2_layout)
#------no of gps and gps altitude widget:
        lines_layout = QGridLayout()
        lines_layout.addWidget(self.latitude_widget,0,1,1,1)
        lines_layout.addWidget(self.longitude_widget,0,2,1,1)
        self.lines_widget = QtWidgets.QWidget()
        self.lines_widget.setFixedWidth(int((500/1980)*self.w))
        self.lines_widget.setFixedHeight(int((50/880)*self.h))
        self.lines_widget.setLayout(lines_layout)
# ----- ends --------------------------------------------
#------latitude and longitude widget ends--------------------------------------------------------------------------------------------------
        gps_label_layout = QGridLayout()
        self. gps_label_layout_widget = namewidget()
        gps_label_layout.addWidget(self.gps_label_layout_widget.nameline("GPS Location",int(((7/1980)/50)*size*self.w),int(((30/880)/50)*size*self.h),int(((16/1980)/50)*size*self.w)),1,0,1,1)
        gps_label_layout.addWidget(self.line2_widget,2,0,1,1)
        gps_label_layout.addWidget(self.lines_widget,3,0,1,1)
        gps_label_layout.addWidget(self.map,4,0,1,1)
        self.gps_label_widget = QtWidgets.QWidget()
        self.gps_label_widget.setFixedWidth(int((500/1980)*self.w))
        self.gps_label_widget.setFixedHeight(int((450/880)*self.h))
        self.gps_label_widget.setLayout(gps_label_layout)
#-------longitude, latitude , no. of gps widget ends--------------------------------------------------------------------------------------------------------
#-------map and gps widget starts-------------------------------------------------------------------------------------------------------------------
        gps_layout = QGridLayout()
        gps_layout.addWidget(self.gps_label_widget,1,0,1,1)
        gps_layout.addWidget(self.telemet_widget,2,0,1,1)
        self.gps_widget = QtWidgets.QWidget()
        self.gps_widget.setLayout(gps_layout)
        self.gps_widget.setFixedWidth(int((500/1980)*self.w))
        self.gps_widget.setFixedHeight(int((880/880)*self.h))
        self.gps_widget.setStyleSheet("background-color: rgb(20,20,20)")
#-------map and gps widget ends--------------------------------------------------------------------------------------
#-------main window starts--------------------------------------------------------------------------------------------
        MAIN_layout = QGridLayout()
        MAIN_layout.addWidget(self.MENU5_widget,1,0,1,1)
        MAIN_layout.addWidget(self.button_widget,2,0,1,1)
        MAIN_layout.addWidget(self.graph_widget,3,0,1,1)
        self.MAIN_widget = QtWidgets.QWidget()
        self.MAIN_widget.setLayout(MAIN_layout)

        all_layout = QGridLayout()
        #sizegrip = QtWidgets.QSizeGrip(MainWindow)
        #all_layout.addWidget(sizegrip, 0, QtCore.Qt.AlignBottom  QtCore.Qt.AlignRight)
        all_layout.addWidget(self.MAIN_widget,1,1,1,1)
        all_layout.addWidget(self.gps_widget,1,2,1,1)
        self.all_widget = QtWidgets.QWidget()
        self.all_widget.setLayout(all_layout)
        self.all_widget.setStyleSheet("background-color: rgb(15,15,15)")
        #self.setFixedSize(self.all_widget.sizeHint())
        self.setCentralWidget(self.all_widget)

        
        self.send_thread = SendDataThread()
        self.receive_thread = ReceiveDataThread()
        self.receiving_timer = QTimer()
        self.receiving_timer.timeout.connect(self.receiver)
        self.receiving_timer.start(500)
        
        self.corruptedPacketsValue = 0
        self.i = 0
        
    def receiver(self):
                global packet
                self.receive_thread.start() 
                try:
                        if (packet is not None ) and (packet!="") and ("error" not in packet):
                                self.connector.update_color("green")
                                self.update(packet)
                                #self.connector.update_color("green")
                                packet = ""
                        if ("error" in packet):
                               self.onGettingData(packet)
                        if (SendDataThread.remote.read_device_info() is not None):
                                self.gps_altitude_widget1.update_color("red")
                                self.tiltxy_widget.update_color("red")
                                self.voltage_widget.update_color("red")
                                self.pressure_widget.update_color("red")
                                self.temperature_widget.update_color("red")
                                self.altitude_widget.update_color("red")
                                self.telemet2_widget.update_color("red")
                                self.gps_label_layout_widget.update_color("red")
                                #self.connector.update_color("red")"""

                        else:
                               
                               
                               #print("Packet not received")
                               self.connector.update_color("red")
                except :
                       #self.onGettingData("Packet not received")
                       pass

           #self.receive_thread.data_received.connect(self.update)
           
           

    def OnReturnPressed(self):
        """ the text is retrieved from tele_cmd_textbox """
        text = self.tele_cmd_textbox.text() + "\n"
        # do some thing withit
        self.cmdoutput(text)
        text = text+"\n"
        self.sending(text)

    def send_simulation(self,file_path):
                global simp
                file = open(f"{file_path}","r")
                simp1 = file.readlines()
                simp=[]
                for line in simp1:
                        if line[0] !="#":
                                simp.append(line.strip('\n'))
                while("" in simp):
                        simp.remove("")

                simp = [sub.replace('$', '2027') for sub in simp]
                #print(simp)
                #self.sending(simp)



    
    def telemetry_button(self):
        if self.button_name1.isChecked():
            self.button_name1.setStyleSheet("QPushButton{color: #f5fcff; font: %spt  'Oswald';background-color: rgb(10,10,10); }" % int((12/1980)*width) )
            check = "OFF"
        else:
            self.button_name1.setStyleSheet("QPushButton{color: #f5fcff; font: %spt  'Oswald';background-color: rgb(30,30,30); }" % int((12/1980)*width) )
            check = "ON"
        DATA_TO_SEND = "CMD,2027,CX," + str(check) + "\n"
        self.sending(DATA_TO_SEND)
        #print(DATA_TO_SEND,"HI")
    def audio_beacon_button(self):
        if self.button_name7.isChecked():
            self.button_name7.setStyleSheet("QPushButton{color: #f5fcff; font: %spt  'Oswald';background-color: rgb(10,10,10); }" % int((12/1980)*width) )
            check = "ON"
        else:
            self.button_name7.setStyleSheet("QPushButton{color: #f5fcff; font: %spt  'Oswald';background-color: rgb(30,30,30); }" % int((12/1980)*width) )
            check = "OFF"
        DATA_TO_SEND = "CMD,2027,BCN," + str(check) + "\n"
        self.sending(DATA_TO_SEND)
        #print(DATA_TO_SEND,"HI")
    def deploy_nose_button(self):
        if self.button_name8.isChecked():
            self.button_name8.setText("Lock Nosecone")
            self.button_name8.setStyleSheet("QPushButton{color: #f5fcff; font: %spt  'Oswald';background-color: rgb(10,10,10); }" % int((12/1980)*width) )
            check = "DEPLOY_NOSE"
        else:
            self.button_name8.setText("Deploy Nosecone")
            self.button_name8.setStyleSheet("QPushButton{color: #f5fcff; font: %spt  'Oswald';background-color: rgb(30,30,30); }" % int((12/1980)*width) )
            check = "LOCK_NOSE"
        DATA_TO_SEND = "CMD,2027," + str(check) + "\n"
        self.sending(DATA_TO_SEND)
        #print(DATA_TO_SEND,"HI")
    def deploy_para_button(self):
        if self.button_name9.isChecked():
            self.button_name9.setText("Lock Parachute")
            self.button_name9.setStyleSheet("QPushButton{color: #f5fcff; font: %spt  'Oswald';background-color: rgb(10,10,10); }" % int((12/1980)*width) )
            check = "DEPLOY_PARA"
        else:
            self.button_name9.setText("Deploy Parachute")
            self.button_name9.setStyleSheet("QPushButton{color: #f5fcff; font: %spt  'Oswald';background-color: rgb(30,30,30); }" % int((12/1980)*width) )
            check = "LOCK_PARA"
        DATA_TO_SEND = "CMD,2027," + str(check) + "\n"
        self.sending(DATA_TO_SEND)
        #print(DATA_TO_SEND,"HI")
    def reset_button(self):
        if self.button_name10.isChecked():
            self.button_name10.setStyleSheet("QPushButton{color: #f5fcff; font: %spt  'Oswald';background-color: rgb(10,10,10); }" % int((12/1980)*width) )
            res = "CMD,2027,RESET\n"
            self.sending(res)
  
        else:
            self.button_name10.setStyleSheet("QPushButton{color: #f5fcff; font: %spt  'Oswald';background-color: rgb(30,30,30); }" % int((12/1980)*width) )
    
    def calibration_button(self):
        if self.button_name2.isChecked():
            self.button_name2.setStyleSheet("QPushButton{color: #f5fcff; font: %spt  'Oswald';background-color: rgb(10,10,10); }" % int((12/1980)*width) )
            cal = "CMD,2027,CAL\n"
            self.sending(cal)
  
        else:
            self.button_name2.setStyleSheet("QPushButton{color: #f5fcff; font: %spt  'Oswald';background-color: rgb(30,30,30); }" % int((12/1980)*width) )
        print(cal)
    def set_time_utc_button(self):
        if self.button_name3.isChecked():
            self.button_name3.setStyleSheet("QPushButton{color: #f5fcff; font: %spt  'Oswald';background-color: rgb(10,10,10); }" % int((12/1980)*width) )
            now_utc = datetime.now(timezone.utc)
            time_utc = now_utc.time()
            b = time_utc.strftime('%H:%M:%S')
            utc = "CMD,2027,ST," + b + "\n"
            self.sending(utc)
        else:        
            self.button_name3.setStyleSheet("QPushButton{color: #f5fcff; font: %spt  'Oswald';background-color: rgb(30,30,30); }" % int((12/1980)*width) )  
    def set_time_gps_button(self):
        if self.button_name4.isChecked():
            self.button_name4.setStyleSheet("QPushButton{color: #f5fcff; font: %spt  'Oswald';background-color: rgb(10,10,10); }" % int((12/1980)*width) )
            gps = "CMD,2027,ST,GPS" + "\n"
            self.sending(gps)
        else:
            self.button_name4.setStyleSheet("QPushButton{color: #f5fcff; font: %spt  'Oswald';background-color: rgb(30,30,30); }" % int((12/1980)*width) )
           
    def simulation_enabled_button(self):
        global check_sim, sim
        if self.button_name5.isChecked() :
                self.button_name5.setText("Simulation-Disable")
                self.button_name5.setStyleSheet("QPushButton{color: #f5fcff; font: %spt  'Oswald';background-color: rgb(10,10,10); }" % int((12/1980)*width) )
                check_sim = 1
                val = "ENABLE"
                self.button_name6.setStyleSheet("QPushButton{color: #f5fcff; font: %spt  'Oswald';background-color: rgb(30,30,30); }" % int((12/1980)*width) )
        else:
                self.button_name5.setText("Simulation-Enable")
                self.button_name5.setStyleSheet("QPushButton{color: #f5fcff; font: %spt  'Oswald';background-color: rgb(30,30,30); }" % int((12/1980)*width) )
                val = "DISABLE"
                check_sim = 0
                self.button_name6.setText("Simulation-Activate")
                self.button_name6.setStyleSheet("QPushButton{color: rgb(200,200,200); font: %spt  'Oswald';background-color: rgb(10,10,10); }" % int((12/1980)*width) )

        sim = "CMD,2027,SIM," + val + "\n"
        self.sending(sim)
        #print(sim)
            
    def simulation_activate_button(self):
        global sima,simp
        if check_sim == 1:
                if self.button_name6.isChecked() :
                        self.button_name6.setStyleSheet("QPushButton{color: #f5fcff; font: %spt  'Oswald';background-color: rgb(10,10,10); }" % int((12/1980)*width) )
                        self.button_name6.setText("Simulation-Deactivate")
                        val = "ACTIVATE"
                        self.sending_timer_simp = QTimer()
                        self.sending_timer_simp.timeout.connect(self.send_sim_data)
                        self.sending_timer_simp.start(1000)
                        

                else:
                        self.sending_timer_simp.stop()
                        self.button_name6.setText("Simulation-Activate")
                        self.button_name6.setStyleSheet("QPushButton{color: #f5fcff; font: %spt  'Oswald';background-color: rgb(0,0,0); }" % int((12/1980)*width) )
                        val = "DISABLE"

        if check_sim == 0:
                if self.button_name6.isChecked() :
                        self.button_name6.setStyleSheet("QPushButton{color: rgb(200,200,200); font: %spt  'Oswald';background-color: rgb(10,10,10); }" % int((12/1980)*width) )
                        self.button_name6.setText("Simulation-Deactivate")
                
                else:
                        self.button_name6.setText("Simulation-Activate")
                        self.button_name6.setStyleSheet("QPushButton{color: rgb(200,200,200); font: %spt  'Oswald';background-color: rgb(10,10,10); }" % int((12/1980)*width) )



        sima = "CMD,2027,SIM," + val + "\n"
        self.sending(sima)
        #print(sima)
        #audio beacon - CMD,2027,BCN,ON / CMD,2027,BCN,OFF - reset

    def send_sim_data(self):
                try:
                        self.sending(simp[0])
                        del simp[0]
                        #self.sending(simp[0])
                        
        #starts to send data from simp
                except:
                        pass
           

    @pyqtSlot()
    def sending(self, send):

        global DATA_TO_SEND
        DATA_TO_SEND = send
        
        self.send_thread.start()
   
    #@pyqtSlot(str)
    def update(self,packet):
        #device.close()
        if packet:
                self.my_packet = open("packet.txt","a+")
                self.my_packet.write(packet+"\n")
                self.my_packet.close()
                self.lis = list(packet.split(","))
                print(packet)
                packet = ""
               


        try:
                self.teamIdValue = int(self.lis[0])
        except:
                self.teamIdValue = 0
        try:
                self.missionTimeValue = self.lis[1]
        except:
                self.missionTimeValue = ""
        try:
                self.packetCountValue = int(self.lis[2])
        except:
               pass
                #self.packetCountValue = self.packetCountValue
        try:
                self.modeValue = self.lis[3].strip() #f or s
        except:
                self.modeValue = ""
        try:
                self.stateValue = self.lis[4].strip() # launch_wait, ascent, rock_sep. descent, hs_released , landed
        except:
                self.stateValue = ""
        try:
                self.altitudeValue = float(self.lis[5]) #00-1.78
        except:
                self.altitudeValue = 0.0
        try:
                self.airSpeedValue = float(self.lis[6])
        except:
                self.airSpeedValue = 0.0
        try:
                self.hsDeployedValue = self.lis[7]
        except:
                self.hsDeployedValue = ""
        try:
                self.pcDeployedValue = self.lis[8]
        except:
                self.pcDeployedValue = ""
        
        try:
                self.temperatureValue = float(self.lis[9])
                
        except:
                self.temperatureValue = 0.0
        try:
                self.voltageValue = float(self.lis[10])
                
        except:
                self.voltageValue = 0.0
        try:
                self.pressureValue = float(self.lis[11])
        except:
                self.pressureValue = 0.0
        try:
                self.gpsTimeValue = self.lis[12]
        except:
                self.gpsTimeValue = ""
        try:
                self.gpsAltitudeValue = float(self.lis[13])
        except:
                self.gpsAltitudeValue = 0.0
        try:
                
                self.gpsLatitudeValue = float(self.lis[14])
        except:
                self.gpsLatitudeValue = 0.0
        try:
                self.gpsLongitudeValue = float(self.lis[15])
                
        except:
                self.gpsLongitudeValue = 0.0
        try:
                self.noOfGpsValue = int(self.lis[16])
        except:
                self.noOfGpsValue = 0
        try:
                self.tiltXValue = float(self.lis[17])
        except:
                self.tiltXValue = 0.0
        try:
                self.tiltYValue = float(self.lis[18])
        except:
                self.tiltYValue = 0.0
        try:
                self.rotZValue = float(self.lis[19])
        except:
                self.rotZValue = 0.0
        try:
                self.cmdEchoValue = self.lis[20]
        except:
                self.cmdEchoValue = ""
        
       
        try:
                if self.modeValue == "S":
                        pass
        
        except:
                pass
        
        try:
        
                self.q = ""
                for x in range(21):
                        self.q+="*"
                        if self.q in self.lis:
                                self.corruptedPacketsValue +=1
                                r=0
                                break
                        else:
                                self.corruptedPacketsValue+=0
                                r=1
                
                self.i += 1
        except:
               pass
        try: 
                if ("*" not in  self.lis[17]) or ("*" not in  self.lis[18]) :
                                self.tiltxy_widget.update_color("rgb(59, 146, 184)")
                else:
                        self.tiltxy_widget.update_color("red")
        except:
                pass
        try:

                if ("*" not in  self.lis[13])  :
                                self.gps_altitude_widget1.update_color("rgb(59, 146, 184)")
                else:
                                self.gps_altitude_widget1.update_color("red")
        except:
                pass

        try:
                if ("*" not in  self.lis[10]) :

                        self.voltage_widget.update_color("rgb(59, 146, 184)")
                else:
                        self.voltage_widget.update_color("red")
        except:
                pass

        try:

                if ("*" not in  self.lis[11])  :
                        self.pressure_widget.update_color("rgb(59, 146, 184)")
                else:
                        self.pressure_widget.update_color("red")
        except:
                pass

        try:

                if ("*" not in  self.lis[9]) :
                        self.temperature_widget.update_color("rgb(59, 146, 184)")
                else:
                        self.temperature_widget.update_color("red")
                
        except:
                pass

        try:
                
                if ("*" not in  self.lis[5]) :
                        self.altitude_widget.update_color("rgb(59, 146, 184)")
                else:
                        self.altitude_widget.update_color("red")
        except:
                pass

        try:

                if  r==1:
                        self.telemet2_widget.update_color("rgb(59, 146, 184)")
                else :
                        self.telemet2_widget.update_color("red")
        except:
                pass

        try:
                if ("*" not in  self.lis[12]) and ("*" not in  self.lis[14]) and ("*" not in  self.lis[15]) and ("*" not in  self.lis[12]) :
                        self.gps_label_layout_widget.update_color("rgb(59, 146, 184)")
                else:
                        self.gps_label_layout_widget.update_color("red")

        except:
                pass

        try:
               self.tiltxy_widget.update_name("Tilt XY : " + "X : " + str(self.tiltXValue) + ", Y : " + str(self.tiltYValue))

        except:
               pass

        try:
               self.gps_altitude_widget1.update_name("GPS Altitude : " +  str(self.gpsAltitudeValue))
        except:
               pass

        try:
               self.voltage_widget.update_name("Voltage : " + str(self.voltageValue))
        except:
               pass

        try:
               self.altitude_widget.update_name("Altitude : " +  str(self.altitudeValue))
        except:
               pass

        try:
               self.temperature_widget.update_name("Temperature : " + str(self.temperatureValue))
        except:
               pass

        try:
               self.pressure_widget.update_name("Pressure : " + str(self.pressureValue))
        except:
               pass





        try:
                self.graphPressure1.update(self.i,[ self.pressureValue])
        except:
                pass
        try:
                self.graphTemperature1.update(self.i,[ self.temperatureValue])
        except:
                pass
        try:
                self.graphAltitude1.update(self.i,[ self.altitudeValue])
        except:
                pass
        try:
                self.graphVoltage1.update(self.i,[ self.voltageValue])
        except:
                pass
        try:
                self.graphGPS_Altitude1.update(self.i,[ self.gpsAltitudeValue])
        except:
                pass
        try:    
                self.graphTilt_XY1.update(self.i,[ self.tiltXValue,self.tiltYValue])
        except:
                pass
        try:
                self.lat = self.gpsLatitudeValue
        #if self.i%2 == 0:
        except:
                self.lat = 0
        try:
                self.lon = self.gpsLongitudeValue
        except:
                self.lon = 0
        try:
                self.map.update(self.lat, self.lon)
        except:
               pass
        #printing the simp from text or csv file
        """
        if  (self.i<= len(simp) - 1):
                print(simp[int(self.i)])"""
        try:
                self.team_label.setText("Team ID:" + str(self.teamIdValue))
        except:
                pass
        try:
                self.packet_count.setText("Packet Count: " + str(self.packetCountValue))
        except:
                pass
        try:
                self.no_of_gps.setText("No. of GPS: " + str(self.noOfGpsValue))
        except:
                pass
        try:
                self.gps_time.setText("GPS Time: " + str(self.gpsTimeValue))
        except:
                pass
        try:
                self.latitude.setText("Latitude: "+ "{:.4f}".format(self.lat))
        except:
                pass
        try:
                self.longitude.setText("Longitude: " + "{:.4f}".format(self.lon) )
        except:
                pass
        try:
                self.corrupted_packets.setText("Corrupted Packets: "+str(self.corruptedPacketsValue))
        except:
                pass
        is_launch_wait, is_ascent, is_descent, is_heat_shield_deployed, is_landed,   is_rocket_separated = 0,0,0,0,0,0

        

        if (self.stateValue == "IDLE"):
                is_launch_wait, is_ascent, is_descent, is_heat_shield_deployed, is_landed,   is_rocket_separated = 0,0,0,0,0,0


        if (self.stateValue == "LAUNCH_WAIT"):
                is_launch_wait =  1

        if (self.stateValue == "ASCENT"):
                is_ascent =  1
                is_launch_wait =  1
        
        if (self.stateValue == "DESCENT"):
                is_ascent =  1
                is_launch_wait =  1
                is_descent = 1

        
        if (self.hsDeployedValue == "P"):
                is_heat_shield_deployed = 1
                is_ascent =  1
                is_launch_wait =  1
                is_descent = 1
        
        if (self.pcDeployedValue == "C"):
                is_parachute_deployed = 1
                is_heat_shield_deployed = 1
                is_ascent =  1
                is_launch_wait =  1
                is_descent = 1
        
        
        if (self.stateValue == "LANDED"):
                is_landed = 1
                is_parachute_deployed = 1
                is_heat_shield_deployed = 1
                is_ascent =  1
                is_launch_wait =  1
                is_descent = 1

        

        if (is_launch_wait==1):
                self.dot1.setText("🟢")
        else:
                self.dot1.setText("🔴")
        
        if is_descent==1:
                self.dot2.setText("🟢")
        else:
                self.dot2.setText("🔴")

        if is_ascent==1:
                self.dot3.setText("🟢")
        else:
                self.dot3.setText("🔴")

        if is_heat_shield_deployed==1:
                self.dot4.setText("🟢")
        else:
                self.dot4.setText("🔴")

        if is_rocket_separated==1:
                self.dot5.setText("🟢")
        else:
                self.dot5.setText("🔴")

        if is_landed==1:
                self.dot6.setText("🟢")
        else:
                self.dot6.setText("🔴")

        

        

        currstate = [is_launch_wait, is_ascent, is_rocket_separated,  is_descent, is_heat_shield_deployed, is_landed]
        allstate = ["Launch Wait","Ascent","Rocket Separated", "Descent","Heat Shield Deployed","Landed",]
        i = currstate.index(0)
        curstate = allstate[i-1]

        self.state.setText("Current State:"+ str(self.stateValue))

        if self.modeValue == "S":

                self.mode_name.setText("Mode: " +"SIMULATION" )
        if self.modeValue == "F":
                self.mode_name.setText("Mode: " +"FLIGHT" )
        
        packet = ""
            
        
    def mission_time(self):
        now_utc = datetime.now(timezone.utc)
        time_utc = now_utc.time()
        v = time_utc.strftime('%H:%M:%S')
        cont1 = list(v.split(":"))
        cont=[]
        for i in range(len(cont1)):
                a = cont1[i]
                a = int(a)
                cont+=[a]
        cont[0] = cont[0]*3600
        cont[1] = cont[1]*60
        cont = cont[0] + cont[1] + cont[2]
        self.time = cont
        m = self.time//60
        s = self.time%60
        h = m//60
        m = m%60
        tim = "{:02d}:{:02d}:{:02d}".format(h,m,s)
        self.time+=1
                
        self.MENU2_mission_time.setText("Mission Time:"+str(tim))

    
    def onGettingData(self, texts):
        #input from cansat
        text = texts
        # do some thing withit
        self.log_output(text+"\n")

    def log_output(self,text):
        self.logOutput.moveCursor(QTextCursor.End)
        self.logOutput.insertPlainText(text)
        sb = self.logOutput.verticalScrollBar()
        sb.setValue(sb.maximum())
    def cmdoutput(self,text):
        self.cmdOutput.moveCursor(QTextCursor.End)
        self.cmdOutput.insertPlainText(text)
        sb = self.cmdOutput.verticalScrollBar()
        sb.setValue(sb.maximum())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    #main_window.receive_thread.moveToThread(QThread())

    main_window.show()
    sys.exit(app.exec_())


