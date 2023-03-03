from QSwitchControl import SwitchControl
from PyQt5 import *
from PyQt5 import QtWidgets
from PyQt5 import QtCore
import sys
import os
from random import randint
from plot import graph
from map_plot import mapWidget
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from widget import states
from widget import namewidget
from widget import button

class MainWindow(QtWidgets.QMainWindow):
    i = 0
    counter=0
    def OnReturnPressed(self):
        """ the text is retrieved from tele_cmd_textbox """
        text = self.tele_cmd_textbox.text()
        # do some thing withit
        self.cmdoutput(text+"\n")

    def update(self):
        self.i += 1
        if self.counter==0:
            self.x=15
            self.y=15
            self.counter+=1
        elif self.counter==1:
            self.x=1
            self.y=1
            self.counter+=1
        else:
            self.x=randint(5,8)
            self.y=randint(5,8)
        self.graphPressure1.update(self.i,[ self.x])
        self.graphTemperature1.update(self.i,[ self.x])
        self.graphAltitude1.update(self.i,[ self.x])
        self.graphVoltage1.update(self.i,[ self.x])
        self.graphGPS_Altitude1.update(self.i,[ self.x])
        self.graphTilt_XY1.update(self.i,[ self.x,self.y])

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
    def __init__(self, *args, **kwargs):


        super(MainWindow, self).__init__(*args, **kwargs)
        self.window_width, self.window_height=1200,1000
        self.setMinimumSize(self.window_width, self.window_height)
        self.setStyleSheet('''
            QWidget {
                font-size:15px;
            }
        ''')
##------logowidget start---------------------------------------------------------------
        self.logo = QLabel()
        logo_image = QPixmap('./Janus Logo.png')
        logo_image = logo_image.scaled(270, 270, QtCore.Qt.KeepAspectRatio)
        self.logo.setPixmap(logo_image)
        logo_layout = QVBoxLayout()
        logo_layout.addWidget(self.logo, stretch=1)
        self.logo_widget = QtWidgets.QWidget()
        self.logo_widget.setLayout(logo_layout)
#-------logowidget ends----------------------------------------------------------------
#-------team id widget starts---------------------------------------------------------------------
        self.team_label = QLabel('TEAM ID:1062')
        team_layout = QVBoxLayout()
        team_layout.addWidget(self.logo, stretch=1)
        team_layout.addWidget(self.team_label)
        self.team_widget = QtWidgets.QWidget()
        self.team_widget.setLayout(team_layout)
#-------team id widget ends-----------------------------------------------------------------------
#-------logo plus team id combined widget starts----------------------------------------------------
        MENU1_layout = QGridLayout()
        MENU1_layout.addWidget(self.logo_widget,0,0,1,1)
        MENU1_layout.addWidget(self.team_widget,0,0,1,1)
        self.MENU1_widget = QtWidgets.QWidget()
        self.MENU1_widget.setLayout(MENU1_layout)
        self.MENU1_widget.setStyleSheet("QLabel{color: #f5fcff; font: 25pt  'Oswald'; background-color: rgb(15,15,15); }")
#-------logo plus team id combined widget ends---------------------------------------------------------------------------
#-------mission time widget starts---------------------------------------------------------------------------------------       
        self.MENU2_mission_time = QLabel('Mission Time: 08:17:40.11')
        self.MENU2_mission_time.setAlignment(QtCore.Qt.AlignCenter)
        MENU2_layout = QGridLayout()
        MENU2_layout.addWidget(self.MENU2_mission_time,1,1,1,1)
        self.MENU2_widget = QtWidgets.QWidget()
        self.MENU2_widget.setLayout(MENU2_layout)
        self.MENU2_widget.setStyleSheet("QLabel{color: #f5fcff; font: 16pt  'Oswald';background-color: rgb(30,30,30); } ")
#-------mission time widget ends----------------------------------------------------------------------------------------------
#-------state widget starts------------------------------------------------------------------------------------------------------
        self.state = QLabel("Current State: Ascent")
        state_layout = QGridLayout()
        self.state.setAlignment(QtCore.Qt.AlignCenter)
        state_layout.addWidget(self.state,1,1,1,1)
        self.state_widget = QtWidgets.QWidget()
        self.state_widget.setStyleSheet("QLabel{color: #f5fcff; font: 16pt  'Oswald';background-color: rgb(30,30,30); }")
        self.state_widget.setLayout(state_layout)
