####################################################
#  D1014636 潘子珉                                      									
####################################################
import socket
import threading
import eel
eel.init('gui', allowed_extensions=['.js', '.html'])

PORT = 6666
backlog = 5
BUF_SIZE = 1024			# Receive buffer size

def clientThread(client, clientAddress):
    print(f"socket connect {clientAddress[0]}:{clientAddress[1]}")
    eel.writeMsg(2, f"socket connect {clientAddress[0]}:{clientAddress[1]}")
    client_msg = client.recv(BUF_SIZE)
    while client_msg:
        client_utf8 = client_msg.decode('utf-8')
        print(client_utf8)
        eel.writeMsg(1, f"{client_utf8} from: {clientAddress[0]}:{clientAddress[1]}")
        client_count = int(client_utf8)
        if client_count >= 0:
            client_count = client_count - 1
            server_reply = str(client_count)
            client.send(server_reply.encode('utf-8'))
            client_msg = client.recv(BUF_SIZE)
        else:
            break
    eel.writeMsg(2, f"socket close {clientAddress[0]}:{clientAddress[1]}")
    client.close()

def main():
    srvSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srvSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    eel.writeMsg(2, "create socket")
    srvSocket.bind(('', PORT))
    srvSocket.listen(backlog)
    eel.writeMsg(2, f"socket bind port:{PORT}")
    while 1:
        client, clientAddress = srvSocket.accept()
        threading.Thread(target=clientThread, args=(client, clientAddress)).start()

threading.Thread(target=main).start()
eel.start('Server.html', size=(500, 500), port=0)  # Start