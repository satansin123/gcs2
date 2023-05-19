from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from dotandstate import DotAndState
from digi.xbee.devices import XBeeDevice, RemoteXBeeDevice, XBee64BitAddress
from digi.xbee.models.address import XBeeAddress
from digi.xbee.exception import TimeoutException
import serial


class MainWidget(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        # Create the DotAndState widgets for each state
        self.states = []
        state_names = ["Ascent", "Descent", "Heat Shield Deployed", "Rocket Separation",
                       "Parachute Deployed", "Probe Deployed", "Landed", "Mast Raised"]
        dot_sizes = [50, 50, 50, 50, 50, 50, 50, 50]
        state_sizes = [100, 100, 100, 100, 100, 100, 100, 100]

        for i in range(len(state_names)):
            dot_and_state = DotAndState(state_names[i], dot_sizes[i], state_sizes[i])
            layout.addWidget(dot_and_state)
            self.states.append(dot_and_state)

        self.setLayout(layout)

    def updateState(self, state_index, dot_color):
        self.states[state_index].setDotColor(dot_color)


def receive_data_callback(xbee_message):
    try:
        data = xbee_message.data.decode()
        print("Received data: %s" % data)

        # Example logic to update the dot color based on received data
        if data == "ASCENT":
            main_widget.updateState(0, "🟢")
        elif data == "DESCENT":
            main_widget.updateState(1, "🟢")
        elif data == "HEAT_SHIELD_DEPLOYED":
            main_widget.updateState(2, "🟢")
        elif data == "ROCKET_SEPARATION":
            main_widget.updateState(3, "🟢")
        elif data == "PARACHUTE_DEPLOYED":
            main_widget.updateState(4, "🟢")
        elif data == "PROBE_DEPLOYED":
            main_widget.updateState(5, "🟢")
        elif data == "LANDED":
            main_widget.updateState(6, "🟢")
        elif data == "MAST_RAISED":
            main_widget.updateState(7, "🟢")

    except Exception as e:
        print("Error in receive_data_callback:", str(e))


if __name__ == '__main__':
    app = QApplication([])
    window = QMainWindow()

    main_widget = MainWidget()
    window.setCentralWidget(main_widget)

    # Configure XBee device
    serial_port = "COM1"  # Replace with the actual serial port
    baud_rate = 9600

    try
