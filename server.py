import socket
import sys

NUM_OF_ARG = 1
MAX_PORT = 65545
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


def off():
    s.close()
    exit()


def check_arg():
    # Server port (and program name).
    if len(sys.argv) != NUM_OF_ARG + 1:
        off()

    # Check port is int type.
    try:
        port = int(sys.argv[1])
        if port > MAX_PORT:
            off()
        s.bind(('', port))
    except:
        off()


def print_data():
    for pkg in arr_data:
        print(pkg.decode('utf8'), end="")


check_arg()
# Start connection with the client - return first ack(amount).
amount, addr = s.recvfrom(3)
s.sendto(amount, addr)

# Initialization.
amount_int = int.from_bytes(amount, 'little')
arr_data = [b'0'] * amount_int
arr_bool = [False for i in range(amount_int)]
count = 0

while True:
    # If we got all packages we can print.
    if count == amount_int:
        # Make sure we print only once.
        count += 1
        print_data()
    data, addr = s.recvfrom(100)
    # amount ack failed - send again.
    if data == amount:
        s.sendto(amount, addr)
    else:
        pkg_index = int.from_bytes(data[-3:len(data)], 'little')
        # New package.
        if not arr_bool[pkg_index]:
            arr_data[pkg_index] = data
            arr_bool[pkg_index] = True
            if count <= amount_int:
                count += 1
        # send package ack.
        s.sendto(data, addr)
