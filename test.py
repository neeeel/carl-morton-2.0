__author__ = 'neil'

import window,texttospeech,decimal,betthread,time,myserversocket,threading,clientsocket
import win32com.client,inputbox
import logging
import speechrecognition



def get_IP():
    global ip_address
    #print("bleh  "  + ip_address)
    w = inputbox.inputBox(ip_address)
    ip_address = w.get_ip()

def keyPress(event):
    global highLow,fav,repeat,selection,w,selectedClothNo
    keymap = w.getKeyMap()
    key = str(event.char)

    print (w.getEdit())
    if clientSocket == None:
        return
    w.disableEntries()
    print(key)
    if key in keymap.keys():
        logging.info( "On client,pressed %s which is key %s in the keymap"  ,repr(event.char),keymap[key])
        if keymap[key] == "0": #fav selected
            sel = rank_runners(1)
            if len(sel) == 0:
                return
            selection = sel[0]
            selectedClothNo = ba.getsaddlecloth(selection)
            logging.info("fav key pressed, selection set to %s , cloth no set to %i",selection,selectedClothNo)
            tts.keyPressed(keymap[key],selectedClothNo)
        if keymap[key] == "1": #second fav selected
            sel = rank_runners(2)
            if len(sel) == 0:
                return
            selection = sel[0]
            selectedClothNo = ba.getsaddlecloth(selection)
            logging.info("2nd fav key pressed, selection set to %s, cloth no set to %i",selection,selectedClothNo)
            tts.keyPressed(keymap[key],selectedClothNo)
        if int(keymap[key]) >=2 and int(keymap[key]) <=4: #BACK BETS
            if selectedClothNo == 0:
                return
            bet = int(keymap[key]) -2 # bet is keeping track of whether the bet is Back 1, Back 2, or Back3, 0 is back1, 1 is back2 ,etc
            betSettings = w.getClientBetSettings()
            selection = getNameFromSaddlecloth(selectedClothNo)
            odds = float(betSettings[bet *2])
            stake = float(betSettings[(bet *2) +1])
            if betSettings[12]!="":
                fillOrKill = int(betSettings[12])
            else:
                fillOrKill = 0
            my_bet_thread.add_bet(selection,odds,stake,fillOrKill,"B")
            msg = "horse:" + str(selection + "," + str(odds) + "," + str(stake) + "," +str("B") + "," + str(bet))
            logging.info("trying to send bet to remote server %s " , msg)
            clientSocket.addToQueue(msg)
        if int(keymap[key]) >=5 and int(keymap[key]) <=7: # LAY BETS
            if selectedClothNo == 0:
                return
            bet = int(keymap[key]) -2 # bet is keeping track of whehter the bet is Lay 1, Lay 2, or Lay 3
            betSettings = w.getClientBetSettings()
            selection = getNameFromSaddlecloth(selectedClothNo)
            odds = float(betSettings[bet *2])
            stake = float(betSettings[(bet *2) +1])
            fillOrKill = 0
            if betSettings[12]!="":
                fillOrKill = int(betSettings[12])
            else:
                fillOrKill = 0
            my_bet_thread.add_bet(selection,odds,stake,fillOrKill,"L")
            msg = "horse:" + str(selection + "," + str(odds) + "," + str(stake) + "," +str("L") + "," + str(bet))
            logging.info("trying to send bet to remote server %s" , msg)
            clientSocket.addToQueue(msg)
        if int(keymap[key]) ==8:
            tts.speakCurrentPrice()
        if int(keymap[key]) ==9:
            speakProfit()
        if int(keymap[key]) ==10:
            incrementClothNo()
            logging.info("incremented cloth no to %i",selectedClothNo)
            tts.keyPressed(keymap[key],selectedClothNo)
        if int(keymap[key]) ==11:
            decrementClothNo()
            logging.info("decremented cloth no to %i ",selectedClothNo)
            tts.keyPressed(keymap[key],selectedClothNo)

