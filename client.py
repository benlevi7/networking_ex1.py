import socket
import sys
import time

IP = sys.argv[1]
PORT = int(sys.argv[2])
FILE_NAME = sys.argv[3]
DEFAULT_TIMEOUT = 12
SIZE_PKG = 97


s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.settimeout(DEFAULT_TIMEOUT)


data = open(FILE_NAME, "rb").read()
arr_data = [data[i:i + SIZE_PKG] for i in range(0, len(data), SIZE_PKG)]
for i in range(0, len(arr_data)):
    arr_data[i] += i.to_bytes(3, 'little')

arr_ack = [False for i in range(len(arr_data))]


def finish():
    for sign in arr_ack:
        if not sign:
            return False
    return True


def ack():
    try:
        while True:
            data_ack, addr = s.recvfrom(100)
            pkg_index = int.from_bytes(data_ack[-3:len(data_ack)], 'little')
            arr_ack[pkg_index] = True
    except:
        if not finish():
            send_pkgs()


def send_pkgs():
    inedx = 0
    for pkg in arr_data:
        if not arr_ack[inedx]:
            s.sendto(pkg, (IP, PORT))
            time.sleep(0.1)
        inedx += 1
    ack()


def start_net(amount):
    s.sendto(amount, (IP, PORT))
    try:
        get_num, addr = s.recvfrom(3)
        send_pkgs()
    except socket.timeout:
        start_net(amount)


start_net((len(arr_data)).to_bytes(3, 'little'))
s.close()
