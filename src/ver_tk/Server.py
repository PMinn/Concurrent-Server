####################################################
#  D1014636 潘子珉                                      									
####################################################
import socket
import module.tk as tk
import threading

PORT = 6666
backlog = 5
BUF_SIZE = 1024			# Receive buffer size


class Socket():
    def __init__(self):
        self.appendFunction = None
        self.isSrart = False
        self.counter = 1
        
    def init(self):
        self.srvSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.srvSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        consoleFmt = "%-25s"
        self.appendFunction(consoleFmt % ("[create socket]",), '#9c7f00')
        self.appendFunction(consoleFmt % ("[setsockopt]",), '#9c7f00')

    def start(self):
        t = threading.Thread(target = self.startTread)
        t.start()
        
    def startTread(self):
        consoleFmt = "%-25s    %s"
        self.isSrart = True
        self.srvSocket.bind(('', PORT))
        self.srvSocket.listen(backlog)
        self.appendFunction(consoleFmt % ("[bind]", f" port: {PORT}"), '#9c7f00')
        self.appendFunction(consoleFmt % ("[socket listen]",""), '#9c7f00')
        print('Starting up server on port: %s' % (PORT))
        
        while(self.isSrart):
            t_name = 'Thread ' + str(self.counter)
            self.counter += 1
            print('Number of threads: %d' % threading.active_count())
            print('Waiting to receive message from client')
            client, (rip, rport) = self.srvSocket.accept()
            print('Got connection. Create thread: %s' % t_name)
            #self.append(consoleFmt % ("[socket close]", str(self.rip), str(self.rport), ""), color = '#9c7f00')
            ServerThread(t_name, client, rip, rport, self.appendFunction)
            
    def stop(self):
        self.isSrart = False
        self.srvSocket.close()
        self.init()

    def setAppendFunction(self, func):
        self.appendFunction = func
        self.init()
        
class ServerThread(threading.Thread):
    def __init__(self, t_name, client_sc, rip, rport, appendFunction):
        self.append = appendFunction
        super().__init__(name = t_name)
        self.client = client_sc
        self.rip = rip
        self.rport = rport
        self.start()

    def run(self):
        consoleFmt = "%-25s %s : %s   %s"
        self.append(consoleFmt % ("[socket connect]", str(self.rip), str(self.rport), ""), "#9c7f00")
        
        #name = threading.current_thread().name
        client_msg = self.client.recv(BUF_SIZE)

        while client_msg:
            client_utf8 = client_msg.decode('utf-8')
            print(client_utf8)
            self.append(consoleFmt % ("[recv]", str(self.rip), str(self.rport), f"data:  {client_utf8}"))
            client_count = int(client_utf8)
            
            if client_count >= 0:
                # Send message to client
                client_count = client_count - 1
                server_reply = str(client_count)
                #self.append(consoleFmt % ("[send]", str(self.rip), str(self.rport), f"data: {server_reply}"), "#009c0d")
                self.client.send(server_reply.encode('utf-8'))
                client_msg = self.client.recv(BUF_SIZE)
            else:
                break
        
        self.append(consoleFmt % ("[socket close]", str(self.rip), str(self.rport), ""), '#9c7f00')
        self.client.close()

def window_init():
    window = tk.Window()
    socket = Socket()
    window.socket = socket
    console = tk.Console(window)
    socket.appendFunction = console.append
    socket.init()
    window.mainloop()
    
if __name__ == '__main__':
    window_init()
