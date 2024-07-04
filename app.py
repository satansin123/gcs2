import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QDialog, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt, QObject, QThread, pyqtSignal, pyqtSlot
from digi.xbee.devices import XBeeDevice
from PyQt5 import *
from PyQt5 import QtWidgets
from PyQt5 import QtCore, QtGui
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

#if a is 0 then dark mode, if a is 1 then light mode
a = 1

if a == 0:
#dark mode
        color_text = "rgb(204, 204, 204)"
        color_text_graph = "#ffffff"
        color_text_activate = "rgb(200,200,200)"
        color_text_label = "rgb(204, 204, 204)"
        color_text2 = "rgb(204, 204, 204)"
        color_graph = (20,20,20)
        color_graph_line = (255,255,255)
        color_background1 = "#303030"
        color_background_activate = "rgb(10,10,10)"
        color_background2 = "#151515"
        color_background3 = "#202020"
        color_background_graph = "rgb(3,0,13)"
        color_background_cmd = "rgb(15,15,15)"
        color_background_btn = "rgb(10,10,10)"
        color_background_btn = "rgb(0,0,0)"
else:
#light mode

        color_text = "rgb(0,0,0)"
        color_text_graph = "#000000"
        color_text_activate = "rgb(56,56,56)"
        color_text_label = "rgb(0,0,0)"
        color_text2 = "rgb(0,0,0)"
        color_graph = (242,236,231)
        color_graph_line = (0,0,0)
        color_background1 = "#d6c3ab"
        color_background_activate = "rgb(10,10,10)"
        color_background2 = "#f2ece7"
        color_background3 = "#f2ecdd"
        color_background_graph = "rgb(3,0,13)"
        color_background_cmd = "rgb(15,15,15)"
        color_background_btn = "rgb(10,10,10)"
        color_background_btn = "rgb(0,0,0)"

try:
        PORT = "COM15"  # Replace with your actual port
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
                        
                        remote  = RemoteXBeeDevice(device,XBee64BitAddress.from_hex_string("0013A20041A38CD0"))
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
        self.setStyleSheet("QWidget {{margin:0; padding:0; font-size:15px; background-color: #f2ece7;}}")
        def buttonfunc(name,fontsize):
            button_layout=QHBoxLayout()
            if name=="Telemetry":
                    self.button_name1= QtWidgets.QPushButton()
                    #self.button_name1.setCheckable(True)
                    self.button_name1.setText(name)
                    self.button_name1.setCheckable(True)
                    self.button_name1.setStyleSheet("QPushButton{{color: {2}; font: {0}pt 'Oswald'; background-color: {1}; }}".format(fontsize, color_background1, color_text ))
                    button_layout.addWidget(self.button_name1)
                    self.y = True
                    self.button_name1.clicked.connect(self.telemetry_button)
            if name=="Calibration":
                    self.button_name2= QtWidgets.QPushButton()
                    self.button_name2.setText(name)
                    self.button_name2.setCheckable(True)
                    self.button_name2.setStyleSheet("QPushButton{{color: {2}; font: {0}pt 'Oswald'; background-color: {1}; }}".format(fontsize, color_background1, color_text ))
                    button_layout.addWidget(self.button_name2)
                    self.button_name2.clicked.connect(self.calibration_button)
            if name=="Set Time UTC":
                    self.button_name3= QtWidgets.QPushButton()
                    self.button_name3.setText(name)
                    self.button_name3.setCheckable(True)
                    self.button_name3.setStyleSheet("QPushButton{{color: {2}; font: {0}pt 'Oswald'; background-color: {1}; }}".format(fontsize, color_background1, color_text ))
                    button_layout.addWidget(self.button_name3)
                    self.button_name3.clicked.connect(self.set_time_utc_button)
            if name=="Set Time GPS":
                    self.button_name4= QtWidgets.QPushButton()
                    self.button_name4.setText(name)
                    self.button_name4.setCheckable(True)
                    self.button_name4.setStyleSheet("QPushButton{{color: {2}; font: {0}pt 'Oswald'; background-color: {1}; }}".format(fontsize, color_background1, color_text ))
                    button_layout.addWidget(self.button_name4)
                    self.button_name4.clicked.connect(self.set_time_gps_button)
            if name=="Simulation-Enable":
                    self.button_name5= QtWidgets.QPushButton()
                    self.button_name5.setText(name)
                    self.button_name5.setCheckable(True)
                    self.button_name5.setStyleSheet("QPushButton{{color: {2}; font: {0}pt 'Oswald'; background-color: {1}; }}".format(fontsize, color_background1, color_text ))
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
                    self.button_name7.setStyleSheet("QPushButton{{color: {2}; font: {0}pt 'Oswald'; background-color: {1}; }}".format(fontsize, color_background1, color_text ))
                    button_layout.addWidget(self.button_name7)
                    self.button_name7.clicked.connect(self.audio_beacon_button)
            if name=="Deploy-Nosecone":
                    self.button_name8= QtWidgets.QPushButton()
                    self.button_name8.setCheckable(True)
                    self.button_name8.setText(name)
                    self.button_name8.setStyleSheet("QPushButton{{color: {2}; font: {0}pt 'Oswald'; background-color: {1}; }}".format(fontsize, color_background1, color_text ))
                    button_layout.addWidget(self.button_name8)
                    self.button_name8.clicked.connect(self.deploy_nose_button)
            if name=="Deploy-Parachute":
                    self.button_name9= QtWidgets.QPushButton()
                    self.button_name9.setCheckable(True)
                    self.button_name9.setText(name)
                    self.button_name9.setStyleSheet("QPushButton{{color: {2}; font: {0}pt 'Oswald'; background-color: {1}; }}".format(fontsize, color_background1, color_text ))
                    button_layout.addWidget(self.button_name9)
                    self.button_name9.clicked.connect(self.deploy_para_button)
            if name=="Reset":
                    self.button_name10= QtWidgets.QPushButton()
                    self.button_name10.setCheckable(True)
                    self.button_name10.setText(name)
                    self.button_name10.setStyleSheet("QPushButton{{color: {2}; font: {0}pt 'Oswald'; background-color: {1}; }}".format(fontsize, color_background1, color_text ))
                    button_layout.addWidget(self.button_name10)
                    self.button_name10.clicked.connect(self.show_reset_confirmation)


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
                    self.dot1.setStyleSheet("QLabel{{color: {0}; font: {1}pt 'Oswald'; background-color: {2};}}".format(color_text_label, fontsize, color_background1))
                    layout.addWidget(self.dot1,1,1,1,1)
            if state == "Descent":
                    self.dot2= QLabel("🔴")
                    self.dot2.setText("🔴")
                    self.dot2.setStyleSheet("QLabel{{color: {0}; font: {1}pt 'Oswald'; background-color: {2};}}".format(color_text_label, fontsize, color_background1))
                    layout.addWidget(self.dot2,1,1,1,1)
            if state == "Ascent":
                    self.dot3= QLabel("🔴")
                    self.dot3.setText("🔴")
                    self.dot3.setStyleSheet("QLabel{{color: {0}; font: {1}pt 'Oswald'; background-color: {2};}}".format(color_text_label, fontsize, color_background1))
                    layout.addWidget(self.dot3,1,1,1,1)
            if state == "HS Released":
                    self.dot4= QLabel("🔴")
                    self.dot4.setText("🔴")
                    self.dot4.setStyleSheet("QLabel{{color: {0}; font: {1}pt 'Oswald'; background-color: {2};}}".format(color_text_label, fontsize, color_background1))
                    layout.addWidget(self.dot4,1,1,1,1)
            if state == "Rocket Separation":
                    self.dot5= QLabel("🔴")
                    self.dot5.setText("🔴")
                    self.dot5.setStyleSheet("QLabel{{color: {0}; font: {1}pt 'Oswald'; background-color: {2};}}".format(color_text_label, fontsize, color_background1))
                    layout.addWidget(self.dot5,1,1,1,1)
            if state == "Landed":
                    self.dot6= QLabel("🔴")
                    self.dot6.setText("🔴")
                    self.dot6.setStyleSheet("QLabel{{color: {0}; font: {1}pt 'Oswald'; background-color: {2};}}".format(color_text_label, fontsize, color_background1))
                    layout.addWidget(self.dot6,1,1,1,1)
            
            
            state_label.setStyleSheet("QLabel{{color: {0}; font: {1}pt 'Oswald'; background-color: {2};}}".format(color_text, fontsize, color_background1))


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
        logo_layout.setAlignment(Qt.AlignLeft)
