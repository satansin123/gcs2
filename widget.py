from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QLabel, QHBoxLayout

class namewidget():
    def __init__(self):
        self.name = QLabel()
        self.line = QLabel('  ')

    def nameline(self, name, width, height, fontsize):
        self.name.setText(name)
        self.name.setStyleSheet("QLabel{color: #f5fcff; font: %spt 'Oswald'; background-color: rgb(20,20,20); }" % fontsize)
        self.line.setText('  ')
        self.line.setFixedWidth(width)
        self.line.setFixedHeight(height)
        #self.line.setStyleSheet("QLabel{background-color: red}")
        self.line.setStyleSheet("QLabel{background-color: rgb(59, 146, 184)}")

        name_layout = QHBoxLayout()
        name_layout.addWidget(self.line)
        name_layout.addWidget(self.name)

        self.name_widget = QtWidgets.QWidget()
        self.name_widget.setLayout(name_layout)

        return self.name_widget

    def update_name(self, new_name):
        self.name.setText(new_name)

    def update_color(self,color):
        self.line.setStyleSheet("QLabel{background-color: %s}" %color)