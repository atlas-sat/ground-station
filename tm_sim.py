# code simulates telemetry being appended to telemetry.csv

import random
import time

def start():
    # listen for incoming data
    while True:
        # simulate telemetry data
        x = random.randint(0, 255)
        y = random.randint(0, 255)
        print(x, y)

        # write data to a file
        with open("telemetry.csv", 'a') as file:
            # write x and y to the file
            file.write(str(x))
            file.write(',')
            file.write(str(y))
            file.write('\n')
        
        time.sleep(20)

start()