#-------logowidget ends----------------------------------

        

        #-------team id widget starts---------------------------------------------------------------------
        self.team_label = QLabel('TEAM ID:2027')
        self.team_label.setAlignment(QtCore.Qt.AlignCenter)
        team_layout = QVBoxLayout()
        team_layout.addWidget(self.team_label)
        self.team_widget = QtWidgets.QWidget()
        self.team_widget.setFixedWidth(int((230/1980)*self.w))
        self.team_widget.setFixedHeight(int((50/880)*self.h))
        
        self.team_widget.setLayout(team_layout)
        
        self.team_widget.setStyleSheet("QLabel{{color: {0}; font: {1}pt 'Oswald'; background-color: {2};}}".format(color_text, int(((20/1980)/50)*size*self.w), color_background2))

#-------team id widget ends---------------------------
        #-------team id widget starts---------------------------------------------------------------------
        self.mis = QLabel('Mission Time : ')
        self.mis.setAlignment(QtCore.Qt.AlignCenter)
        mis_layout = QVBoxLayout()
        mis_layout.addWidget(self.mis)
        self.mis_widget = QtWidgets.QWidget()
        self.mis_widget.setFixedWidth(int((230/1980)*self.w))
        self.mis_widget.setFixedHeight(int((40/880)*self.h))
        
        self.mis_widget.setLayout(mis_layout)
        
        self.mis_widget.setStyleSheet("QLabel{{color: {0}; font: {1}pt 'Oswald'; background-color: {2};}}".format(color_text, int(((11/1980)/50)*size*self.w), color_background2))

#-------team id widget ends---------------------------
        
        #-------logo plus team id combined widget starts----------------------------------------------------
        MENU1_layout = QVBoxLayout()
        MENU1_layout.setSpacing(0)
        #MENU1_layout.addWidget(self.logo2_widget,1,0,1,1,QtCore.Qt.AlignVCenter)
        MENU1_layout.addWidget(self.logo_widget)
        MENU1_layout.addWidget(self.team_widget)
        MENU1_layout.addWidget(self.mis_widget)
        self.MENU1_widget = QtWidgets.QWidget()
        self.MENU1_widget.setLayout(MENU1_layout)
        self.MENU1_widget.setFixedWidth(int((240/1980)*self.w))
        self.MENU1_widget.setFixedHeight(int((160/880)*self.h))
        #self.MENU1_widget.seftStyleSheet("QLabel{color: #f5fcff; font: %spt  'Oswald'; background-color: rgb(15,15,15); }" %(int((25/1980)*self.w)))
#-------logo plus team id combined widget ends---------
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
        self.MENU2_widget.setFixedWidth(int((350/1980)*self.w))
        self.MENU2_widget.setFixedHeight(int((60/880)*self.h))
        self.MENU2_widget.setStyleSheet("QLabel{{color: {0}; font: {1}pt 'Oswald'; background-color: {2};}}".format(color_text, int(((16/1980)/50)*size*self.w), color_background1))
#-------mission time widget ends----------------------------------------------------------------------------------------------
#-------state widget starts------------------------------------------------------------------------------------------------------
        self.state = QLabel("Current State: Ascent")
        self.state.setAlignment(QtCore.Qt.AlignCenter)
        state_layout = QVBoxLayout()
        state_layout.addWidget(self.state)
        self.state_widget = QtWidgets.QWidget()
        self.state_widget.setFixedWidth(int((350/1980)*self.w))
        self.state_widget.setFixedHeight(int((60/880)*self.h))
        self.state_widget.setStyleSheet("QLabel{{color: {0}; font: {1}pt 'Oswald'; background-color: {2};}}".format(color_text, int(((16/1980)/50)*size*self.w), color_background1))
        self.state_widget.setLayout(state_layout)
#-------state widget ends---------------------------------------------------------------------------------------------------------
#-------mode widgets starts-------------------------------------------------------------------------------------------------------
        self.mode_name = QLabel("Mode: Flight")
        mode_layout = QVBoxLayout()
        mode_layout.addWidget(self.mode_name)
        self.mode_widget = QtWidgets.QWidget()
        self.mode_widget.setFixedWidth(int((350/1980)*self.w))
        self.mode_widget.setFixedHeight(int((60/880)*self.h))
        self.mode_name.setAlignment(QtCore.Qt.AlignCenter)
        self.mode_widget.setStyleSheet("QLabel{{color: {0}; font: {1}pt 'Oswald'; background-color: {2};}}".format(color_text, int(((16/1980)/50)*size*self.w), color_background1))
        self.mode_widget.setLayout(mode_layout)
#-------mode widget ends---------\
        #-------menu 3 starts with widget of mission time, mode and state---------------------------------------------------------------------------------------
        MENU3_layout = QHBoxLayout()
        MENU3_layout.addWidget(self.mode_widget)
        MENU3_layout.addWidget(self.MENU2_widget)
        MENU3_layout.addWidget(self.state_widget)
        self.MENU3_widget = QtWidgets.QWidget()
        self.MENU3_widget.setLayout(MENU3_layout)  
        self.MENU3_widget.setFixedWidth(int((1250/1980)*self.w))
        self.MENU3_widget.setFixedHeight(int((70/880)*self.h))      
        self.MENU3_widget.setStyleSheet("QWidget{background-color: %s; }" % color_background3)
#-------menu 3 ends----------------------------
#-------longitude, latitude , no. of gps widget starts---------------------------------------------------------------------------------------------------------------
        self.longitude = QLabel("Longitude: 00.0000°E")
        self.longitude.setAlignment(QtCore.Qt.AlignCenter)

        self.gps_time = QLabel("GPS Time: 0.0")
        self.gps_time.setAlignment(QtCore.Qt.AlignCenter)
        self.latitude = QLabel("Latitude: 00.0000°N")
        self.latitude.setAlignment(QtCore.Qt.AlignCenter)
        
        self.no_of_gps = QLabel("No. of Sats: 0")
        self.no_of_gps.setAlignment(QtCore.Qt.AlignCenter)

        gps_time_layout = QHBoxLayout()
        gps_time_layout.addWidget(self.gps_time)
        
        
        self.gps_time_widget = QtWidgets.QWidget()
        self.gps_time_widget.setFixedWidth(int((170/1980)*self.w))
        self.gps_time_widget.setFixedHeight(int((50/880)*self.h))
        self.gps_time_widget.setStyleSheet("QLabel{{color: {0}; font: {1}pt 'Oswald'; background-color: {2};}}".format(color_text, int(((11/1980)/50)*size*self.w), color_background1))
        self.gps_time_widget.setLayout(gps_time_layout)
        
        

        no_of_gps_layout = QHBoxLayout()
        no_of_gps_layout.addWidget(self.no_of_gps)
        self.no_of_gps_widget = QtWidgets.QWidget()
        self.no_of_gps_widget.setFixedWidth(int((170/1980)*self.w))
        self.no_of_gps_widget.setFixedHeight(int((50/880)*self.h))
        self.no_of_gps_widget.setStyleSheet("QLabel{{color: {0}; font: {1}pt 'Oswald'; background-color: {2};}}".format(color_text, int(((11/1980)/50)*size*self.w), color_background1))
        self.no_of_gps_widget.setLayout(no_of_gps_layout)


        latitude_layout = QHBoxLayout()
        latitude_layout.addWidget(self.latitude)
        self.latitude_widget = QtWidgets.QWidget()
        self.latitude_widget.setFixedWidth(int((170/1980)*self.w))
        self.latitude_widget.setFixedHeight(int((50/880)*self.h))
        self.latitude_widget.setStyleSheet("QLabel{{color: {0}; font: {1}pt 'Oswald'; background-color: {2};}}".format(color_text, int(((11/1980)/50)*size*self.w), color_background1))
        self.latitude_widget.setLayout(latitude_layout)

        longitude_layout = QHBoxLayout()
        longitude_layout.addWidget(self.longitude)
        self.longitude_widget = QtWidgets.QWidget()
        self.longitude_widget.setFixedWidth(int((170/1980)*self.w))
        self.longitude_widget.setFixedHeight(int((50/880)*self.h))
        self.longitude_widget.setStyleSheet("QLabel{{color: {0}; font: {1}pt 'Oswald'; background-color: {2};}}".format(color_text, int(((11/1980)/50)*size*self.w), color_background1))
        self.longitude_widget.setLayout(longitude_layout)

        #-------packet count widget starts---------------------------------------------------------------------------------------------------------
        self.packet_count=QLabel("Packet Count: 0")
        self.packet_count.setText("Packet Count: 0")
        self.packet_count.setAlignment(QtCore.Qt.AlignCenter)
        packet_count_layout = QHBoxLayout()
        #packet_count_layout.setSpacing(0)
        packet_count_layout.addWidget(self.packet_count)
        self.packet_count_widget = QtWidgets.QWidget()
        self.packet_count_widget.setFixedWidth(int((170/1980)*self.w))
        self.packet_count_widget.setFixedHeight(int((50/880)*self.h))
        self.packet_count_widget.setStyleSheet("QLabel{{color: {0}; font: {1}pt 'Oswald'; background-color: {2};}}".format(color_text, int(((11/1980)/50)*size*self.w), color_background1))
        self.packet_count_widget.setLayout(packet_count_layout)
