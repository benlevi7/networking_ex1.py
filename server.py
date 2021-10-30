# Itay Etelis 209041474
# Ben Levi 318811304
import socket
import sys

NUM_OF_ARG = 1
MAX_PORT = 65545
s_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


def off():
    s_socket.close()
    exit()


def check_arg():
    # Server port (and program name).
    if len(sys.argv) != NUM_OF_ARG + 1:
        off()

    # Check port is valid int type.
    try:
        port = int(sys.argv[1])
        if port > MAX_PORT or port < 0:
            off()
        s_socket.bind(('', port))
    except:
        off()


def print_data():
    for pkg in arr_data:
        print(pkg.decode('utf8'), end="")


check_arg()
# Start connection with the client - return first ack(amount).
amount, addr = s_socket.recvfrom(3)
s_socket.sendto(amount, addr)

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
    data, addr = s_socket.recvfrom(100)
    # Amount ack failed - send again.
    if data == amount:
        s_socket.sendto(amount, addr)
    else:
        pkg_index = int.from_bytes(data[-3:len(data)], 'little')
        # New package.
        if not arr_bool[pkg_index]:
            arr_data[pkg_index] = data
            arr_bool[pkg_index] = True
            if count <= amount_int:
                count += 1
        # Send package ack.
        s_socket.sendto(data, addr)
