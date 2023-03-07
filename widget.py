
from QSwitchControl import SwitchControl
from PyQt5 import *
import sys
import os
from random import randint
from plot import graph
from map_plot import mapWidget
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtWidgets
from PyQt5 import QtCore

class states():
     def dotAndState(self,state,colour,height,fontsize):
        self.state_label=QLabel(state)
        if colour == "red":
            self.dot= QLabel("🔴")
        if colour == "green":
            self.dot= QLabel("🟢")
        self.dot.setStyleSheet("QLabel{color: rgb(255,0,13); ; font: %spt  'Oswald'; background-color: rgb(30,30,30);}" % fontsize)
        self.state_label.setStyleSheet("QLabel{color: #f5fcff; font: %spt  'Oswald';background-color: rgb(30,30,30); }" % fontsize)

        self.layout=QGridLayout()
        self.layout.addWidget(self.dot,1,1,1,1)
        self.layout.addWidget(self.state_label,1,2,1,5)
        self.layout_widget = QtWidgets.QWidget()
        self.layout_widget.setLayout(self.layout)
        self.layout_widget.setFixedHeight(height)
        return self.layout_widget
     
class namewidget():
    def nameline(self,name,width,height,fontsize):
        self.name= QLabel(name)
        self.name.setStyleSheet("QLabel{color: #f5fcff; font: %spt  'Oswald';background-color: rgb(20,20,20); }" %fontsize)
        self.line= QLabel('  ')
        self.line.setFixedWidth(width)
        self.line.setFixedHeight(height)
        self.line.setStyleSheet("QLabel{background-color: rgb(59, 146, 184)}")
        name_layout = QHBoxLayout()
        name_layout.addWidget(self.line)
        name_layout.addWidget(self.name)
        self.name_widget = QtWidgets.QWidget()
        self.name_widget.setLayout(name_layout)
        return self.name_widget
    
class button():
    def buttonfunc(self,name,fontsize):
        self.button_name= QtWidgets.QPushButton()
        self.button_name.setText(name)
        self.button_name.setStyleSheet("QPushButton{color: #f5fcff; font: %spt  'Oswald';background-color: rgb(30,30,30); }" % fontsize)

        button_layout=QHBoxLayout()

        button_layout.addWidget(self.button_name)

        self.button_widget = QtWidgets.QWidget()
        self.button_widget.setLayout(button_layout)
        self.button_widget.setFixedHeight(60)
        return self.button_widget
