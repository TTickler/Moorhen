import socket
import sys



HOST = ''
PORT = 8888

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((HOST, PORT))
except socket.error as msg:
    print msg
    sys.exit()

s.listen(10)
conn, addr = s.accept()
while True:
    #conn, addr = s.accept()
    data = conn.recv(4096)
    message = data.decode()
    print(message)
    print 'Connected with ' + addr[0] + ':' + str(addr[1])