def monitorMarketChange():
    global selectedClothNo,current_market,ba,tts,botOn
    while botOn:
        m = ba.marketID
        #print(str(m) + " " +  str(current_market))
        if m !=current_market:
            selectedClothNo = 0
            logging.info("market change detected in monitorMarketChange, new market is %s",str(m))
            tts.reset()
            current_market = ba.marketid
        time.sleep(1)

def incrementClothNo():
    global ba,selection,selectedClothNo

    price_list = []
    prices = ba.getprices
    for p in prices:
        price_list.append((p.selection, ba.getsaddlecloth(p.selection)))
    price_list = sorted(price_list, key=lambda p: (p[1]))
    selectedClothNo+=1
    price_list = price_list[::-1]
    if price_list[0][1] < selectedClothNo:
        selectedClothNo = price_list[0][1]
    print("selected cloth no is",selectedClothNo)
    print("in test, incrementing cloth no to",selectedClothNo)

def decrementClothNo():
    global ba,selection,selectedClothNo
    price_list = []
    prices = ba.getprices
    for p in prices:
        price_list.append((p.selection, ba.getsaddlecloth(p.selection)))
    price_list = sorted(price_list, key=lambda p: (p[1]))
    selectedClothNo-=1
    if price_list[0][1] > selectedClothNo:
        selectedClothNo = price_list[0][1]
    print("selected cloth no is",selectedClothNo)

def speakProfit():
    global tts
    global ba
    global repeat, botOn
    if selectedClothNo == 0:
        return ""
    selection = getNameFromSaddlecloth(selectedClothNo)
    prices = ba.getprices
    for p in prices:
        if p.selection == selection:
            total = p.liability
    total = float("%.2f" % float(total))
    tts.talk(str(total))

def talk(s):
    global speaker
    global tts
    tts.set_text(s)
    tts.speak()

def getNameFromSaddlecloth(clothNo):
    prices = ba.getprices
    for p in prices:
        if p == None:
            return ""
        else:
            cloth = ba.getsaddlecloth(p.selection)
            if cloth == clothNo:
                return p.selection
    return ""

def get_index(horse):
    index = 0
    prices = ba.getprices
    for p in prices:
        if p.selection.lower() == horse.lower():
            return index
        index += 1
    return -1

def rank_runners(rnk):
    global ba
    price_list = []
    count = 0
    prices = ba.getprices
    if prices == None:
        return ()
    for p in prices:
        price_list.append((p.selection, p.backodds1, p.totalmatched))
    price_list = sorted(price_list, key=lambda p: (p[1], -p[2]))
    return price_list[rnk - 1]

def on_closing():
    global local_bet_thread_flag,ip_address,botOn,tts
    logging.info("window closed, shutting down all threads and services")
    if clientSocket != None:
        clientSocket.stop_client()
        logging.info("Stopping client thread")
    botOn = False
    w.saveSettings(ip_address)
    my_bet_thread.close()
    logging.info("Stopping bet thread")
    stop_server()
    logging.info("Stopping server thread")
    if tts !=None:
        tts.kill()
    w.destroy()

def start_server():
    #statuslabel.configure(text="Listening", fg="green")
    global serversocket, my_bet_thread,w
    logging.info("Starting up server")
    serversocket = myserversocket.myServerSocket(my_bet_thread)
    serversocket.setWindow(w)
    serversocket.bind(('', 5554))
    serversocket.listen(5)
    logging.info("Server listening")

def stop_server():
    global server_thread, server_started
    global serversocket
    server_started = False
    logging.info("Stopping server")
    if serversocket is None:
        print("server not connected")
    else:
        print("server Disconnected by user")
        serversocket.close_connection()
        serversocket = None
        if not server_thread is None:
            server_thread.join()
            server_thread = None
    logging.info("Server stopped")

def temp():
    global server_started
    if server_started ==False:
        server_started = True
        server_thread = threading.Thread(target=start_server, args=())
        server_thread.daemon = True
        server_thread.start()

