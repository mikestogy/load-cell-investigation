import serial.tools.list_ports
import numpy as np
import matplotlib.pyplot as plt
import time

ports = serial.tools.list_ports.comports()
serialInst = serial.Serial(port='COM3', baudrate=115200)

# Needed, for whatever reason, to scrap old data left in buffer
time.sleep(1)
serialInst.read_all()

collecting = True

rawLineList = []
counter = 0
# Accepts data while argument is true
print("Collecting...")
while counter < 1000:
    if serialInst.in_waiting:       # 1 or more characters in the input buffer
        rawLine = serialInst.readline()   # Reads one line of data as 'bytes'
        rawLineList.append(rawLine)     # Adds line to list
        counter += 1
print("Finished")
serialInst.close()
serialInst.close()


# Converts each value in rawLineList to usable/desired format into a new list of lists
cleanLineList = []
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
    x[i] = x[i] / 1000     # Convert to milliseconds

xDelta = []

for i in range((len(x)) - 1):
    xDelta.append(x[i+1] - x[i])

# Y values represent the converted differential voltage
y = dataArray[:, 1]
# Converted differential ADC value, or Y, is equal to (resolution/FSR) * V_in
# Solving for V_in, divide Y by (resolution/FSR)
for i in range(len(y)):
    y[i] = float(y[i])
    y[i] = y[i] * ((2*0.256)/65536)     # This is the raw differential voltage
    y[i] = y[i] * (1/0.001) * (5/5)      # Convert to kg
    y[i] = y[i] * 9.81      # Newtons of force

impulse = 0
for i in range(len(xDelta)):
    impulse += xDelta[i] * y[i]

# Make the plot
plt.figure(figsize=(14, 8), facecolor='lightgray')
plt.grid(True, color='gray', linestyle='--', linewidth=0.25)
plt.xticks(np.arange(min(x), max(x)+1, 50))
plt.yticks(np.arange(0, max(y)+1, 2))
plt.xlabel("Time (ms)")
plt.ylabel("Force (N)")
plt.title("Impulse")
ax = plt.gca()
ax.set_facecolor("lightgray")

plt.scatter(x, y)
plt.show()


