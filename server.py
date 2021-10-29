import socket
import sys

PORT = int(sys.argv[1])
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('', PORT))


amount, addr = s.recvfrom(3)
s.sendto(amount, addr)
amount_int = int.from_bytes(amount, 'little')
arr_data = [b'0'] * amount_int
arr_bool = [False for i in range(amount_int)]
count = 0


def print_data():
    for pkg in arr_data:
        print(pkg.decode('utf8'))


while True:
    if count == amount_int:
        print_data()
    data, addr = s.recvfrom(100)
    if data == amount:
        s.sendto(amount, addr)
    else:
        pkg_index = int.from_bytes(data[-3:len(data)], 'little')
        if not arr_bool[pkg_index]:
            arr_data[pkg_index] = data
            arr_bool[pkg_index] = True
            if count <= amount_int:
                count += 1
        # that's why the client will stop at the end.
        s.sendto(data, addr)