#-------state widget ends---------------------------------------------------------------------------------------------------------
#-------mode widgets starts-------------------------------------------------------------------------------------------------------
        self.mode = QLabel("Mode: Flight")
        mode_layout = QGridLayout()
        mode_layout.addWidget(self.mode,1,1,1,1)
        self.mode_widget = QtWidgets.QWidget()
        self.mode.setAlignment(QtCore.Qt.AlignCenter)
        self.mode_widget.setStyleSheet("QLabel{color: #f5fcff; font: 16pt  'Oswald';background-color: rgb(30,30,30); }")
        self.mode_widget.setLayout(mode_layout)
#-------mode widget ends------------------------------------------------------------------------------------------------------------
#-------states 1 widget starts, code in widget.py file-------------------------------------------------------------------------------
        states1_layout=QGridLayout()
        states1_layout.addWidget(states().dotAndState("Ascent", "green"),1,1,1,6)
        states1_layout.addWidget(states().dotAndState("Heat Shield Deployed", "red"),1,7,1,6)
        states1_layout.addWidget(states().dotAndState("Probe Deployed", "red"),1,13,1,6)
        states1_layout.addWidget(states().dotAndState("Landed", "red"),1,19,1,6)
        states1_layout.addWidget(states().dotAndState("Descent", "red"),2,1,1,6)
        states1_layout.addWidget(states().dotAndState("Rocket Separation", "red"),2,7,1,6)
        states1_layout.addWidget(states().dotAndState("Parachute Deployed", "red"),2,13,1,6)
        states1_layout.addWidget(states().dotAndState("Mast Raised", "red"),2,19,1,6)

        self.states1_widget = QtWidgets.QWidget()
        self.states1_widget.setLayout(states1_layout)
        self.states1_widget.setStyleSheet("QWidget{background-color: rgb(30,30,30); }")
#-------state 1 widget ends-------------------------------------------------------------------------------------------------------------
#-------menu 3 starts with widget of mission time, mode and state---------------------------------------------------------------------------------------
        MENU3_layout = QGridLayout()
        MENU3_layout.addWidget(self.mode_widget,1,1,1,1)
        MENU3_layout.addWidget(self.MENU2_widget,1,2,1,1)
        MENU3_layout.addWidget(self.state_widget,1,3,1,1)
        self.MENU3_widget = QtWidgets.QWidget()
        self.MENU3_widget.setLayout(MENU3_layout)        
        self.MENU3_widget.setStyleSheet("QWidget{background-color: rgb(20,20,20); }")
#-------menu 3 ends------------------------------------------------------------------------------------------------------------------------
#-------menu 4 starts with widgets of menu3, states1 and states2----------------------------------------------------------------------------
        MENU4_layout = QGridLayout()
        MENU4_layout.addWidget(self.MENU3_widget,1,1,1,10)
        MENU4_layout.addWidget(self.states1_widget,2,2,1,8)
        self.MENU4_widget = QtWidgets.QWidget()
        self.MENU4_widget.setLayout(MENU4_layout)
#-------menu 4 ends---------------------------------------------------------------------------------------------------------------------------------
#-------menu 5 starts with widget of team id and logo along with menu 4------------------------------------------------------------------------------
        MENU5_layout = QGridLayout()
        MENU5_layout.addWidget(self.MENU1_widget,1,1,1,1)
        MENU5_layout.addWidget(self.MENU4_widget,1,2,1,1)
        self.MENU5_widget = QtWidgets.QWidget()
        self.MENU5_widget.setLayout(MENU5_layout)
