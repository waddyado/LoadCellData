import serial, time
import matplotlib.pyplot as plt
import re
import os

def visualize():
    data_file = "data.txt"

    data = []

    load1_data = []
    load2_data = []

    with open(data_file, "r") as f:
            data = f.readlines()

	
    for d in data:
	
            load1 = d.split(" ")[4]
            load2 = d.split(" ")[12].strip("\n")

            print("load1: " + load1 + "\tload2: " + load2)

            load1 = float(load1)

            load1_data.append(load1)
            
            # invert load2 value(optional)
            load2 = -1 * float(load2)
            
            load2_data.append(load2)




        # calculate k point moving averages

    k = 5

    n = (len(load1_data) / 5) - k

	

    fig, axs = plt.subplots(2,2)

    axs[0, 0].plot(load1_data)
    axs[0, 1].plot(load2_data)

    plt.show()


try:
    print('Press CTRL+C to stop gathering data')
    time.sleep(1)
    ser = serial.Serial(port='COM3', baudrate=57600, timeout=.1)
    ser.flushInput()
    file = open('data.txt', 'w')
    while True:
        ser_bytes = ser.readline()
        decoded_bytes = ser_bytes.decode('utf-8')
        print(ser_bytes.decode('utf-8'))
        if decoded_bytes == '':
            continue
        else:
            file.write(str(decoded_bytes))


except KeyboardInterrupt:
    
    print('Data gathering stopped')
    file.close()
    file = open('data.txt', 'r')
    data = []
    for line in file:
        if not line.isspace():
            data.append(line)
    file.close()
    file = open('data.txt', 'w')
    for item in data:
        file.write(item)
    print('Data formatted\n')
    file.close()
    
    inp = input('Would you like to visualize your data? (Y/N) :')
    
    while True:
        if inp == 'Y':
            visualize()
            break  
        elif inp == 'N':
            print('Have a nice day')
            quit()
        else:
            print('Invalid input.\n')
        
except:
    print('USB error, Make sure no other applications are open\nand that the arduino is connected to the right port')


