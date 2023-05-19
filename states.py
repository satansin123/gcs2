from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt5.QtCore import QSize


class DotAndState(QWidget):
    def __init__(self, state_name, dot_size, state_size):
        super().__init__()

        self.dot_label = QLabel("🔴")
        self.state_label = QLabel(state_name)

        layout = QVBoxLayout()
        layout.addWidget(self.dot_label)
        layout.addWidget(self.state_label)

        self.setLayout(layout)
        self.setFixedSize(QSize(state_size, state_size))

    def setDotColor(self, color):
        self.dot_label.setText(color)
