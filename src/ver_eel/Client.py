####################################################
#  D1014636 潘子珉                                      									
####################################################
#import sys
import socket
import threading
import eel
eel.init('gui', allowed_extensions=['.js', '.html'])

PORT = 6666
BUF_SIZE = 1024			# Receive buffer size

def main(serverIP, val1):
    cSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    eel.writeMsg(2, "create socket")

    print('Connecting to %s port %s' % (serverIP, PORT))
    try:
        cSocket.connect((serverIP, PORT))
    except Exception as msg:
        eel.writeMsg(4, msg)
        return
    val1 = int(val1) - 1
    val1Str = str(val1)
    cSocket.send(val1Str.encode('utf-8'))
    eel.writeMsg(0, val1Str)
    
    server_reply = cSocket.recv(BUF_SIZE)
    while server_reply:
        server_utf8 = server_reply.decode('utf-8')
        print(server_utf8)
        eel.writeMsg(1, server_utf8)
        server_count = int(server_utf8)
        if server_count >= 0:
            server_count = server_count - 1
            val1Str = str(server_count)
            eel.writeMsg(0, val1Str)
            cSocket.send(val1Str.encode('utf-8'))
            server_reply = cSocket.recv(BUF_SIZE)
        else:
            break
    eel.writeMsg(2, "socket close")
    cSocket.close()

@eel.expose
def start(serverIP, val1):
    threading.Thread(target=main, args=(serverIP, val1)).start()

eel.start('Client.html', size=(500, 500), port=0)  # Start