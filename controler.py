import tkinter
from playsound import playsound
from view import View
from model import SocketServer,SocketClient

class Controller():
    def __init__(self):
        root = tkinter.Tk()
        self.gui = View(root)

        self.gui.master.wm_title("ChatLAN")
        self.gui.master.bind("<Return>",lambda e:self.sendmsg())
        self.gui.master.protocol("WM_DELETE_WINDOW", self.__closing)
        self.gui.ip_var.set("localhost")
        self.gui.port_var.set("9090")
        self.gui.user_var.set("username")

        self.server_btn_active = False
        self.client_btn_active = False
        self.tree_dict = {}
        self.gui.server_btn.config(command=self.init_server)
        self.gui.client_btn.config(command=self.init_client)
        self.gui.msg_send_btn.config(command=self.sendmsg)

        self.gui.mainloop()

    def __sound(self):
        playsound("sound.mp3")

    def __closing(self):
        try:
            self.clnt.stop()
        except:
            pass
        finally:
            self.gui.master.destroy()

    def __write_logs(self,log):
        with open("file.log","a") as f:
            f.write(log+"\n")

    def __input_basic_check(self):
        if self.gui.ip_var.get() != "localhost":
            try:
                for i in self.gui.ip_var.get():
                    if i != ".":
                        int(i)
            except:
                self.add_msg_log("[Err] -> IP-incorrect")
                return False
        try:
            int(self.gui.port_var.get())
        except:
            self.add_msg_log("[Err] -> PORT-incorrect")
            return False
        return True

    def init_server(self):
        if self.gui.server_check_var.get() == True and self.__input_basic_check() == True:
            if self.server_btn_active == False:
                ip = self.gui.ip_var.get()
                port = int(self.gui.port_var.get())
                self.srv = SocketServer(ip,port,self.add_msg_log,self.control_treev)
                self.srv.run()
                if self.srv.err == False:
                    self.gui.server_btn.config(text="stop")
                    self.gui.ip_entry.config(state="disabled")
                    self.gui.port_entry.config(state="disabled")
                    self.server_btn_active = True

            elif self.server_btn_active == True:
                self.srv.stop()
                self.gui.server_btn.config(text="init")
                self.gui.ip_entry.config(state="normal")
                self.gui.port_entry.config(state="normal")
                self.server_btn_active = False

    def init_client(self):
        if self.gui.client_check_var.get() == True and self.__input_basic_check() == True:
            if self.client_btn_active == False:
                if self.gui.user_var.get() == "username" or self.gui.user_var.get() == "":
                    self.add_msg_log("[info] -> Set-username")
                else:
                    ip = self.gui.ip_var.get()
                    port = int(self.gui.port_var.get())
                    usr = self.gui.user_var.get()
                    self.clnt = SocketClient(ip,port,self.add_msg_log,usr)
                    self.clnt.run()
                    if self.clnt.err == False:
                        self.gui.client_btn.config(text="stop")
                        self.gui.user_entry.config(state="disabled")
                        self.gui.user_set.config(text=self.clnt.user)
                        self.client_btn_active = True

            elif self.client_btn_active == True:
                self.clnt.stop()
                self.gui.client_btn.config(text="init")
                self.gui.user_entry.config(state="normal")
                self.gui.user_set.config(text="@user")
                self.client_btn_active = False

    def sendmsg(self):
        try:
            msg = self.gui.msg_var.get()
            self.clnt.send_to_srv(msg)
        except:
            self.add_msg_log("[Errno 404] -> No-connected")
        finally:
            self.gui.msg_var.set("")

    def add_msg_log(self,message,logger=False,sound=False):
        if type(message) == bytes:
            message = message.decode()
        self.gui.cuadrotexto.config(state="normal")
        self.gui.cuadrotexto.insert("end",message + "\n")
        self.gui.cuadrotexto.config(state="disabled")
        self.gui.cuadrotexto.see("end")
        if logger == True:
            self.__write_logs(message)
        if sound == True:
            self.__sound()


    def control_treev(self,user,ip,port,hostname,opt):
        if opt == "add":
            tmp = self.gui.treev.insert("","end",text=user)
            self.gui.treev.insert(tmp,"end",text=hostname)
            self.gui.treev.insert(tmp,"end",text=ip)
            self.gui.treev.insert(tmp,"end",text=str(port))
            self.tree_dict[user] = tmp
        elif opt == "del":
            self.gui.treev.delete(self.tree_dict[user])
            self.tree_dict.pop(user)

# TODO:
# no se como liberar el puerto despues de cerrar el socket "TIME_WAIT" (no pasa en windows)
def main():
    app = Controller()
if __name__ == "__main__":
    main()
