import serial.tools.list_ports
import numpy as np
import matplotlib.pyplot as plt
import time

ports = serial.tools.list_ports.comports()
serialInst = serial.Serial()

portList = []

for onePort in ports:
    portList.append(str(onePort))
    print(str(onePort))

val = input("select Port: COM")

for x in range(0, len(portList)):
    if portList[x].startswith("COM" + str(val)):
        portVar = "COM" + str(val)
        print(portList[x])

serialInst.baudrate = 115200
serialInst.port = portVar
serialInst.open()

# Needed, for whatever reason, to scrap old data left in buffer
time.sleep(1)
serialInst.read_all()

rawLineList = []
cleanLineList = []
counter = 0

collecting = True

# Arduino Serial.println() converts inputs to strings then sends their ASCII value
# serial.readLine reads this data and separates it into 'bytes' at a new line
# 'Bytes' is a list which contains the ASCII value, as an int, of each character sent
# example: Serial.println(42) is converted to string 42. The ASCII value of each character is then sent.
# the '4' character is sent with a 52, and the '2' character is sent with a 50. Therefore,
# 'bytes' is a list of ints [52, 50]

# Accepts 30 data values
while counter < 1000:
    if serialInst.in_waiting:       # 1 or more characters in the input buffer
        rawLine = serialInst.readline()   # Reads one line of data as 'bytes'
        rawLineList.append(rawLine)     # Adds line to list
        counter += 1

# Converts each value in rawLineList to usable/desired format into a new list of lists
for x in range(len(rawLineList)):
    cleanLine = rawLineList[x]      # Take the first line, or 'bytes', from rawLineList
    cleanLine = cleanLine.decode().split()      # Decode and split the bytes of ASCII characters into a list of strings
    for j in range(len(cleanLine)):
        cleanLine[j] = float(cleanLine[j])        # Converts all string elements of list to float
    cleanLineList.append(cleanLine)     # Adds line to list

# Convert cleanLineList to a numpy array called dataArray
dataArray = np.array(cleanLineList)

# X values represent time in microseconds
x = dataArray[:, 0]
timeZero = x[0]
for i in range(len(x)):
    x[i] = x[i] - timeZero    # Zero out the time to the first data point
    x[i] = x[i] / 1000      # Convert to milliseconds

# Y values represent the converted differential voltage
y = dataArray[:, 1]
# Converted differential ADC value, or Y, is equal to (resolution/FSR) * V_in
# Solving for V_in, divide Y by (resolution/FSR)
for i in range(len(y)):
    y[i] = float(y[i])
    y[i] = y[i] * ((2*0.256)/65536)     # This is the raw differential voltage
    y[i] = y[i] * (1/0.001) * (5/5)      # Convert to kg
    y[i] = y[i] * 9.81      # Newtons of force

# Make the plot
plt.figure(figsize=(16*0.8, 9*0.8), facecolor='lightgray')
plt.scatter(x, y)
plt.xticks(np.arange(min(x), max(x)+1, 50))
plt.yticks(np.arange(0, max(y)+1, 2))
plt.xlabel("Time (ms)")
plt.ylabel("Force (N)")
plt.title("Impulse")
plt.show()