#-------menu 5 ends----------------------------------------------------------------------------------------------------------------------------
#-------button widget starts, code for which is in widget.py file------------------------------------------------------------------------------
        button_layout=QGridLayout()
        button_layout.addWidget(button().buttonfunc("Telemetry"),1,1,1,1)
        button_layout.addWidget(button().buttonfunc("Calibration"),1,2,1,1)
        button_layout.addWidget(button().buttonfunc("Set Time UTC"),1,3,1,1)
        button_layout.addWidget(button().buttonfunc("Set Time GPS"),1,4,1,1)
        button_layout.addWidget(button().buttonfunc("Simulation-Enable"),1,5,1,1)
        button_layout.addWidget(button().buttonfunc("Simulation-Activate"),1,6,1,1)
        self.button_widget = QtWidgets.QWidget()
        self.button_widget.setLayout(button_layout)
        self.button_widget.setStyleSheet("QWidget{background-color: rgb(20,20,20); }")
#-------button widget ends---------------------------------------------------------------------------------------------------------------
#-------graph1 starts, code can be found in plot.py and widget.py--------------------------------------------------------------------
#-------graph pressure starts---------------------------------------------------------------------------------------------
        self.graphPressure1 = graph([
        	{
        		"color": (245,252,255),
        		"name": "Pressure"
        	}], True, 200, "", "Pressure ")
        graphPressure_Layout = QVBoxLayout()
        graphPressure_Layout.addWidget(namewidget().nameline("Pressure"))
        graphPressure_Layout.addWidget(self.graphPressure1.graphWidget)
        self.graphPressure = QtWidgets.QWidget()
        self.graphPressure.setLayout(graphPressure_Layout)
        self.graphPressure.setStyleSheet("QLabel{color: #f5fcff; font: 10pt  'Oswald';background-color: rgb(3,0,13); }")
#-------graph pressure ends---------------------------------------------------------------------------------------------------
#-------graph temperature starts----------------------------------------------------------------------------------------------
        self.graphTemperature1 = graph([
        	{
        		"color": (245,252,255),
        		"name": "Temperature"
        	}], True, 200, "", "Temperature ")
        graphTemperature_Layout = QVBoxLayout()
        graphTemperature_Layout.addWidget(namewidget().nameline("Temperature"))
        graphTemperature_Layout.addWidget(self.graphTemperature1.graphWidget)
        self.graphTemperature = QtWidgets.QWidget()
        self.graphTemperature.setLayout(graphTemperature_Layout)
        self.graphTemperature.setStyleSheet("QLabel{color: #f5fcff; font: 10pt  'Oswald';background-color: rgb(3,0,13); }")
#-------graph temperature ends-------------------------------------------------------------------------------------------------
#-------graph altitude starts---------------------------------------------------------------------------------------------------
        self.graphAltitude1 = graph([
        	{
        		"color": (245,252,255),
        		"name": "Altitude"
        	}], True, 200, "", "Altitude ")
        graphAltitude_Layout = QVBoxLayout()
        graphAltitude_Layout.addWidget(namewidget().nameline("Altitude"))
        graphAltitude_Layout.addWidget(self.graphAltitude1.graphWidget)
        self.graphAltitude = QtWidgets.QWidget()
        self.graphAltitude.setLayout(graphAltitude_Layout)
        self.graphAltitude.setStyleSheet("QLabel{color: #f5fcff; font: 12pt  'Oswald';background-color: rgb(3,0,13); }")
#-------graph altitude ends--------------------------------------------------------------------------------------------------------
#-------graph 1 widget making starts-------------------------------------------------------------------------------------------
        GRAPH1_layout = QGridLayout()
        GRAPH1_layout.addWidget(self.graphPressure,1,1,1,1)
        GRAPH1_layout.addWidget(self.graphTemperature,1,2,1,1)
        GRAPH1_layout.addWidget(self.graphAltitude,1,3,1,1)
        self.GRAPH1_widget = QtWidgets.QWidget()
        self.GRAPH1_widget.setLayout(GRAPH1_layout)
        self.GRAPH1_widget.setStyleSheet("background-color: rgb(30,30,30)")
#-------graph 1 widget making ends---------------------------------------------------------------------------------------------------
#-------graph2 widget starts, code can found on widget.py and plot.py-----------------------------------------------------------------------------------------
#-------graph voltage starts---------------------------------------------------------------------------------------------------------
        self.graphVoltage1 = graph([
        	{
        		"color": (245,252,255),
        		"name": "Voltage"
        	}], True, 200, "", "Voltage ")
        graphVoltage_Layout = QVBoxLayout()
        graphVoltage_Layout.addWidget(namewidget().nameline("Voltage"))
        graphVoltage_Layout.addWidget(self.graphVoltage1.graphWidget)
        self.graphVoltage = QtWidgets.QWidget()
        self.graphVoltage.setLayout(graphVoltage_Layout)
        self.graphVoltage.setStyleSheet("QLabel{color: #f5fcff; font: 10pt  'Oswald';background-color: rgb(3,0,13); }")
