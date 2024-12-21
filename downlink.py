import serial
import time
import os
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# read all files in the input folder, then append the byte arrays to a list
def read_files():
    byte_string = b''
    # for file in sorted(os.listdir("output")):
    # get number of files in the input folder
    num_files = len(os.listdir("input"))
    logging.info(f"Found {num_files} files in the input folder")
    for i in range(num_files):
        file = f"chunk_{i}.wav"
        with open(f"input/{file}", 'rb') as f:
            # append the byte string to byte_string
            byte_string += f.read()
    return byte_string

# turn a byte array into a single file
def create_file(byte_array, file_name):
    # turn byte array into a byte string
    with open(f"{file_name}", 'wb') as file:
        file.write(byte_array)

def start():

    # Connects to a 433MHz joined to a UART USB Bridge at COM8 (for example)
    ser = serial.Serial('COM6')
    ser.baudrate = 9600 # Baud Rate configured in the HC-12, refer to datasheet to set
    ser.timeout = 30 # timeout to prevent readline from blocking

    time.sleep(1) # wait for HC12 to initialize

    # send the start command to the HC-12
    ser.write(b'start')
    logging.info("Sent START command to HC-12")

    ser.close()

def downlink_start():

    # Connects to a 433MHz joined to a UART USB Bridge at COM8 (for example)
    ser = serial.Serial('COM6')
    ser.baudrate = 9600 # Baud Rate configured in the HC-12, refer to datasheet to set
    ser.timeout = 1 # timeout to prevent readline from blocking

    time.sleep(1) # wait for HC12 to initialize

    # send the downlink command to the HC-12
    ser.write(b'downlink')
    logging.info("Sent DOWNLINK command to HC-12")

    # Create a directory named after the current time
    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    os.makedirs(current_time, exist_ok=True)
    output_file_path = os.path.join(current_time, "output.wav")

    # receive byte arrays from the HC-12 and write them to a file
    cntr = 0
    finished = False
    while byte_array := ser.read(64):
        with open(output_file_path, 'ab') as file:
            # check if byte array contains EOF
            if b'EOF' in byte_array:
                logging.info("Received EOF")
                # remove EOF from byte array
                byte_array = byte_array[:byte_array.index(b'EOF')]
                # set finished to True
                finished = True
            file.write(byte_array)
            logging.info(f"Received {len(byte_array)} bytes from HC-12")
            logging.info(f"Counter: {cntr}")
            cntr += 1
        if finished:
            ser.close()
            logging.info("Serial connection closed")
            break