#-------packet count widget ends--------------------------------------------------------------------------------------------------------------
#-------corrupted packets widget starts--------------------------------------------------------------------------------------------------------------
        self.corrupted_packets = QLabel("Corrupted Packets: 0")
        self.corrupted_packets.setAlignment(QtCore.Qt.AlignCenter)
        corrupted_packets_layout = QHBoxLayout()
        #corrupted_packets_layout.setSpacing(0)
        corrupted_packets_layout.addWidget(self.corrupted_packets)
        self.corrupted_packets_widget = QtWidgets.QWidget()
        self.corrupted_packets_widget.setFixedWidth(int((170/1980)*self.w))
        self.corrupted_packets_widget.setFixedHeight(int((50/880)*self.h))
        self.corrupted_packets_widget.setStyleSheet("QLabel{{color: {0}; font: {1}pt 'Oswald'; background-color: {2};}}".format(color_text, int(((11/1980)/50)*size*self.w), color_background1))
        self.corrupted_packets_widget.setLayout(corrupted_packets_layout)
#-------corrupted packet widget ends------------------
#-------longitude and latitude widget------------
        #--no of gps and gps altitude widge , latitude and longitude witget t:
        lines_layout = QHBoxLayout()
        lines_layout.setContentsMargins(0, 0, 0, 0)
        lines_layout.setSpacing(0)
        lines_layout.addWidget(self.gps_time_widget)
        lines_layout.addWidget(self.no_of_gps_widget)
        lines_layout.addWidget(self.latitude_widget)
        lines_layout.addWidget(self.longitude_widget)
        lines_layout.addWidget(self.packet_count_widget)
        #lines_layout.addWidget(self.corrupted_packets_widget)
        self.lines_widget = QtWidgets.QWidget()
        self.lines_widget.setFixedWidth(int((1250/1980)*self.w))
        self.lines_widget.setFixedHeight(int((70/880)*self.h))
        self.lines_widget.setLayout(lines_layout)
        self.lines_widget.setStyleSheet("QWidget{background-color: %s; }" % color_background3)
# ----- ends --------------------------------------------
        #-------graph1 starts, code can be found in plot.py and widget.py--------------------------------------------------------------------
#-------graph pressure starts---------------------------------------------------------------------------------------------
        self.pressure_widget = namewidget()
        

        self.graphPressure1 = graph([
                {
                        "color": color_graph_line,
                        "name": "Pressure"
                }], True, 200, "", "Pressure ")
        self.graphPressure1.backgroundColor(color_graph, color_text_graph)
        graphPressure_Layout = QVBoxLayout()
        graphPressure_Layout.addWidget(self.pressure_widget.nameline("Pressure",int(((7/1980)/50)*size*self.w),int(((25/880)/50)*size*self.h),int(((13/1980)/50)*size*self.w)))
        graphPressure_Layout.addWidget(self.graphPressure1.graphWidget)
        self.graphPressure = QtWidgets.QWidget()
        self.graphPressure.setLayout(graphPressure_Layout)
        self.graphPressure.setFixedWidth(int((500/1980)*self.w))
        self.graphPressure.setFixedHeight(int((200/880)*self.h))
        self.pressure_widget.update_color_text(color_text, color_background3,int(((13/1980)/50)*size*self.w))
        self.graphPressure.setStyleSheet("QLabel{{color: {0}; font: {1}pt 'Oswald'; background-color: {2};}}".format(color_text, 10, color_background_graph))

#-------graph pressure ends---------------------------------------------------------------------------------------------------
#-------graph temperature starts----------------------------------------------------------------------------------------------
        self.temperature_widget = namewidget()
        self.graphTemperature1 = graph([
                {
                        "color": color_graph_line,
                        "name": "Temperature"
                }], True, 200, "", "Temperature ")
        self.graphTemperature1.backgroundColor(color_graph, color_text_graph)
        graphTemperature_Layout = QVBoxLayout()
        graphTemperature_Layout.addWidget(self.temperature_widget.nameline("Temperature",int(((7/1980)/50)*size*self.w),int(((25/880)/50)*size*self.h),int(((13/1980)/50)*size*self.w)))
        graphTemperature_Layout.addWidget(self.graphTemperature1.graphWidget)
        self.graphTemperature = QtWidgets.QWidget()
        self.graphTemperature.setLayout(graphTemperature_Layout)
        self.graphTemperature.setFixedWidth(int((500/1980)*self.w))
        self.graphTemperature.setFixedHeight(int((200/880)*self.h))
        self.temperature_widget.update_color_text(color_text, color_background3,int(((13/1980)/50)*size*self.w))
        self.graphTemperature.setStyleSheet("QLabel{{color: {0}; font: {1}pt 'Oswald'; background-color: {2};}}".format(color_text, 10, color_background_graph))
#-------graph temperature ends-------------------------------------------------------------------------------------------------
#-------graph altitude starts---------------------------------------------------------------------------------------------------
        self.altitude_widget = namewidget()
        self.graphAltitude1 = graph([
                {
                        "color": color_graph_line,
                        "name": "Altitude"
                }], True, 200, "", "Altitude ")
        self.graphAltitude1.backgroundColor(color_graph, color_text_graph)
        graphAltitude_Layout = QVBoxLayout()
        graphAltitude_Layout.addWidget(self.altitude_widget.nameline("Altitude",int(((7/1980)/50)*size*self.w),int(((25/880)/50)*size*self.h),int(((13/1980)/50)*size*self.w)))
        graphAltitude_Layout.addWidget(self.graphAltitude1.graphWidget)
        self.graphAltitude = QtWidgets.QWidget()
        self.graphAltitude.setLayout(graphAltitude_Layout)
        self.graphAltitude.setFixedWidth(int((500/1980)*self.w))
        self.graphAltitude.setFixedHeight(int((200/880)*self.h))
        self.altitude_widget.update_color_text(color_text, color_background3,int(((13/1980)/50)*size*self.w))
        self.graphAltitude.setStyleSheet("QLabel{{color: {0}; font: {1}pt 'Oswald'; background-color: {2};}}".format(color_text, 10, color_background_graph))