#-------graph voltage ends------------------------------------------------------------------------------------------------------------
#-------graph gps altitude starts-----------------------------------------------------------------------------------------------------
        self.graphGPS_Altitude1 = graph([
        	{
        		"color": (245,252,255),
        		"name": "GPS_Altitude"
        	}], True, 200, "", "GPS_Altitude")
        graphGPS_Altitude_Layout = QVBoxLayout()
        graphGPS_Altitude_Layout.addWidget(namewidget().nameline("GPS Altitude"))
        graphGPS_Altitude_Layout.addWidget(self.graphGPS_Altitude1.graphWidget)
        self.graphGPS_Altitude = QtWidgets.QWidget()
        self.graphGPS_Altitude.setLayout(graphGPS_Altitude_Layout)
        self.graphGPS_Altitude.setStyleSheet("QLabel{color: #f5fcff; font: 10pt  'Oswald';background-color: rgb(3,0,13); }")
#-------graph gps altitude ends--------------------------------------------------------------------------------------------------------
#-------graph titl xy starts-----------------------------------------------------------------------------------------------------------
        self.graphTilt_XY1 = graph([
        	{
        		"color": (245,252,255),
        		"name": "X-axis"
        	},{
                "color": (245,252,255),
        		"name": "Y-axis"
            }], True, 200, "", "Tilt_XY ")
        graphTilt_XY_Layout = QVBoxLayout()
        graphTilt_XY_Layout.addWidget(namewidget().nameline("Tilt XY"))
        graphTilt_XY_Layout.addWidget(self.graphTilt_XY1.graphWidget)
        self.graphTilt_XY = QtWidgets.QWidget()
        self.graphTilt_XY.setLayout(graphTilt_XY_Layout)
        self.graphTilt_XY.setStyleSheet("QLabel{color: #f5fcff; font: 10pt  'Oswald';background-color: rgb(3,0,13); }")
#-------graph titlt xy ends------------------------------------------------------------------------------------------------------------
#-------graph 2 widget making starts---------------------------------------------------------------------------------------------------
        GRAPH2_layout = QGridLayout()
        GRAPH2_layout.addWidget(self.graphVoltage,1,1,1,1)
        GRAPH2_layout.addWidget(self.graphGPS_Altitude,1,2,1,1)
        GRAPH2_layout.addWidget(self.graphTilt_XY,1,3,1,1)
        self.GRAPH2_widget = QtWidgets.QWidget()
        self.GRAPH2_widget.setLayout(GRAPH2_layout)
        self.GRAPH2_widget.setStyleSheet("background-color: rgb(30,30,30)")
#-------graph 2 widget ends-------------------------------------------------------------------------------------------------------------
#-------graph widget starts--------------------------------------------------------------------------------------------------------------
        graph_layout = QGridLayout()
        graph_layout.addWidget(self.GRAPH2_widget,2,1,1,1)
        graph_layout.addWidget(self.GRAPH1_widget,1,1,1,1)
        self.graph_widget = QtWidgets.QWidget()
        self.graph_widget.setLayout(graph_layout)
#-------graph widget ends--------------------------------------------------------------------------------------------------------------------
#-------gps widget starts----------------------------------------------------------------------------------------------------------------
        self.map = mapWidget()
        self.map.update(17.5449,78.5718)
#-------gps widget ends-----------------------------------------------------------------------------------------------------------------------
#-------telemtry output from cansat widget starts----------------------------------------------------------------------------------------------------------
        tele_layout = QGridLayout()
        self.logOutput = QtWidgets.QTextEdit()
        self.logOutput.setReadOnly(True)
        self.logOutput.setStyleSheet("background-color: rgb(20,20,20) ;border: 0px ;color: white;font-family: 'Oswald'")
        self.logOutput.setLineWrapMode(QtWidgets.QTextEdit.NoWrap)

        tele_layout.addWidget(self.logOutput)

        self.tele_widget = QtWidgets.QWidget()
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
        self.send.setStyleSheet("QPushButton{color: #f5fcff; font: 8pt  'Oswald';background-color: rgb(20,20,20); }")
        self.send.setFixedWidth(70)
        self.send.setFixedHeight(15)
