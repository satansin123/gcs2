from PyQt5.QtWidgets import QPushButton
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class MyButton(QPushButton):
    def __init__(self, text="Click me!", font_size=16, parent=None):
        super().__init__(text, parent)
        self.setFont(QFont("Arial", font_size))
        self.clicked.connect(self.change_color)
    
    def resizeEvent(self, event):
        button_size = min(event.size().width(), event.size().height()) * 0.8
        self.setFixedSize(button_size, button_size)
        font_size = int(button_size / 4)
        self.setFont(QFont("Arial", font_size))
    
    def change_color(self):
        if self.palette().button().color().name() == "red":
            self.setStyleSheet("background-color: green")
        else:
            self.setStyleSheet("background-color: red")