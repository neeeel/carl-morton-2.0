__author__ = 'neil'

import socket,threading,time,win32com

class ClientSocket(threading.Thread):

    messageQueue = []
    active = True
    clientSocket = None
    lastPing = 0.0
    lastMarketCheck = 0.0
    isOpen = False
    w = None
    ba = None #win32com.client.Dispatch("BettingAssistantCom.Application.ComClass")
    currentMarket = ""

    def __init__(self):
        super().__init__()
        self.ba = win32com.client.Dispatch("BettingAssistantCom.Application.ComClass")

    def run(self):
        self.w.setClientMessage("Connected","green")
        self.addToQueue("change," + str(self.ba.marketID)+  "," + str(self.ba.marketname))
        while self.active:
            for msg in self.messageQueue:
                length = len(msg)
                if length < 10:
                    length_as_string = "0" + str(length)
                else:
                    length_as_string = str(length)
                #print("length of message string is " + length_as_string)
                if not self.clientSocket == None:
                    try:
                        self.clientSocket.send(length_as_string.encode())
                    except Exception as e:
                        print("failed to send length string ", type(e))
                        self.clientSocket.close()
                        self.isOpen = False
                        self.w.setClientMessage("Not Connected","red")
                        return
                    try:
                        #print("trying to send " , msg)
                        self.clientSocket.send(msg.encode())
                        #print("sent message ", msg)
                    except Exception as e:
                        print("failed to send message string ", type(e))
                        self.clientSocket.close()
                        self.isOpen = False
                        self.w.setClientMessage("Not Connected","red")
                        return
                else:
                    print("client not connected, failed to send message")
                    self.clientSocket.close()
                    self.isOpen = False
                    self.w.setClientMessage("Not Connected","red")
                    return
                del (self.messageQueue[0])
            if time.time()*1000 - self.lastPing*1000 > 5000:
                #print(time.time(),self.lastPing)
                self.lastPing = time.time()
                self.addToQueue("PING")
            if time.time()*1000 - self.lastMarketCheck*1000 > 1000:
                self.lastMarketCheck = time.time()
                if self.currentMarket != str(self.ba.marketID):
                    self.currentMarket = str(self.ba.marketID)
                    print("current market before sending change message ",str(self.ba.marketname))
                    self.addToQueue("change," + str(self.currentMarket) +  "," + str(self.ba.marketname))
            time.sleep(0.01)
        print("stopping clientsocket Thread")

    def start_client(self,ip_address):
        self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if len(ip_address) == 0:
            print("no IP address provided, couldnt connect")
            return False
        try:
            print("trying to connect to " + str(ip_address))
            self.clientSocket.connect((str(ip_address), 5554))
            #clientStatusLabel.configure(text="Connected", fg="green")
            #sync_market()
        except Exception as e:
            # print(e.__class__)
            # print(type(e))
            print("failed to connect to server , ", type(e))
            self.clientSocket.close()
            self.isOpen = False
            self.w.setClientMessage("Not Connected " + str(type(e)),"red")
            return
        self.start()

    def stop_client(self):
        self.active = False
        self.w.setClientMessage("Not Connected","red")
        self.clientSocket.close()

    def addToQueue(self,msg):
        self.messageQueue.append(msg)

    def setWindow(self,w):
        self.w = w