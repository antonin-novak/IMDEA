from serial.tools.list_ports import comports

# print all available ports
for port in comports():
    print(port)
