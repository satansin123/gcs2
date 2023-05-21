import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5.QtGui import QPainter, QColor, QBrush
from PyQt5.QtCore import Qt

class CircularButton(QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(100, 100)
        self.setStyleSheet("border-radius: 50px;")
        self.clicked.connect(self.on_clicked)

    def on_clicked(self):
        # Handle button click event
        print("Button clicked!")

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QBrush(QColor('red')))
        painter.setPen(Qt.NoPen)
        size = min(self.width(), self.height())
        painter.drawEllipse((self.width() - size) // 2, (self.height() - size) // 2, size, size)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = QWidget()
    button = CircularButton(widget)
    button.setGeometry(50, 50, 100, 100)
    widget.setGeometry(200, 200, 200, 200)
    widget.show()
    sys.exit(app.exec_())
