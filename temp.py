from digi.xbee.devices import XBeeDevice

# TODO: Replace with the serial port where your local module is connected to.
PORT = "COM5"
# TODO: Replace with the baud rate of your local module.
BAUD_RATE = 9600




def main():
    device = XBeeDevice(PORT, BAUD_RATE)
    device.open()

    while True:
        try:
            data = input('\n')
            
            
            device.send_data_broadcast(data + "\n")
            
        except:
            pass


if __name__ == '__main__':
    main()