#-------graph altitude ends--------------------------------------------------------------------------------------------------------
#-------graph 1 widget making starts-------------------------------------------------------------------------------------------
        GRAPH1_layout = QGridLayout()
        GRAPH1_layout.addWidget(self.graphPressure,1,1,1,1,QtCore.Qt.AlignCenter)
        GRAPH1_layout.addWidget(self.graphTemperature,1,2,1,1,QtCore.Qt.AlignCenter)
        GRAPH1_layout.addWidget(self.graphAltitude,1,3,1,1,QtCore.Qt.AlignCenter)
        self.GRAPH1_widget = QtWidgets.QWidget()
        self.GRAPH1_widget.setLayout(GRAPH1_layout)
        self.GRAPH1_widget.setFixedWidth(int((1520/1980)*self.w))
        self.GRAPH1_widget.setFixedHeight(int((210/880)*self.h))
        self.GRAPH1_widget.setStyleSheet("background-color: %s" % color_background1)
#-------graph 1 widget making ends---------------------------------------------------------------------------------------------------
#-------graph2 widget starts, code can found on widget.py and plot.py-----------------------------------------------------------------------------------------
#-------graph voltage starts---------------------------------------------------------------------------------------------------------
        self.voltage_widget = namewidget()
        self.graphVoltage1 = graph([
                {
                        "color": color_graph_line,
                        "name": "Voltage"
                }], True, 200, "", "Voltage ")
        self.graphVoltage1.backgroundColor(color_graph, color_text_graph)
        graphVoltage_Layout = QVBoxLayout()
        graphVoltage_Layout.addWidget(self.voltage_widget.nameline("Voltage",int((7/1980)*self.w),int((25/880)*self.h),int((13/1980)*self.w)))
        graphVoltage_Layout.addWidget(self.graphVoltage1.graphWidget)
        self.graphVoltage = QtWidgets.QWidget()
        self.graphVoltage.setFixedWidth(int((500/1980)*self.w))
        self.graphVoltage.setFixedHeight(int((200/880)*self.h))
        self.voltage_widget.update_color_text(color_text, color_background3,int(((13/1980)/50)*size*self.w))
        self.graphVoltage.setLayout(graphVoltage_Layout)
        self.graphVoltage.setStyleSheet("QLabel{{color: {0}; font: {1}pt 'Oswald'; background-color: {2};}}".format(color_text, 10, color_background_graph))
#-------graph voltage ends------------------------------------------------------------------------------------------------------------
#-------graph gps altitude starts-----------------------------------------------------------------------------------------------------
        self.gps_altitude_widget1 = namewidget()
        self.graphGPS_Altitude1 = graph([
                {
                        "color": color_graph_line,
                        "name": "GPS_Altitude"
                }], True, 200, "", "GPS_Altitude")
        self.graphGPS_Altitude1.backgroundColor(color_graph, color_text_graph)
        graphGPS_Altitude_Layout = QVBoxLayout()
        graphGPS_Altitude_Layout.addWidget(self.gps_altitude_widget1.nameline("GPS Altitude",int(((7/1980)/50)*size*self.w),int(((25/880)/50)*size*self.h),int(((13/1980)/50)*size*self.w)))
        graphGPS_Altitude_Layout.addWidget(self.graphGPS_Altitude1.graphWidget)
        self.graphGPS_Altitude = QtWidgets.QWidget()
        self.graphGPS_Altitude.setFixedWidth(int((500/1980)*self.w))
        self.graphGPS_Altitude.setFixedHeight(int((200/880)*self.h))
        self.graphGPS_Altitude.setLayout(graphGPS_Altitude_Layout)
        self.gps_altitude_widget1.update_color_text(color_text, color_background3,int(((13/1980)/50)*size*self.w))
        self.graphGPS_Altitude.setStyleSheet("QLabel{{color: {0}; font: {1}pt 'Oswald'; background-color: {2};}}".format(color_text, 10, color_background_graph))
#-------graph gps altitude ends--------------------------------------------------------------------------------------------------------
#-------graph titl xy starts-----------------------------------------------------------------------------------------------------------
        self.tiltxy_widget = namewidget()
        self.graphTilt_XY1 = graph([
                {
                        "color": color_graph_line,
                        "name": "X-axis"
                },{
                "color": color_graph_line,
                        "name": "Y-axis"
        }], True, 200, "", "Tilt_XY ")
        self.graphTilt_XY1.backgroundColor(color_graph, color_text_graph)
        graphTilt_XY_Layout = QVBoxLayout()
        graphTilt_XY_Layout.addWidget(self.tiltxy_widget.nameline("Tilt XY",int(((7/1980)/50)*size*self.w),int(((25/880)/50)*size*self.h),int(((13/1980)/50)*size*self.w)))
        graphTilt_XY_Layout.addWidget(self.graphTilt_XY1.graphWidget)
        self.graphTilt_XY = QtWidgets.QWidget()
        self.graphTilt_XY.setFixedWidth(int((500/1980)*self.w))
        self.graphTilt_XY.setFixedHeight(int((200/880)*self.h))
        self.graphTilt_XY.setLayout(graphTilt_XY_Layout)
        self.tiltxy_widget.update_color_text(color_text, color_background3,int(((13/1980)/50)*size*self.w))
        self.graphTilt_XY.setStyleSheet("QLabel{{color: {0}; font: {1}pt 'Oswald'; background-color: {2};}}".format(color_text, 10, color_background_graph))
#-------graph titlt xy ends------------------------------------------------------------------------------------------------------------
#-------graph 2 widget making starts---------------------------------------------------------------------------------------------------
        GRAPH2_layout = QGridLayout()
        GRAPH2_layout.addWidget(self.graphVoltage,1,1,1,1,QtCore.Qt.AlignCenter)
        GRAPH2_layout.addWidget(self.graphGPS_Altitude,1,2,1,1,QtCore.Qt.AlignCenter)
        GRAPH2_layout.addWidget(self.graphTilt_XY,1,3,1,1,QtCore.Qt.AlignCenter)
        self.GRAPH2_widget = QtWidgets.QWidget()
        self.GRAPH2_widget.setLayout(GRAPH2_layout)
        self.GRAPH2_widget.setFixedWidth(int((1520/1980)*self.w))
        self.GRAPH2_widget.setFixedHeight(int((210/880)*self.h))
        self.GRAPH2_widget.setStyleSheet("background-color: %s" % color_background1)
#-------graph 2 widget ends-------------------------------------------------------------------------------------------------------------
#-------graph3 widget starts, code can found on widget.py and plot.py-----------------------------------------------------------------------------------------
#-------graph rot z starts---------------------------------------------------------------------------------------------------------
        self.rotation_widget = namewidget()
        self.graphRotation1 = graph([
                {
                        "color": color_graph_line,
                        "name": "RotationZ"
                }], True, 200, "", "RotationZ ")
        self.graphRotation1.backgroundColor(color_graph, color_text_graph)
        graphRotation_Layout = QVBoxLayout()
        graphRotation_Layout.addWidget(self.rotation_widget.nameline("Rotation",int((7/1980)*self.w),int((25/880)*self.h),int((13/1980)*self.w)))
        graphRotation_Layout.addWidget(self.graphRotation1.graphWidget)
        self.graphRotation = QtWidgets.QWidget()
        self.graphRotation.setFixedWidth(int((500/1980)*self.w))
        self.graphRotation.setFixedHeight(int((200/880)*self.h))
        self.rotation_widget.update_color_text(color_text, color_background3,int(((13/1980)/50)*size*self.w))
        self.graphRotation.setLayout(graphRotation_Layout)
        self.graphRotation.setStyleSheet("QLabel{{color: {0}; font: {1}pt 'Oswald'; background-color: {2};}}".format(color_text, 10, color_background_graph))
