import sys
import time
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt, QObject, QThread, pyqtSignal, pyqtSlot

# Simulated probe class to send/receive data
class RocketProbe(QObject):
    data_received = pyqtSignal(str)

    def __init__(self):
        super().__init__()

    def send_data(self, data):
        # Simulating data transmission delay
        time.sleep(2)
        self.data_received.emit(f"Received: {data}")

    def receive_data(self):
        # Simulating data retrieval delay
        time.sleep(2)
        return "Probe Data"


# Worker thread for sending data
class SendDataThread(QThread):
    def __init__(self, probe):
        super().__init__()
        self.probe = probe

    def run(self):
        data = "Data from Python"
        self.probe.send_data(data)


# Worker thread for receiving data
class ReceiveDataThread(QThread):
    data_received = pyqtSignal(str)

    def __init__(self, probe):
        super().__init__()
        self.probe = probe

    def run(self):
        data = self.probe.receive_data()
        self.data_received.emit(data)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Rocket Probe GUI")

        self.data_label = QLabel("No data received yet.")
        self.send_data_label = QLabel("")

        layout = QVBoxLayout()
        layout.addWidget(self.data_label)
        layout.addWidget(self.send_data_label)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    @pyqtSlot(str)
    def update_data_label(self, data):
        self.data_label.setText(data)

    @pyqtSlot(str)
    def update_send_data_label(self, data):
        self.send_data_label.setText(data)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()

    probe = RocketProbe()

    send_thread = SendDataThread(probe)
    send_thread.finished.connect(send_thread.deleteLater)

    receive_thread = ReceiveDataThread(probe)
    receive_thread.data_received.connect(main_window.update_data_label)
    receive_thread.finished.connect(receive_thread.deleteLater)

    # Move the receive thread to a different QThread to run simultaneously
    receive_thread.moveToThread(QThread())

    # Start the threads
    send_thread.start()
    receive_thread.start()

    main_window.show()
    sys.exit(app.exec_())