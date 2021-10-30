# Itay Etelis 209041474
# Ben Levi 318811304
import socket
import sys

NUM_OF_ARG = 3
SIZE_PKG = 97
MAX_PORT = 65545
MAX_IP = 255
DEFAULT_TIMEOUT = 12
c_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
c_socket.settimeout(DEFAULT_TIMEOUT)


def off():
    c_socket.close()
    exit()


def check_arg():
    # IP + PORT + FILE_NAME (and program name).
    if len(sys.argv) != NUM_OF_ARG + 1:
        off()
    try:
        # Check valid IP address.
        arr = sys.argv[1].split('.')
        # IPv4
        if len(arr) != 4:
            off()
        for n in arr:
            if int(n) > MAX_IP or int(n) < 0:
                off()

        # Check port is valid int type.
        if int(sys.argv[2]) > MAX_PORT or int(sys.argv[2]) < 0:
            off()
    except:
        off()


check_arg()
IP = sys.argv[1]
PORT = int(sys.argv[2])
FILE_NAME = sys.argv[3]

arr_data = []
# Check file is exist.
try:
    data = open(FILE_NAME, "rb").read()
    # Create bytes array from the data.
    arr_data = [data[i:i + SIZE_PKG] for i in range(0, len(data), SIZE_PKG)]
except:
    off()

# Add to any package the right index.
for i in range(0, len(arr_data)):
    arr_data[i] += i.to_bytes(3, 'little')
# Array for mark ack \ not ack.
arr_ack = [False for i in range(len(arr_data))]


# If we got ack for all packages.
def finish():
    for sign in arr_ack:
        if not sign:
            return False
    return True


def ack():
    try:
        while True:
            data_ack, addr = c_socket.recvfrom(100)
            pkg_index = int.from_bytes(data_ack[-3:len(data_ack)], 'little')
            arr_ack[pkg_index] = True
    except:
        # Continue send the remaining packages.
        if not finish():
            send_pkgs()


def send_pkgs():
    index = 0
    for pkg in arr_data:
        # Package with no ack - send again.
        if not arr_ack[index]:
            c_socket.sendto(pkg, (IP, PORT))
        index += 1
    ack()


def start_net(amount):
    # Send server amount of packages.
    c_socket.sendto(amount, (IP, PORT))
    try:
        # Get ack and start send packages.
        ack_amount, addr = c_socket.recvfrom(3)
        send_pkgs()
    except socket.timeout:
        start_net(amount)


start_net((len(arr_data)).to_bytes(3, 'little'))
c_socket.close()
