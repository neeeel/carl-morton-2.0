__author__ = 'neil'

from tkinter import *
from tkinter import ttk
from tkinter import font
import threading
import speechrecognition


class Window(Tk):
    def __init__(self):
        super().__init__()
        self.note = ttk.Notebook(self)
        self.tab1 = Frame(self.note)
        self.tab2 = Frame(self.note)
        self.tab3 = Frame(self.note)
        self.clientEntryValues = []
        self.serverEntryValues = []
        self.messageLabel = None
        self.edit = IntVar()
        self.buildClient()
        self.buildServer()
        self.loadSettings()
        self.build_mic_settings()
        self.note.add(self.tab1, text = "Settings")
        self.note.add(self.tab2, text = "Client")
        self.note.add(self.tab3, text = "Mic Settings")
        self.note.bind_all("<<NotebookTabChanged>>", self.tabChanged)
        self.note.pack()
        #self.loadSettings()
        self.note.select(1)
        self.micTestFlag = False
        self.clientRunning = False ### indicates that the client is running, so that if we are on the mic settings, we dont consume any saddlecloth numbers


    def client_running(self,val):
        self.clientRunning = val

    def tabChanged(self,event):
        if self.note.index(self.note.select()) == 0:
            self.micTestFlag = False
        if self.note.index(self.note.select()) == 1:
            self.hideSettings()
            self.micTestFlag = False
            speechrecognition.clear_saddlecloth_queue()
        if self.note.index(self.note.select()) == 2:
            self.hideSettings()
            self.toggle_mic_test()

    def buildServer(self):
        startButton = Button(self.tab1,text = "Listen",command = self.getIncrements )
        stopButton = Button(self.tab1,text = "Stop")
        self.messageLabel = Label(self.tab1,text = "Not Listening",fg="red")
        labels = []
        entries = []
        vars = []
        for i in range(0,12):
            lbl = Label(self.tab1,font = "Times 8")
            var = StringVar()
            entry = Entry(self.tab1,textvariable = var,width = 5,justify = CENTER)
            labels.append(lbl)
            entries.append(entry)
            self.serverEntryValues.append(var)
            lbl.grid(row = i + 3,column = 0 ,pady=5, padx=5)
            entry.grid(row = i + 3,column =1 ,pady=5, padx=5)
            lbl = Label(self.tab1,font = "Times 8")
            var = StringVar()
            entry = Entry(self.tab1,textvariable = var,width = 5,justify = CENTER)
            labels.append(lbl)
            entries.append(entry)
            self.serverEntryValues.append(var)
            lbl.grid(row = i + 3,column = 2 ,pady=5, padx=5)
            entry.grid(row = i + 3,column =3 ,pady=5, padx=5)
        labels[0].configure(text ="Betfair Back Odds 1")
        labels[2].configure(text ="Betfair Back Stake 1")
        labels[4].configure(text ="Betfair Back Odds 2")
        labels[6].configure(text ="Betfair Back Stake 2")
        labels[8].configure(text ="Betfair Back Odds 3")
        labels[10].configure(text ="Betfair Back Stake 3")#
        labels[12].configure(text ="Betfair Lay Odds 1")
        labels[14].configure(text ="Betfair Lay Stake 1")
        labels[16].configure(text ="Betfair Lay Odds 2")
        labels[18].configure(text ="Betfair Lay Stake 2")
        labels[20].configure(text ="Betfair Lay Odds 3")
        labels[22].configure(text ="Betfair Lay Stake 3")
        labels[1].configure(text ="Betdaq Back Odds 1")
        labels[3].configure(text ="Betdaq Back Stake 1")
        labels[5].configure(text ="Betdaq Back Odds 2")
        labels[7].configure(text ="Betdaq Back Stake 2")
        labels[9].configure(text ="Betdaq Back Odds 3")
        labels[11].configure(text ="Betdaq Back Stake 3")#
        labels[13].configure(text ="Betdaq Lay Odds 1")
        labels[15].configure(text ="Betdaq Lay Stake 1")
        labels[17].configure(text ="Betdaq Lay Odds 2")
        labels[19].configure(text ="Betdaq Lay Stake 2")
        labels[21].configure(text ="Betdaq Lay Odds 3")
        labels[23].configure(text ="Betdaq Lay Stake 3")
        var = StringVar()
        fillOrKillLabel = Label(self.tab1, text = "Fill or Kill")
        fillOrKillEntry = Entry(self.tab1,textvariable = var,width = 5,justify = CENTER)
        self.serverEntryValues.append(var)
        self.messageLabel.grid(row = 0,column = 0, columnspan = 3,pady=5, padx=5, sticky=N)
        startButton.grid(row =1,column = 0,pady=5, padx=5 )
        stopButton.grid(row =1,column = 1,pady=5, padx=5)
        fillOrKillLabel.grid(row =2,column = 0,pady=5, padx=5, sticky=W)
        fillOrKillEntry.grid(row =2,column = 1,pady=5, padx=5, sticky=W)
        self.tab1.pack()
        self.hideSettings()

    def buildClient(self):
        labels  = []
        entries = []
        connectButton = Button(self.tab2,text = "Connect" )
        stopButton = Button(self.tab2,text = "Stop")
        enterButton = Button(self.tab2,text = "Enter")
        loginButton = Button(self.tab2,text = "Log In")
        messageLabel = Label(self.tab2,text = "Not Connected",fg="red")
        messageLabel.grid(row = 0,column = 0, columnspan = 3,pady=10, padx=10, sticky=N)
        connectButton.grid(row =1,column = 0,pady=10, padx=10 )
        stopButton.grid(row =1,column = 1,pady=10, padx=10)
        enterButton.grid(row =1,column = 2,pady=10, padx=10)
        loginButton.grid(row =1,column = 3,pady=10, padx=10)
        for i in range(0,12):
            lbl = Label(self.tab2)
            var = StringVar()
            entry = Entry(self.tab2,textvariable = var,width = 5,justify = CENTER)
            labels.append(lbl)
            entries.append(entry)
            self.clientEntryValues.append(var)
            lbl.grid(row = i + 3,column = 0 ,pady=10, padx=10)
            entry.grid(row = i + 3,column =1 ,pady=10, padx=10)
            lbl = Label(self.tab2)
            var = StringVar()
            entry = Entry(self.tab2,textvariable = var,width = 5,justify = CENTER)
            labels.append(lbl)
            entries.append(entry)
            self.clientEntryValues.append(var)
            lbl.grid(row = i + 3,column = 2 ,pady=10, padx=10)
            entry.grid(row = i + 3,column =3 ,pady=10, padx=10)
        lbl = Label(self.tab2) # because we have a single entry box at the bottom of the window
        var = StringVar()
        entry = Entry(self.tab2,textvariable = var,width = 6)
        labels.append(lbl)
        entries.append(entry)
        lbl.grid(row = 123,column = 0 ,pady=10, padx=10)
        entry.grid(row = 123,column =1 ,pady=10, padx=10)
        self.clientEntryValues.append(var)
        labels[0].configure(text ="Select Fav")
        labels[2].configure(text ="Select 2nd Fav")
        labels[4].configure(text ="Back at Odds 1 for Stake 1")
        labels[6].configure(text ="Back at Odds 2 for Stake 2")
        labels[8].configure(text ="Back at Odds 3 for Stake 3")
        labels[10].configure(text ="Lay at Odds 1 for Stake 1")
        labels[12].configure(text ="Lay at Odds 2 for Stake 2")
        labels[14].configure(text ="Lay at Odds 3 for Stake 3")
        labels[1].configure(text ="Back Odds 1")
        labels[3].configure(text ="Back Stake 1")
        labels[5].configure(text ="Back Odds 2")
        labels[7].configure(text ="Back Stake 2")
        labels[9].configure(text ="Back Odds 3")
        labels[11].configure(text ="Back Stake 3")#
        labels[13].configure(text ="Lay Odds 1")
        labels[15].configure(text ="Lay Stake 1")
        labels[17].configure(text ="Lay Odds 2")
        labels[19].configure(text ="Lay Stake 2")
        labels[21].configure(text ="Lay Odds 3")
        labels[23].configure(text ="Lay Stake 3")
        labels[16].configure(text = "Give Current Price")
        labels[18].configure(text = "Say PnL")
        labels[20].configure(text = "Saddlecloth Up")
        labels[22].configure(text = "Saddlecloth Down")
        labels[24].configure(text = "Fill Or Kill")
        self.tab2.pack()
        print (len(self.clientEntryValues))

    def build_mic_settings(self):
        f = font.Font(family="Times New Roman", size=30,weight="bold")
        settings = speechrecognition.get_recogniser_settings()
        print("settings are")
        Label(self.tab3,text="Vol. Threshold").grid(row=0,column=0)
        w = Scale(self.tab3, from_=0, to=1000, orient=HORIZONTAL,resolution = 10,length = 250)
        w.grid(row=0,column=1)
        w.set(settings[0])
        print("setting 0",w.get())
        w.config(command= lambda x:self.mic_settings_changed(x,1))
        Label(self.tab3,text="End Of Phrase Quiet Length").grid(row=1,column=0)
        w = Scale(self.tab3, from_=0, to=1, orient=HORIZONTAL,resolution = 0.01,length = 250)
        w.grid(row=1,column=1)
        w.set(settings[1])
        print("setting 1",w.get())
        w.config(command= lambda x:self.mic_settings_changed(x,2))
        Label(self.tab3,text="Min Audio Length").grid(row=2,column=0)
        w = Scale(self.tab3, from_=0, to=1, orient=HORIZONTAL,resolution = 0.01,length = 250)
        w.grid(row=2,column=1)
        w.set(settings[2])
        print("setting 2",w.get())
        w.config(command= lambda x:self.mic_settings_changed(x,3))
        Button(self.tab3,text="Test",command=self.toggle_mic_test).grid(row=3,column=0,columnspan=2)
        self.resultLabel = Label(self.tab3,text="0",relief=GROOVE,borderwidth=2,font =f)
        s = ttk.Style()
        s.theme_use('clam')
        s.configure("red.Horizontal.TProgressbar", foreground='red', background='red')
        self.pb = ttk.Progressbar(self.tab3, style="red.Horizontal.TProgressbar", orient="horizontal", length=200)
        self.pb["maximum"]= 600
        self.pb.grid(row=5,column=0,columnspan = 2)

        self.resultLabel.grid(row=4,column=0,columnspan=2)

    def mic_settings_changed(self,event,index):
        print(event,index)
        settings = []
        #if index == 1:
            #self.pb["maximum"] = 2 * event
        for child in self.tab3.winfo_children():
            if type(child)== Scale:
                print(child.get())
                settings.append(child.get())
        speechrecognition.set_recogniser_settings(settings)
        self.saveSettings(self.ip_address)

    def toggle_mic_test(self):
        if self.micTestFlag == False:
            self.micTestFlag = True
            self.mic_test()
        else:
            self.micTestFlag = False

    def mic_test(self):
        if self.micTestFlag == True:
            consume = True
            #print(speechrecognition.get_microphone_energy())
            energy = speechrecognition.get_microphone_energy()
            s = ttk.Style()
            s.theme_use('clam')
            if energy > self.tab3.winfo_children()[1].get():
                s.configure("red.Horizontal.TProgressbar", foreground='green', background='green')
            else:
                s.configure("red.Horizontal.TProgressbar", foreground='red', background='red')
            if self.clientRunning == True:
                consume = False
            self.pb["value"] = energy
            next = speechrecognition.get_next_saddlecloth_selection(consume=consume)

            if next != "":
                print("next is",next)
                self.resultLabel.config(text=next)
            self.after(100,self.mic_test)

    def getClientBetSettings(self):
        l = []
        for i in range(0,25):
            if i%2 ==1:
                l.append(self.clientEntryValues[i].get())
        l.append(self.clientEntryValues[24].get())
        #l.append(self.placeRemoteBet.get())
        #l.append(self.enableBetdaq.get())
        return l

    def getServerBetSettings(self):
        l = []
        for i in range(0,24,2):
                l.append(self.serverEntryValues[i].get())
        for i in range(1,24,2):
                l.append(self.serverEntryValues[i].get())
        l.append(self.clientEntryValues[24].get())
        print(l)
        return l

    def getEdit(self):
        return self.edit.get()

    def loadSettings(self):
        print("no of entry boxes",len(self.clientEntryValues))
        with open('settings.txt', 'r') as f:
            count = 0
            for e in self.clientEntryValues:
                text = f.readline()
                text = text.replace("\n", "")
                print("read",text)
                e.set(text)
                count += 1
            self.ip_address = f.readline().replace("\n", "")
            recognizer_settings = [float(f.readline().replace("\n", "")) for i in range(3)]
            print("recognizer settins are",recognizer_settings)
            speechrecognition.set_recogniser_settings(recognizer_settings)
            print("read ip add as " + self.ip_address)
        with open('serversettings.txt', 'r') as f:
            count = 0
            for e in self.serverEntryValues:
                text = f.readline()
                text = text.replace("\n", "")
                print("read",text)
                e.set(text)
        return self.ip_address

    def saveSettings(self,ip_address):
        with open('settings.txt', 'w') as f:
            for e in self.clientEntryValues:
                if e.get() == "":
                    f.write("\n")
                else:
                    f.write(e.get() + "\n")
            f.write(ip_address+ "\n")
            for v in speechrecognition.get_recogniser_settings():
                f.write(str(v) + "\n")

        with open('serversettings.txt', 'w') as f:
            for e in self.serverEntryValues:
                if e.get() == "":
                    f.write("\n")
                else:
                    f.write(e.get() + "\n")

    def getIncrements(self):
        print(self.serverEntryValues[0].get(),self.serverEntryValues[1].get())
        return(self.serverEntryValues[0].get(),self.serverEntryValues[1].get())

    def getKeyMap(self):
        l = {}
        for i in range(0,23):
            if i%2 ==0:
                l[self.clientEntryValues[i].get()] = str(int(i/2))
        return l

    def bindServerFunctions(self,name,fun):
        for i in self.tab1.winfo_children():
            if (i.config('text')[-1]) ==name:
                i.configure(command = fun)

    def bindClientFunctions(self,name,fun):
        for i in self.tab2.winfo_children():
            if (i.config('text')[-1]) ==name:
                i.configure(command = fun)

    def setClientMessage(self,msg,colour):
        widgets = self.tab2.winfo_children()
        widgets[4].configure(text=msg, fg=colour)
        print("seting message to ",msg)

    def setServerMessage(self,msg,colour):
        self.messageLabel.configure(text=msg, fg=colour)

    def setStatusMessage(self,msg,colour):
        widgets = self.tab2.winfo_children()
        widgets[5].configure(text=msg, fg=colour)

    def disableEntries(self):
        for i in self.tab2.winfo_children():
            if (type(i)) ==   Entry:
                i.configure(state = DISABLED )

    def enableEntries(self):
        for i in self.tab2.winfo_children():
            if (type(i)) ==  Entry :
                i.configure(state = NORMAL)

    def hideSettings(self):
        for i in self.tab1.winfo_children():
            i.grid_remove()

    def showSettings(self):
        for i in self.tab1.winfo_children():
            i.grid()
        self.note.select(0)