#-------graph voltage ends------------------------------------------------------------------------------------------------------------
#-------graph gps altitude starts-----------------------------------------------------------------------------------------------------
        self.speed_widget = namewidget()
        self.graphSpeed1 = graph([
                {
                        "color": color_graph_line,
                        "name": "Speed"
                }], True, 200, "", "Speed ")
        self.graphSpeed1.backgroundColor(color_graph, color_text_graph)
        graphSpeed_Layout = QVBoxLayout()
        graphSpeed_Layout.addWidget(self.speed_widget.nameline("Speed",int((7/1980)*self.w),int((25/880)*self.h),int((13/1980)*self.w)))
        graphSpeed_Layout.addWidget(self.graphSpeed1.graphWidget)
        self.graphSpeed = QtWidgets.QWidget()
        self.graphSpeed.setFixedWidth(int((500/1980)*self.w))
        self.graphSpeed.setFixedHeight(int((200/880)*self.h))
        self.speed_widget.update_color_text(color_text, color_background3,int(((13/1980)/50)*size*self.w))
        self.graphSpeed.setLayout(graphSpeed_Layout)
        self.graphSpeed.setStyleSheet("QLabel{{color: {0}; font: {1}pt 'Oswald'; background-color: {2};}}".format(color_text, 10, color_background_graph))
#-------graph gps altitude ends--------------------------------------------------------------------------------------------------------
#-------graph extra starts-----------------------------------------------------------------------------------------------------------
        self.cmd_echo = QLabel("CMD ECHO : ")
        self.battery_val = QLabel("Battery % : ")
        self.cmd_echo.setAlignment(QtCore.Qt.AlignLeft)
        self.battery_val.setAlignment(QtCore.Qt.AlignLeft)
        cmd_echo_layout = QVBoxLayout()
        #corrupted_packets_layout.setSpacing(0)
        cmd_echo_layout.addWidget(self.cmd_echo)
        cmd_echo_layout.addWidget(self.battery_val)
        self.cmd_echo_widget = QtWidgets.QWidget()
        self.cmd_echo_widget.setFixedWidth(int((170/1980)*self.w))
        self.cmd_echo_widget.setFixedHeight(int((100/880)*self.h))
        self.cmd_echo_widget.setStyleSheet("QLabel{{color: {0}; font: {1}pt 'Oswald'; background-color: {2};}}".format(color_text, int(((11/1980)/50)*size*self.w), color_background1))

        self.cmd_echo_widget.setLayout(cmd_echo_layout)
        


        self.connection = namewidget()
       
        connection_Layout = QVBoxLayout()
        connection_Layout.addWidget(self.connection.nameline("Connecting",int((7/1980)*self.w),int((25/880)*self.h),int((13/1980)*self.w)))
        connection_Layout.addWidget(self.cmd_echo_widget)
        connection_Layout.addStretch(1)
        self.connection1 = QtWidgets.QWidget()
        self.connection1.setFixedWidth(int((500/1980)*self.w))
        self.connection1.setFixedHeight(int((200/880)*self.h))
        self.connection.update_color_text(color_text, color_background3,int(((13/1980)/50)*size*self.w))
        self.connection1.setLayout(connection_Layout)
        self.connection1.setStyleSheet("QLabel{{color: {0}; font: {1}pt 'Oswald'; background-color: {2};}}".format(color_text, 10, color_background_graph))




        
       
        
        
        #self.extra.setStyleSheet("QLabel{color: #f5fcff; font: 10pt  'Oswald';background-color: rgb(3,0,13); }")
#-------graph titlt xy ends------------------------------------------------------------------------------------------------------------
#-------graph 2 widget making starts---------------------------------------------------------------------------------------------------
        GRAPH3_layout = QGridLayout()
        GRAPH3_layout.addWidget(self.graphRotation,1,1,1,1,QtCore.Qt.AlignCenter)
        GRAPH3_layout.addWidget(self.graphSpeed,1,2,1,1,QtCore.Qt.AlignCenter)
        GRAPH3_layout.addWidget(self.connection1,1,3,1,1,QtCore.Qt.AlignCenter)
        self.GRAPH3_widget = QtWidgets.QWidget()
        self.GRAPH3_widget.setFixedWidth(int((1520/1980)*self.w))
        self.GRAPH3_widget.setFixedHeight(int((210/880)*self.h))
        self.GRAPH3_widget.setLayout(GRAPH3_layout)
        self.GRAPH3_widget.setStyleSheet("background-color: %s" % color_background1)
#-------graph 2 widget ends-------------------------------------------------------------------------------------------------------------
#-------graph widget starts--------------------------------------------------------------------------------------------------------------
        graph_layout = QGridLayout()
        graph_layout.addWidget(self.GRAPH2_widget,2,1,1,1,QtCore.Qt.AlignCenter)
        graph_layout.addWidget(self.GRAPH1_widget,1,1,1,1,QtCore.Qt.AlignCenter)
        graph_layout.addWidget(self.GRAPH3_widget,3,1,1,1,QtCore.Qt.AlignCenter)
        self.graph_widget = QtWidgets.QWidget()
        self.graph_widget.setFixedWidth(int((1520/1980)*self.w))
        self.graph_widget.setFixedHeight(int((670/880)*self.h))
        self.graph_widget.setLayout(graph_layout)
#-------graph widget ends-----
        #-------gps widget starts----------------------------------------------------------------------------------------------------------------
        self.map = mapWidget()
        self.lat, self.lon = 17.5449,78.5718
        self.map.setFixedWidth(int((390/1980)*self.w))
        self.map.setFixedHeight(int((280/880)*self.h))
        self.map.setStyleSheet("color: %s" % color_background3)
#-------gps widget ends---------
# ------right side with states, gps , buttons and telemetry
        gps_label_layout = QVBoxLayout()
        self. gps_label_layout_widget = namewidget()
        gps_label_layout.addWidget(self.gps_label_layout_widget.nameline("GPS Location",int((7/1980)*self.w),int((25/880)*self.h),int((13/1980)*self.w)))
        #gps_label_layout.addWidget(self.gps_label_layout_widget.nameline("GPS Location",int(((7/1980)/50)*size*self.w),int(((30/880)/50)*size*self.h),int(((16/1980)/50)*size*self.w)),1,0,1,1)
        gps_label_layout.addWidget(self.map)
        self.gps_label_layout_widget.update_color_text(color_text, color_background3,int(((13/1980)/50)*size*self.w))
        
        self.gps_label_widget = QtWidgets.QWidget()
        self.gps_label_widget.setFixedWidth(int((400/1980)*self.w))
        self.gps_label_widget.setFixedHeight(int((350/880)*self.h))
        
        self.gps_label_widget.setLayout(gps_label_layout)


        self.gpsLabel = namewidget()
       
        gps_Layout = QVBoxLayout()
        gps_Layout.addWidget(self.gpsLabel.nameline("GPS Location",int((7/1980)*self.w),int((30/880)*self.h),int((16/1980)*self.w)))
        gps_Layout.addWidget(self.map)
        #connection_Layout.addStretch(1)
        self.gps1 = QtWidgets.QWidget()
        self.gps1.setFixedWidth(int((400/1980)*self.w))
        self.gps1.setFixedHeight(int((350/880)*self.h))
        self.gpsLabel.update_color_text(color_text, color_background3,int(((16/1980)/50)*size*self.w))
        self.gps1.setLayout(gps_Layout)
        self.gps1.setStyleSheet("QLabel{{color: {0}; font: {1}pt 'Oswald'; background-color: {2};}}".format(color_text, 10, color_background_graph))