#-------send button widget ends---------------------------------------------------------------------------------------------------------------------
#-------cmd text box plus send button widget starts------------------------------------------------------------------------------------------------
        tele_cmd_textbox_send_layout=QGridLayout()
        tele_cmd_textbox_send_layout.addWidget(self.tele_cmd_textbox,1,1,1,1)
        tele_cmd_textbox_send_layout.addWidget(self.send,1,2,1,1)
        self.tele_cmd_textbox_send_widget = QtWidgets.QWidget()
        self.tele_cmd_textbox_send_widget.setLayout(tele_cmd_textbox_send_layout)
#-------cmd text box plus send button widget ends-----------------------------------------------------------------------------------------------------
#-------cmd output box from text box widget starts----------------------------------------------------------------------------------------------------
        self.cmdOutput = QtWidgets.QTextEdit()
        self.cmdOutput.setReadOnly(True)
        self.cmdOutput.setMaximumHeight(130)
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
        self.cmd_widget.setStyleSheet("background-color: rgb(30,30,30)")
        self.cmd_widget.setLayout(cmd_layout)
#-------cmd textbox plus output box widget ends------------------------------------------------------------------------------------------------------------
#-------packet count widget starts---------------------------------------------------------------------------------------------------------
        self.packet_count=QLabel("Packet Count: 200")
        self.packet_count.setAlignment(QtCore.Qt.AlignCenter)
        packet_count_layout = QHBoxLayout()
        packet_count_layout.addWidget(self.packet_count)
        self.packet_count_widget = QtWidgets.QWidget()
        self.packet_count_widget.setFixedHeight(45)
        self.packet_count_widget.setStyleSheet("QLabel{color: #f5fcff; font: 10pt  'Oswald';background-color: rgb(30,30,30); }")
        self.packet_count_widget.setLayout(packet_count_layout)
#-------packet count widget ends--------------------------------------------------------------------------------------------------------------
#-------corrupted packets widget starts--------------------------------------------------------------------------------------------------------------
        self.corrupted_packets = QLabel("Corrupted Packets: 5")
        self.corrupted_packets.setAlignment(QtCore.Qt.AlignCenter)
        corrupted_packets_layout = QHBoxLayout()
        corrupted_packets_layout.addWidget(self.corrupted_packets)
        self.corrupted_packets_widget = QtWidgets.QWidget()
        self.corrupted_packets_widget.setFixedHeight(45)
        self.corrupted_packets_widget.setStyleSheet("QLabel{color: #f5fcff; font: 10pt  'Oswald';background-color: rgb(30,30,30); }")
        self.corrupted_packets_widget.setLayout(corrupted_packets_layout)
#-------corrupted packet widget ends-----------------------------------------------------------------------------------------------------------------
#-------packet count and corrupted packet widget starts-------------------------------------------------------------------------------------------------
        tele_pac_name_layout = QGridLayout()
        tele_pac_name_layout.addWidget(self.packet_count_widget,1,1,1,1)
        tele_pac_name_layout.addWidget(self.corrupted_packets_widget,1,2,1,1)
        self.tele_pac_name_widget = QtWidgets.QWidget()
        self.tele_pac_name_widget.setLayout(tele_pac_name_layout)
#-------packet count and corrupted packet widget ends---------------------------------------------------------------------------------------------------------
#-------full telemetry widget starts---------------------------------------------------------------------------------------------------------------------------
        telemet_layout = QGridLayout()
        telemet_layout.addWidget(namewidget().nameline("Telemetry"),1,1,1,4)
        telemet_layout.addWidget(self.tele_pac_name_widget,2,1,1,4)
        telemet_layout.addWidget(self.tele_widget,3,1,5,1)
        telemet_layout.addWidget(self.cmd_widget,8,1,3,1)
        self.telemet_widget = QtWidgets.QWidget()
        self.telemet_widget.setLayout(telemet_layout)
