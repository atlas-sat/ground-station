import serial
import time

can_listen = False

ser = None

def start():
    global can_listen, ser
    can_listen = True

    # configure the serial connections (the parameters differs on the device you are connecting to)
    ser = serial.Serial(
        port='COM6',
        baudrate=9600,
        timeout=30 # always set to longer than the time between telemetry packets
    )

    # wait for the HC12 to initialize
    time.sleep(1)

    # listen for incoming data
    while can_listen:
        x = ser.read_until(b'\r\n')
        print(x)
        x = bytearray(x)

        # check if x is empty
        if not x:
            break

        # access 15th byte of x
        print(x[14])
        # access 16th byte of x
        print(x[15])

        # write data to a file
        with open("telemetry.csv", 'a') as file:
            # write x[14] and x[15] to the file
            file.write(str(x[14]))
            file.write(',')
            file.write(str(x[15]))
            file.write('\n')

    
    # close the serial connection
def stop():
    global can_listen, ser
    can_listen = False
    print("Stopped listening")
    ser.close()