# ----------------------- gps ends ---------------------------------------
        #-------button widget starts, code for which is in widget.py file------------------------------------------------------------------------------
        button_layout=QVBoxLayout()
        button_layout1=QGridLayout()
        button_layout2=QGridLayout()
        button_layout3=QGridLayout()
        button_layout4=QGridLayout()
        self.tel = buttonfunc("Telemetry",int((11/1980)*self.w))
        #print(self.tel.clicked.connect())
        button_layout1.addWidget(self.tel,1,1,1,1)   
        button_layout1.addWidget(buttonfunc("Calibration",int((11/1980)*self.w)),1,2,1,1)
        button_layout1.addWidget(buttonfunc("Set Time UTC",int((11/1980)*self.w)),1,3,1,1)
        button_layout3.addWidget(buttonfunc("Set Time GPS",int((11/1980)*self.w)),1,1,1,1)
        button_layout2.addWidget(buttonfunc("Simulation-Enable",int((11/1980)*self.w)),1,1,1,1)
        button_layout2.addWidget(buttonfunc("Simulation-Activate",int((11/1980)*self.w)),1,2,1,1)
        button_layout3.addWidget(buttonfunc("Audio-Beacon",int((11/1980)*self.w)),1,2,1,1)
        button_layout4.addWidget(buttonfunc("Deploy-Nosecone",int((11/1980)*self.w)),1,1,1,1)
        button_layout4.addWidget(buttonfunc("Deploy-Parachute",int((11/1980)*self.w)),1,2,1,1)
        button_layout3.addWidget(buttonfunc("Reset",int((11/1980)*self.w)),1,3,1,1)
        self.button_widget1 = QtWidgets.QWidget()
        self.button_widget1.setLayout(button_layout1)
        self.button_widget2 = QtWidgets.QWidget()
        self.button_widget2.setLayout(button_layout2)
        self.button_widget3 = QtWidgets.QWidget()
        self.button_widget3.setLayout(button_layout3)
        self.button_widget4 = QtWidgets.QWidget()
        self.button_widget4.setLayout(button_layout4)
        
        button_layout.addWidget(self.button_widget1)
        button_layout.addWidget(self.button_widget2)
        button_layout.addWidget(self.button_widget3)
        button_layout.addWidget(self.button_widget4)
        
        self.button_widget = QtWidgets.QWidget()
        self.button_widget.setLayout(button_layout)
        self.button_widget.setFixedWidth(int((400/1980)*self.w))
        self.button_widget.setFixedHeight(int((250/880)*self.h))
        self.button_widget.setStyleSheet("QWidget{background-color: %s; }" % color_background3)
#-------button widget ends-----------
        #-------states 1 widget starts, code in widget.py file-------------------------------------------------------------------------------
        states1_layout=QHBoxLayout()
        states1_layout.setSpacing(0)
        self.asc=dotAndState("Launch Wait",int((50/880)*self.h),int(((12/1980)/50)*size*self.w))
        states1_layout.addWidget(self.asc)
        states1_layout.addWidget(dotAndState("Descent", int((50/880)*self.h),int(((12/1980)/50)*size*self.w)))
        self.states1_widget = QtWidgets.QWidget()
        self.states1_widget.setFixedWidth(int((400/1980)*self.w))
        self.states1_widget.setFixedHeight(int((60/880)*self.h))
        self.states1_widget.setLayout(states1_layout)
        self.states1_widget.setStyleSheet("QWidget{background-color: %s; }" % color_background1)
#-------state 1 widget ends-------------------------------------------------------------------------------------------------------------
#-------state 2 widget starts------------------------------------------------------------------------------------------------------------------
        states2_layout=QHBoxLayout()
        states2_layout.setSpacing(0)
        states2_layout.addWidget(dotAndState("Ascent", int((50/880)*self.h),int(((12/1980)/50)*size*self.w)))
        states2_layout.addWidget(dotAndState("HS Released", int((50/880)*self.h),int(((12/1980)/50)*size*self.w)))

        self.states2_widget = QtWidgets.QWidget()
        self.states2_widget.setFixedWidth(int((400/1980)*self.w))
        self.states2_widget.setFixedHeight(int((60/880)*self.h))
        self.states2_widget.setLayout(states2_layout)
        self.states2_widget.setStyleSheet("QWidget{background-color: %s; }" % color_background1)
#-------state 2 widget ends-----------------------------------------------------------------------------------------------------------------------
#-------state 3 widget starts--------------------------------------------------------------------------------------------------------------
        states3_layout=QHBoxLayout()
        states3_layout.setSpacing(0)
        states3_layout.addWidget(dotAndState("Rocket Separation", int((50/880)*self.h),int(((12/1980)/50)*size*self.w)))
        states3_layout.addWidget(dotAndState("Landed", int((50/880)*self.h),int(((12/1980)/50)*size*self.w)))

        self.states3_widget = QtWidgets.QWidget()
        self.states3_widget.setFixedWidth(int((400/1980)*self.w))
        self.states3_widget.setFixedHeight(int((60/880)*self.h))
        self.states3_widget.setLayout(states3_layout)
        self.states3_widget.setStyleSheet("QWidget{background-color: %s; }" % color_background1)
#-------state 3 widget ends----------------------------------------------------------------------------------------------------------------------------

#-------statesfull starts --------------------------------------------------------------------------------------------------------------------
        statesfull_layout=QVBoxLayout()
        statesfull_layout.setSpacing(0)
        statesfull_layout.addWidget(self.states1_widget)
        statesfull_layout.addWidget(self.states2_widget)
        statesfull_layout.addWidget(self.states3_widget)
        
        self.statesfull_widget = QtWidgets.QWidget()
        self.statesfull_widget.setLayout(statesfull_layout)
        self.statesfull_widget.setFixedWidth(int((400/1980)*self.w))
        self.statesfull_widget.setFixedHeight(int((180/880)*self.h))
        self.statesfull_widget.setStyleSheet("QWidget{background-color: %s; }" % color_background1)
#-------statesfull ends -------

        #-------cmd textbox starts---------------------------------------------------------------------------------------------------------------
        self.tele_cmd_textbox =  QLineEdit()
        self.tele_cmd_textbox.setStyleSheet("background-color: %s ;border: 0px ;color: #149414;font-family: 'Oswald'" % color_background3)
        #self.tele_cmd_textbox.setFixedWidth(300)
        self.tele_cmd_textbox.returnPressed.connect(self.OnReturnPressed)
#-------cmd textbox ends-------------------------------------------------------------------------------------------------------------------
#------send button widget starts---------------------------------------------------------------------------------------------------------------
        self.send = QtWidgets.QPushButton()
        self.send.setText("SEND")
        self.send.setStyleSheet("QPushButton{{color: {0}; font: {1}pt 'Oswald'; background-color: {2};}}".format(color_text, int(((8/1980)/50)*size*self.w), color_background3))

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
        self.cmdOutput.setStyleSheet("background-color: %s ;border: 0px ;color: #149414;font-family: 'Oswald'" % color_background1)
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
        self.cmd_widget.setFixedWidth(int((400/1980)*self.w))
        self.cmd_widget.setFixedHeight(int((100/880)*self.h))
        self.cmd_widget.setStyleSheet("background-color: %s" % color_background1)
        self.cmd_widget.setLayout(cmd_layout)
#-------cmd textbox plus output box widget ends-----



        combo_layout4 = QVBoxLayout()
        #sizegrip = QtWidgets.QSizeGrip(MainWindow)
        #all_layout.addWidget(sizegrip, 0, QtCore.Qt.AlignBottom  QtCore.Qt.AlignRight)
        
        combo_layout4.addWidget(self.gps1)
        combo_layout4.addWidget(self.button_widget)
        combo_layout4.addWidget(self.statesfull_widget)
        
        combo_layout4.addWidget(self.cmd_widget)
        self.combo_widget4 = QtWidgets.QWidget()
        self.combo_widget4.setLayout(combo_layout4)
        self.combo_widget4.setStyleSheet("background-color: %s" % color_background2)
