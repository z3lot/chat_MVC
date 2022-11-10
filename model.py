import socket
import threading

def consol_log(t,**args):
    print(t)

class SocketServer():
    def __init__(self,ip,port,func,tree=None):
        self.ip_srv = (ip,port)
        self.func = func
        self.tree = tree
        self.connections = {}
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        self.err = False
        try:
            self.sock.bind(self.ip_srv)
            self.func(f"[log] -> Server-init-to: {self.ip_srv}",logger=True)
            self.sock.listen(3)
        except Exception as err:
            self.func(f"{err}",logger=True)
            self.err = True

    def recv_message(self,conn,addr):
        user = None
        while True:
            if user == None:
                data = conn.recv(512).decode()
                data = data.split()
                user = data[0]
                hostname = data[1]
                if user in self.connections:
                    conn.sendall(b"[Err] -> Username-in-use")
                    conn.sendall(b"/exit")
                    conn.close()
                    self.func(f"[Err] -> Connection-close: {addr}->in-Set-your-username",logger=True)
                    break
                self.connections[user] = conn
                if self.tree != None:
                    self.tree(user,addr[0],addr[1],hostname,opt="add")
                continue
            try:
                msg = self.connections[user].recv(512)
            except:
                break
            if msg:
                if msg == b"/exit":
                    self.connections[user].close()
                    self.connections.pop(user)
                    self.func(f"[log] -> Connection-close: [{user}]->{addr}",logger=True)
                    if self.tree != None:
                        self.tree(user,None,None,None,opt="del")
                    break
                self.func(f"[log] -> {addr}->[{user}]: {msg.decode()}",logger=True)
                # enviar mensages a los demas usuarios
                for cl in list(self.connections.keys()):
                    if user != cl:
                        self.connections[cl].sendall(f"[{cl}] -> {msg.decode()}".encode())

    def connection_accept(self):
        while True:
            try:
                conn,addr = self.sock.accept()
            except:
                break
            self.func(f"[log] -> New-connection: {addr}",logger=True)
            threading.Thread(target=self.recv_message,args=(conn,addr),daemon=True).start()

    def run(self):
        if self.err == False:
            threading.Thread(target=self.connection_accept,daemon=True).start()

    def stop(self):
        for u in list(self.connections.keys()):
            self.connections[u].sendall(b"/exit")
            self.connections[u].shutdown(1)
            self.connections[u].close()
            self.err = True
            self.tree(u,None,None,None,"del")
        self.connections = {}
        self.sock.shutdown(1)
        self.sock.close()
        self.func("[log] -> Server-stop",logger=True)

class SocketClient():
    def __init__(self,ip,port,func,user=None):
        self.ip_srv = (ip,port)
        self.func = func
        self.user = user
        self.hostname = socket.gethostname().encode()
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.err = False
        try:
            self.sock.connect(self.ip_srv)
            self.runner = True
            if user != None:
                self.sock.sendall(self.user.encode() + b" " + self.hostname)
            self.func(f"[info] -> connect: {self.ip_srv}-as>{self.user}")
        except Exception as err:
            self.func(f"{err}")
            self.err = True

    def recv_message(self):
        while True:
            try:
                msg = self.sock.recv(512)
            except:
                break
            if msg:
                if msg == b"/exit":
                    self.func("[info] -> Server-disconnect")
                    self.sock.close()
                    break
                self.func(msg.decode(),sound=True)

    def send_to_srv(self,msg=None,gui=True):
        if gui == True:
            self.func(f"[{self.user}] -> {msg}")
            msg = msg.encode()
            self.sock.sendall(msg)
        else:
            while self.runner == True:
                if self.user == None:
                    self.user = input("username:")
                    self.sock.sendall((self.user).encode() + b" " + self.hostname)
                msg = input().encode()
                if msg == b"/exit":
                    self.sock.sendall(msg)
                    self.sock.close()
                    self.func("cliente cerrado")
                    break
                self.sock.sendall(msg)
                self.func(f"[{self.user}]:{msg.decode()}")
                print('test')

    def run(self):
        if self.err == False:
            self.recive = threading.Thread(target=self.recv_message,daemon=True)
            self.recive.start()
            if __name__ == "__main__":
                self.send_to_srv(gui=False)

    def stop(self):
        self.runner = False
        try:
            self.sock.sendall(b"/exit")
        except:
            pass
        self.sock.shutdown(1)
        self.sock.close()

