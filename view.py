import tkinter
from tkinter import ttk

class View(tkinter.Frame):
    def __init__(self,master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.widgets()

    def widgets(self):
        self.config(bd=8,bg="#9aaab9")
        frame1 = tkinter.Frame(self,bg="#9aaab9")
        frame1.grid(row=1,column=1)

        frame1_sub1 = tkinter.Frame(frame1,bd=3,relief="ridge")
        frame1_sub1.grid(row=1,column=1,pady=3,padx=5)
        frame1_sub2 = tkinter.Frame(frame1,bd=3,relief="ridge")
        frame1_sub2.grid(row=2,column=1,pady=3)
        frame1_sub3 = tkinter.Frame(frame1,bd=3,relief="ridge")
        frame1_sub3.grid(row=3,column=1,pady=3)

        frame2 = tkinter.Frame(self,bg="#9aaab9")
        frame2.grid(row=1,column=2,rowspan=40)

        frame3 = tkinter.Frame(self)
        frame3.grid(row=2,column=1,rowspan=39)
        #---frame1---#
        self.ip_label = tkinter.Label(frame1_sub1,text="IP:")
        self.ip_label.grid(row=1,column=1,padx=5,pady=2)
        self.ip_var = tkinter.StringVar()
        self.ip_entry = tkinter.Entry(frame1_sub1,textvariable=self.ip_var,width=16,font=20)
        self.ip_entry.grid(row=1,column=2,sticky="w",padx=5,pady=2)

        self.port_label = tkinter.Label(frame1_sub1,text="PORT:")
        self.port_label.grid(row=2,column=1,padx=5,pady=2)
        self.port_var = tkinter.StringVar()
        self.port_entry = tkinter.Entry(frame1_sub1,textvariable=self.port_var,width=7,font=20)
        self.port_entry.grid(row=2,column=2,sticky="w",padx=5,pady=2)

        self.server_check_var = tkinter.BooleanVar()
        self.server_check = tkinter.Checkbutton(frame1_sub2,text="SERVER")
        self.server_check.config(variable=self.server_check_var,onvalue=True,offvalue=False)
        self.server_check.grid(row=3,column=1,sticky="w",padx=5,pady=2)
        self.server_btn = tkinter.Button(frame1_sub2,text="init")
        self.server_btn.grid(row=3,column=2,sticky="w",padx=5,pady=2)

        self.client_check_var = tkinter.BooleanVar()
        self.client_check = tkinter.Checkbutton(frame1_sub2,text="CLIENT")
        self.client_check.config(variable=self.client_check_var,onvalue=True,offvalue=False)
        self.client_check.grid(row=4,column=1,sticky="w",padx=5,pady=2)
        self.client_btn = tkinter.Button(frame1_sub2,text="init")
        self.client_btn.grid(row=4,column=2,sticky="w",padx=5,pady=2)

        self.user_label = tkinter.Label(frame1_sub3,text="user:")
        self.user_label.grid(row=5,column=1,padx=5,pady=2)
        self.user_var = tkinter.StringVar()
        self.user_entry = tkinter.Entry(frame1_sub3,textvariable=self.user_var,width=12,font=20)
        self.user_entry.grid(row=5,column=2,sticky="w",padx=5,pady=2)
        #---frame2---#
        self.cuadrotexto = tkinter.Text(frame2,state="disabled",width=60,height=20,font=20)
        self.cuadrotexto.grid(row=1,column=1,columnspan=3)

        self.scroll_y = tkinter.Scrollbar(frame2,comman=self.cuadrotexto.yview)
        self.scroll_y.grid(row=1,column=4,sticky="nsew")
        self.cuadrotexto.config(yscrollcommand=self.scroll_y.set)

        self.user_set = tkinter.Label(frame2,text="[username]",width=20)
        self.user_set.grid(row=2,column=1)

        self.msg_var = tkinter.StringVar()
        self.msg_entry = tkinter.Entry(frame2,textvariable=self.msg_var,width=30,font=20)
        self.msg_entry.grid(row=2,column=2)

        self.msg_send_btn = tkinter.Button(frame2,text="send",bg="#7099fc")
        self.msg_send_btn.grid(row=2,column=3)
        #---frame3---#
        self.treev = ttk.Treeview(frame3)
        self.treev.pack()


def main():
    root = tkinter.Tk()
    window = View(root)
    window.mainloop()


if __name__ == "__main__":
    main()