#---right side ends ---------------------------------------
        combo_layout1 = QVBoxLayout()
        #sizegrip = QtWidgets.QSizeGrip(MainWindow)
        #all_layout.addWidget(sizegrip, 0, QtCore.Qt.AlignBottom  QtCore.Qt.AlignRight)
        
        combo_layout1.addWidget(self.MENU3_widget)
        combo_layout1.addWidget(self.lines_widget)
        self.combo_widget1 = QtWidgets.QWidget()
        self.combo_widget1.setLayout(combo_layout1)
        self.combo_widget1.setFixedWidth(int((1280/1980)*self.w))
        self.combo_widget1.setFixedHeight(int((140/880)*self.h))
        self.combo_widget1.setStyleSheet("background-color: %s" % color_background2)
        #self.setFixedSize(self.all_widget.sizeHint())


        combo_layout2 = QHBoxLayout()
        #sizegrip = QtWidgets.QSizeGrip(MainWindow)
        #all_layout.addWidget(sizegrip, 0, QtCore.Qt.AlignBottom  QtCore.Qt.AlignRight)
        
        combo_layout2.addWidget(self.MENU1_widget)
        combo_layout2.addWidget(self.combo_widget1)
        self.combo_widget2 = QtWidgets.QWidget()
        self.combo_widget2.setLayout(combo_layout2)
        self.combo_widget2.setStyleSheet("background-color: %s" % color_background2)
        #self.setFixedSize(self.all_widget.sizeHint())

        combo_layout3 = QVBoxLayout()
        #sizegrip = QtWidgets.QSizeGrip(MainWindow)
        #all_layout.addWidget(sizegrip, 0, QtCore.Qt.AlignBottom  QtCore.Qt.AlignRight)
        
        combo_layout3.addWidget(self.combo_widget2)
        combo_layout3.addWidget(self.graph_widget)
        self.combo_widget3 = QtWidgets.QWidget()
        self.combo_widget3.setLayout(combo_layout3)
        self.combo_widget3.setStyleSheet("background-color: %s" % color_background2)
        #self.setFixedSize(self.all_widget.sizeHint())
        

        all_layout = QHBoxLayout()
        #sizegrip = QtWidgets.QSizeGrip(MainWindow)
        #all_layout.addWidget(sizegrip, 0, QtCore.Qt.AlignBottom  QtCore.Qt.AlignRight)
        all_layout.addWidget(self.combo_widget3)
        all_layout.addWidget(self.combo_widget4)
        
        
        self.all_widget = QtWidgets.QWidget()
        self.all_widget.setLayout(all_layout)
        self.all_widget.setStyleSheet("background-color: %s" % color_background2)
        #self.setFixedSize(self.all_widget.sizeHint())
        
        self.setCentralWidget(self.all_widget)
        
        self.send_thread = SendDataThread()
        self.receive_thread = ReceiveDataThread()
        self.receiving_timer = QTimer()
        self.receiving_timer.timeout.connect(self.receiver)
        self.receiving_timer.start(990)
        
        self.corruptedPacketsValue = 0
        self.i = 0
        
       
    
    def receiver(self):
                global packet
                self.receive_thread.start() 
                try:
                       previous_state_packet = self.packetCountValue
                except:
                       pass
                
                try:
                        if (packet is not None ) and (packet!="") and ("error" not in packet):
                                self.connection.update_color("green")
                                self.connection.update_name("Connected")
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
                               self.connection.update_color("red")
                except :
                       #self.onGettingData("Packet not received")
                       pass
                
                if (previous_state_packet == self.packetCountValue):
                        self.connection.update_color("red")
                        self.connection.update_name("Disconnected")

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
            self.button_name1.setStyleSheet("QPushButton{{color: {0}; font: {1}pt 'Oswald'; background-color: {2};}}".format(color_text, int((12/1980)*width), color_background_activate))

            check = "OFF"
        else:
            self.button_name1.setStyleSheet("QPushButton{{color: {0}; font: {1}pt 'Oswald'; background-color: {2};}}".format(color_text, int((12/1980)*width), color_background1))

            check = "ON"
        DATA_TO_SEND = "CMD,2027,CX," + str(check) + "\n"
        self.sending(DATA_TO_SEND)
        #print(DATA_TO_SEND,"HI")
    def audio_beacon_button(self):
        if self.button_name7.isChecked():
                self.button_name7.setStyleSheet("QPushButton{{color: {0}; font: {1}pt 'Oswald'; background-color: {2};}}".format(color_text, int((12/1980)*width), color_background_activate))
                check = "ON"
        else:
                self.button_name7.setStyleSheet("QPushButton{{color: {0}; font: {1}pt 'Oswald'; background-color: {2};}}".format(color_text, int((12/1980)*width), color_background1))
                check = "OFF"
        DATA_TO_SEND = "CMD,2027,BCN," + str(check) + "\n"
        self.sending(DATA_TO_SEND)

    def deploy_nose_button(self):
        if self.button_name8.isChecked():
                self.button_name8.setText("Lock Nosecone")
                self.button_name8.setStyleSheet("QPushButton{{color: {0}; font: {1}pt 'Oswald'; background-color: {2};}}".format(color_text, int((12/1980)*width), color_background_activate))
                check = "DEPLOY_NOSE"
        else:
                self.button_name8.setText("Deploy Nosecone")
                self.button_name8.setStyleSheet("QPushButton{{color: {0}; font: {1}pt 'Oswald'; background-color: {2};}}".format(color_text, int((12/1980)*width), color_background1))
                check = "LOCK_NOSE"
        DATA_TO_SEND = "CMD,2027," + str(check) + "\n"
        self.sending(DATA_TO_SEND)
        #print(DATA_TO_SEND,"HI")
    def deploy_para_button(self):
        if self.button_name9.isChecked():
                self.button_name9.setText("Lock Parachute")
                self.button_name9.setStyleSheet("QPushButton{{color: {0}; font: {1}pt 'Oswald'; background-color: {2};}}".format(color_text, int((12/1980)*width), color_background_activate))
                check = "DEPLOY_PARA"
        else:
                self.button_name9.setText("Deploy Parachute")
                self.button_name9.setStyleSheet("QPushButton{{color: {0}; font: {1}pt 'Oswald'; background-color: {2};}}".format(color_text, int((12/1980)*width), color_background1))
                check = "LOCK_PARA"
        DATA_TO_SEND = "CMD,2027," + str(check) + "\n"
        self.sending(DATA_TO_SEND)
        #print(DATA_TO_SEND,"HI")
    def show_reset_confirmation(self):
        if self.button_name10.isChecked():
                reply = QtWidgets.QMessageBox.question(self, 'Confirm Reset', 'Are you sure you want to reset?', 
                                                        QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, 
                                                        QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
                self.reset_button()
        else:
                self.button_name10.setChecked(False)
        
    def reset_button(self):
        if self.button_name10.isChecked():
                self.button_name10.setStyleSheet("QPushButton{{color: {0}; font: {1}pt 'Oswald'; background-color: {2};}}".format(color_text, int((12/1980)*width), color_background_activate))
                res = "CMD,2027,RESET\n"
                self.sending(res)
                self.corrupted_packets.setText("Corrupted Packets: 0")
                self.corruptedPacketsValue = 0
        else:
                self.button_name10.setStyleSheet("QPushButton{{color: {0}; font: {1}pt 'Oswald'; background-color: {2};}}".format(color_text, int((12/1980)*width), color_background1))
        
    def calibration_button(self):
        if self.button_name2.isChecked():
                self.button_name2.setStyleSheet("QPushButton{{color: {0}; font: {1}pt 'Oswald'; background-color: {2};}}".format(color_text, int((12/1980)*width), color_background_activate))
                cal = "CMD,2027,CAL\n"
                self.sending(cal)
        else:
                self.button_name2.setStyleSheet("QPushButton{{color: {0}; font: {1}pt 'Oswald'; background-color: {2};}}".format(color_text, int((12/1980)*width), color_background1))

    def set_time_utc_button(self):
        if self.button_name3.isChecked():
                self.button_name3.setStyleSheet("QPushButton{{color: {0}; font: {1}pt 'Oswald'; background-color: {2};}}".format(color_text, int((12/1980)*width), color_background_activate))
                now_utc = datetime.now(timezone.utc)
                time_utc = now_utc.time()
                b = time_utc.strftime('%H:%M:%S')
                utc = "CMD,2027,ST," + b + "\n"
                self.sending(utc)
        else:        
                self.button_name3.setStyleSheet("QPushButton{{color: {0}; font: {1}pt 'Oswald'; background-color: {2};}}".format(color_text, int((12/1980)*width), color_background1))  

    def set_time_gps_button(self):
        if self.button_name4.isChecked():
                self.button_name4.setStyleSheet("QPushButton{{color: {0}; font: {1}pt 'Oswald'; background-color: {2};}}".format(color_text, int((12/1980)*width), color_background_activate))
                gps = "CMD,2027,ST,GPS" + "\n"
                self.sending(gps)
        else:
                self.button_name4.setStyleSheet("QPushButton{{color: {0}; font: {1}pt 'Oswald'; background-color: {2};}}".format(color_text, int((12/1980)*width), color_background1))

    def simulation_enabled_button(self):
        global check_sim, sim
        if self.button_name5.isChecked():
                self.button_name5.setText("Simulation-Disable")
                self.button_name5.setStyleSheet("QPushButton{{color: {0}; font: {1}pt 'Oswald'; background-color: {2};}}".format(color_text, int((12/1980)*width), color_background_activate))
                check_sim = 1
                val = "ENABLE"
                self.button_name6.setStyleSheet("QPushButton{{color: {0}; font: {1}pt 'Oswald'; background-color: {2};}}".format(color_text, int((12/1980)*width), color_background1))
        else:
                self.button_name5.setText("Simulation-Enable")
                self.button_name5.setStyleSheet("QPushButton{{color: {0}; font: {1}pt 'Oswald'; background-color: {2};}}".format(color_text, int((12/1980)*width), color_background1))
                val = "DISABLE"
                check_sim = 0
                self.button_name6.setText("Simulation-Activate")
                self.button_name6.setStyleSheet("QPushButton{{color: {0}; font: {1}pt 'Oswald'; background-color: {2};}}".format(color_text_activate,int((12/1980)*width, color_background3)))
        sim = "CMD,2027,SIM," + val + "\n"
        self.sending(sim)


    def simulation_activate_button(self):
        global sima, simp
        if check_sim == 1:
                if self.button_name6.isChecked():
                        self.button_name6.setStyleSheet("QPushButton{{color: {0}; font: {1}pt 'Oswald'; background-color: {2};}}".format(color_text, int((12/1980)*width), color_background3))
                        self.button_name6.setText("Simulation-Deactivate")
                        val = "ACTIVATE"
                        self.sending_timer_simp = QTimer()
                        self.sending_timer_simp.timeout.connect(self.send_sim_data)
                        self.sending_timer_simp.start(1000)
                else:
                        self.sending_timer_simp.stop()
                        self.button_name6.setText("Simulation-Activate")
                        self.button_name6.setStyleSheet("QPushButton{{color: {0}; font: {1}pt 'Oswald'; background-color: {2};}}".format(color_text, int((12/1980)*width), color_background_btn))
                        val = "DISABLE"

        if check_sim == 0:
                if self.button_name6.isChecked():
                        self.button_name6.setStyleSheet("QPushButton{{color: {0}; font: {1}pt 'Oswald'; background-color: {2};}}".format(color_text_activate, int((12/1980)*width,color_background_activate )))
                        self.button_name6.setText("Simulation-Deactivate")
                else:
                        self.button_name6.setText("Simulation-Activate")
                        self.button_name6.setStyleSheet("QPushButton{{color: {0}; font: {1}pt 'Oswald'; background-color: {2};}}".format(color_text_activate, int((12/1980)*width,color_background_activate )))


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
                
                packet = ""
               

        print(self.lis)
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
                self.altitudeValue = self.lis[5]
                if('-' in self.altitudeValue):
                       parts = self.altitudeValue.split('-')
                       parts[0] = parts[0].lstrip('0')
                       result = '-'.join(parts)
                else:
                # If there is no minus sign, simply remove leading zeros
                        result = self.altitudeValue.lstrip('0')
                self.altitudeValue = float(result)
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
                self.tiltXValue = self.lis[17]
                if('-' in self.tiltXValue):
                       parts = self.tiltXValue.split('-')
                       parts[0] = parts[0].lstrip('0')
                       result = '-'.join(parts)
                else:
                # If there is no minus sign, simply remove leading zeros
                        result = self.tiltXValue.lstrip('0')
                self.tiltXValue = float(result)
        except:
                self.tiltXValue = 0.0


        try:
                self.tiltYValue = self.lis[18]
                if('-' in self.tiltYValue):
                       parts = self.tiltYValue.split('-')
                       parts[0] = parts[0].lstrip('0')
                       result = '-'.join(parts)
                else:
                # If there is no minus sign, simply remove leading zeros
                        result = self.tiltYValue.lstrip('0')
                self.tiltYValue = float(result)
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
                self.batteryValue = int(self.lis[21])
        except:
                self.batteryValue = 0
        
       
        try:
                if self.modeValue == "S":
                        pass
        
        except:
                pass

        try:
                self.packet_count.setText("Packet Count: " + str(self.packetCountValue))
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
                
                if ("*" not in  self.lis[6]) :
                        self.speed_widget.update_color("rgb(59, 146, 184)")
                else:
                        self.speed_widget.update_color("red")
        except:
                pass
        try:
                
                if ("*" not in  self.lis[19]) :
                        self.rotation_widget.update_color("rgb(59, 146, 184)")
                else:
                        self.rotation_widget.update_color("red")
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
                if ("*" not in  self.lis[12]) and ("*" not in  self.lis[13]) and ("*" not in  self.lis[14]) and ("*" not in  self.lis[16]) :
                        self.gps_label_layout_widget.update_color("rgb(59, 146, 184)")
                else:
                        self.gps_label_layout_widget.update_color("red")

        except:
                pass

        try:
               self.tiltxy_widget.update_name("Tilt XY : " + "X : " + str(self.tiltXValue) + "°" + ", Y : " + str(self.tiltYValue) + "°")

        except:
               pass

        try:
               self.gps_altitude_widget1.update_name("GPS Altitude : " +  str(self.gpsAltitudeValue) + " meters")
        except:
               pass

        try:
               self.voltage_widget.update_name("Voltage : " + str(self.voltageValue) + " volts")
        except:
               pass

        try:
               self.altitude_widget.update_name("Altitude : " +  str(self.altitudeValue) + " meters")
        except:
               pass

        try:
               self.temperature_widget.update_name("Temperature : " + str(self.temperatureValue) + " °C")
        except:
               pass

        try:
               self.pressure_widget.update_name("Pressure : " + str(self.pressureValue) + " kPa")
        except:
               pass
        try:
               self.speed_widget.update_name("Speed : " + str(self.airSpeedValue) + " m/s")
        except:
               pass
        try:
               self.rotation_widget.update_name("Rotation Z : " + str(self.rotZValue) + "°")
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
                self.graphRotation1.update(self.i,[ self.rotZValue])
        except:
                pass
        try:
                self.graphSpeed1.update(self.i,[ self.airSpeedValue])
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
                self.mis.setText("Mission Time:" + str(self.missionTimeValue))
        except:
                pass
        
        try:
                self.no_of_gps.setText("No. of Sats: " + str(self.noOfGpsValue))
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
        try:
                self.cmd_echo.setText("CMD ECHO : "+str(self.cmdEchoValue))
        except:
                pass
        try:
                self.battery_val.setText("Battery % : "+str(self.batteryValue))
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
                is_rocket_separated = 1

        
        if (self.hsDeployedValue == "P"):
                is_heat_shield_deployed = 1
                is_ascent =  1
                is_launch_wait =  1
                is_descent = 1
                is_rocket_separated = 1
        if (self.pcDeployedValue == "C"):
                is_parachute_deployed = 1
                is_heat_shield_deployed = 1
                is_ascent =  1
                is_launch_wait =  1
                is_descent = 1
                is_rocket_separated = 1
        
        
        if (self.stateValue == "LANDED"):
                is_landed = 1
                is_parachute_deployed = 1
                is_heat_shield_deployed = 1
                is_ascent =  1
                is_launch_wait =  1
                is_descent = 1
                is_rocket_separated = 1
        if (self.stateValue == "ROCKET_SEPARATION"):
                
                is_rocket_separated = 1
                
                is_ascent =  1
                is_launch_wait =  1
                

        

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
                
        self.MENU2_mission_time.setText("GMT TIME:"+str(tim))

    
   

    
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
        