#-------telemetry widget ends--------------------------------------------------------------------------------------------------------------------------------------
#-------longitude, latitude , no. of gps widget starts---------------------------------------------------------------------------------------------------------------
        self.longitude = QLabel("Longitude: 78.5718°E")
        self.longitude.setAlignment(QtCore.Qt.AlignCenter)
        self.latitude = QLabel("Latitude: 17.5449°N")
        self.latitude.setAlignment(QtCore.Qt.AlignCenter)
        self.gps_location = QLabel("GPS Location")
        self.no_of_gps = QLabel("No. of GPS: 5")
        self.no_of_gps.setAlignment(QtCore.Qt.AlignCenter)

        no_of_gps_layout = QHBoxLayout()
        no_of_gps_layout.addWidget(self.no_of_gps)
        self.no_of_gps_widget = QtWidgets.QWidget()
        self.no_of_gps_widget.setStyleSheet("QLabel{color: #f5fcff; font: 10pt  'Oswald';background-color: rgb(30,30,30); }")
        self.no_of_gps_widget.setLayout(no_of_gps_layout)

        latitude_layout = QHBoxLayout()
        latitude_layout.addWidget(self.latitude)
        self.latitude_widget = QtWidgets.QWidget()
        self.latitude_widget.setStyleSheet("QLabel{color: #f5fcff; font: 10pt  'Oswald';background-color: rgb(30,30,30); }")
        self.latitude_widget.setLayout(latitude_layout)

        longitude_layout = QHBoxLayout()
        longitude_layout.addWidget(self.longitude)
        self.longitude_widget = QtWidgets.QWidget()
        self.longitude_widget.setStyleSheet("QLabel{color: #f5fcff; font: 10pt  'Oswald';background-color: rgb(30,30,30); }")
        self.longitude_widget.setLayout(longitude_layout)
#-------longitude and latitude widget---------------------------------------------------------------------------------------------------
        lines_layout = QGridLayout()
        lines_layout.addWidget(self.latitude_widget,1,1,1,1)
        lines_layout.addWidget(self.longitude_widget,1,2,1,1)
        self.lines_widget = QtWidgets.QWidget()
        self.lines_widget.setLayout(lines_layout)
#------latitude and longitude widget ends--------------------------------------------------------------------------------------------------
        gps_label_layout = QGridLayout()
        gps_label_layout.addWidget(namewidget().nameline("GPS Location"))
        gps_label_layout.addWidget(self.no_of_gps_widget,1,0,1,1)
        gps_label_layout.addWidget(self.lines_widget,2,0,1,1)
        self.gps_label_widget = QtWidgets.QWidget()
        #self.gps_label_widget.setFixedHeight(220)
        self.gps_label_widget.setLayout(gps_label_layout)
#-------longitude, latitude , no. of gps widget ends--------------------------------------------------------------------------------------------------------
#-------map and gps widget starts-------------------------------------------------------------------------------------------------------------------
        self.map.setFixedHeight(300)
        self.map.setStyleSheet("color: rgb(20,20,20)")
        gps_layout = QGridLayout()
        gps_layout.addWidget(self.gps_label_widget,1,0,1,1)
        gps_layout.addWidget(self.map,2,0,1,1)
        gps_layout.addWidget(self.telemet_widget,3,0,1,1)
        self.gps_widget = QtWidgets.QWidget()
        self.gps_widget.setLayout(gps_layout)
        self.gps_widget.setFixedWidth(500)
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

        all_layout.addWidget(self.MAIN_widget,1,1,1,1)
        all_layout.addWidget(self.gps_widget,1,2,1,1)
        self.all_widget = QtWidgets.QWidget()
        self.all_widget.setLayout(all_layout)
        self.all_widget.setStyleSheet("background-color: rgb(15,15,15)")
        self.setCentralWidget(self.all_widget)
#-------main window ends--------------------------------------------------------------------------------------------------
        self.timer = QtCore.QTimer()
        self.timer.setInterval(250)
        self.timer.timeout.connect(self.update)
        self.timer.start()

app = QtWidgets.QApplication(sys.argv)
w = MainWindow()
w.show()
sys.exit(app.exec_())