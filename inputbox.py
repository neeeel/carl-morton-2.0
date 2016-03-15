__author__ = 'neil'


import tkinter

class inputBox():

    def __init__(self,ip_address):
        self.ip_address = ""
        self.top = tkinter.Tk()
        e2var = tkinter.StringVar()
        self.e2var1 = tkinter.StringVar()
        e2var.set(ip_address)
        self.L1 = tkinter.Label(self.top, text="Enter IP")
        self.L2 = tkinter.Label(self.top,text = "PW")
        self.L1.grid(row = 0,column =0)
        self.L2.grid(row = 1,column =0)
        self.E1 = tkinter.Entry(self.top,textvariable=e2var, bd =5)
        self.E2 = tkinter.Entry(self.top,textvariable=self.e2var1,show="*", bd =5)
        self.B1 = tkinter.Button(self.top,text= "Go" ,command = lambda: self.press())
        self.E1.grid(row = 0,column =1)
        self.E2.grid(row = 1,column =1)
        self.B1.grid(row = 0,column =2)
        self.E1.focus_set()
        e2var.set(ip_address)

        self.top.mainloop()

    def press(self):
        if self.E2.get() =="12345":
            self.ip_address = self.E1.get()
        self.top.destroy()
        self.top.quit()

    def get_ip(self):
        return self.ip_address


class loginBox():

    def __init__(self,w):
        self.ip_address = ""
        self.top = tkinter.Tk()
        e2var = tkinter.StringVar()
        self.e2var1 = tkinter.StringVar()
        self.L2 = tkinter.Label(self.top,text = "PW")
        self.L2.grid(row = 1,column =0)
        self.E2 = tkinter.Entry(self.top,textvariable=self.e2var1,show="*", bd =5)
        self.B1 = tkinter.Button(self.top,text= "Go" ,command = lambda: self.press())
        self.E2.grid(row = 0,column =1)
        self.B1.grid(row = 0,column =2)
        self.w = w
        self.E2.focus_set()
        self.top.mainloop()


    def press(self):
        if self.E2.get() =="12345":
            self.w.showSettings()
        self.top.destroy()
        self.top.quit()