def speakPrice():
    global selection,fav
    global ba
    global repeat, botOn,current_market
    prices = ba.getprices
    if current_market != ba.marketid:
        current_market = ba.marketid
        fav= ""
        selection = ""
        return
    if botOn:
        for p in prices:
            if p == None:
                return
            if p.selection == selection:
                talk(str(p.backodds1))
        print("resetting timer")
        if not repeat is None:
            repeat.cancel()
            print("cancelling timer")
        repeat = threading.Timer(3.5, speakPrice)
        repeat.start()

def start_client():
    global ip_address,clientSocket,w,botOn,fav, selection,tts,selectedClothNo,processSaddleclothQueue

    print("is client socket set to NONE " ,clientSocket == None)
    if clientSocket != None:
        print("is client socket alive? " ,clientSocket.isAlive())
        if not clientSocket.isAlive():
            clientSocket  = None
    if not botOn:
        logging.info("Starting up client")
        if clientSocket == None:
            tts = texttospeech.TTS()
            processSaddleclothQueue = True
            process_change_of_saddlecloth_queue()

            logging.info("Started tts thread")
            clientSocket = clientsocket.ClientSocket()
            logging.info("started client socket")
            clientSocket.setWindow(w)
            clientSocket.start_client(ip_address)
            botOn = True
            t = threading.Thread(target = monitorMarketChange)
            t.start()
            fav = ""
            selection = ""
            w.disableEntries()
            w.client_running(True)
            selectedClothNo = 0

def stop_client():
    global clientSocket,botOn,tts,selectedClothNo
    botOn = False
    selectedClothNo = 0
    if clientSocket != None:
        logging.info("Client stopped")
        clientSocket.stop_client()
        clientSocket = None
        w.enableEntries()
        w.client_running(False)
        stop_processing_change_of_saddlecloth_queue()
        tts.kill()
        tts = None

def start_speechrecognition_thread():
    global speechrecognitionThread
    if speechrecognitionThread is None:
        speechrecognitionThread = threading.Thread(target=speechrecognition.speech_recognition_thread)
        speechrecognitionThread.daemon = True
        speechrecognitionThread.start()


def stop_speechrecognition_thread():
    global speechrecognitionThread
    speechrecognition.stop_speech_recognition_thread()
    speechrecognitionThread = None

def process_change_of_saddlecloth_queue():
    global selectedClothNo
    if processSaddleclothQueue == True:
        #print("checking saddlecloth queue")
        next = speechrecognition.get_next_saddlecloth_selection()
        #print("next spoken saddlecloth is",next)
        if next != "":
            if not tts is None:
                selectedClothNo = next
                tts.change_selection_via_speech(next)
        threading.Timer(0.1, process_change_of_saddlecloth_queue).start()

def stop_processing_change_of_saddlecloth_queue():
    global processSaddleclothQueue
    processSaddleclothQueue = False

def logIn():
    x = inputbox.loginBox(w)


keymap = []
processSaddleclothQueue = False
highLow = "low"
ip_address = ""
client_connected = False
server_listening = False
running = False
fav = ""
selection = ""
selectedClothNo = 0
botOn = False
server_started = False
server_thread = None
serversocket = None
clientSocket = None
repeat = None
tts = None
logging.basicConfig(level=logging.INFO,filename = "log.txt",format='%(asctime)s %(message)s' , datefmt='%m/%d/%Y %I:%M:%S %p')
#ba = win32com.client.Dispatch("BettingAssistantCom.Application.ComClass")
ba =win32com.client.dynamic.Dispatch("BettingAssistantCom.Application.ComClass")
w = window.Window()
current_market = ba.marketid
settings = w.getClientBetSettings()
my_bet_thread = betthread.betThread()
speechrecognitionThread = None
w.bind("<Key>",keyPress)
ip_address = w.loadSettings()
print("loaded ip address " ,ip_address)
w.protocol("WM_DELETE_WINDOW", on_closing)
w.bindServerFunctions("Listen",temp)
w.bindServerFunctions("Stop",stop_server)
w.bindClientFunctions("Connect",start_client)
w.bindClientFunctions("Stop",stop_client)
w.bindClientFunctions("Enter",get_IP)
w.bindClientFunctions("Log In",logIn)
start_speechrecognition_thread()
w.mainloop()