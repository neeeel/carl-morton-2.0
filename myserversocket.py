__author__ = 'neil'

import socket
import threading
import win32com.client
import decimal
import pythoncom
import time,betdaq
import logging


class myServerSocket(socket.socket):
    def __init__(self,betThread):
        pythoncom.CoInitialize()
        self.ba = win32com.client.Dispatch("BettingAssistantCom.Application.ComClass")
        self.clients = []
        super(myServerSocket, self).__init__(socket.AF_INET, socket.SOCK_STREAM)
        self.index  = -1
        self.betType = "B"
        self.odds = 0.0
        self.stake = 0.0
        self.betThread = betThread
        self.isAlive = False
        self.currentmarket  = ""
        self.currentBetdaqMarket = ""
        self.w = None
        self.bd = betdaq.betdaqManager()

    def listen(self, max):
        super(myServerSocket, self).listen(1)
        self.isAlive = True
        print("listening")
        self.w.setServerMessage("Listening","green")
        while self.isAlive:
            try:
                client, address = self.accept()
            except Exception as e:
                self.w.setServerMessage("Not Listening","red")
                logging.info("Server: error while listening , error message", exc_info=True)
                break
            self.clients.append(client)
            logging.info("Server: new connection made, address is %s ",str(address[0]))
            t = threading.Thread(target=self.deal_with_client, args= (client,))
            t.start()
            logging.info("Server: started new deal with client thread")

    def stop_server(self):
        self.isAlive = False
        logging.info("Server: closing down server")
        for c in self.clients:
            c.close()

        self.w.setServerMessage("Not Listening","red")

    def isAlive(self):
        return self.isAlive

    def close_connection(self):
        print("closing server down")
        for c in self.clients:
            c.close()
        self.w.setServerMessage("Not Listening","red")
        self.close()

    def setWindow(self,w):
        self.w = w

    def deal_with_client(self,client):
        while True:
            try:
                client.settimeout(10.0)
                print("listening to client")
                data = client.recv(2)
                if not data:
                    logging.info("Server: connection dropped by client ")
                    client.close()
                    client = None
                    return
                length = str(data.decode())
            except ConnectionResetError as e:
                logging.info("connection forcibly closed by client ")
                client.close()
                client = None
                return
            except ConnectionAbortedError as e:
                logging.info("connection aborted  ")
                client.close()
                client = None
                return
            except socket.timeout:
                logging.info("socket timed out without receiving any data")
                client.close()
                client = None
                return
            except OSError as e:
                logging.info("socket is closed, not a socket, closing connection")
                client.close()
                client = None
                return
            if length == '':
                return

            MSGLEN = int(length)
            chunks = []
            received = 0
            while received < MSGLEN:
                try:
                    client.settimeout(10)
                    chunk  = str(client.recv(min(MSGLEN - received, 2048)).decode())
                except ConnectionResetError as e:
                    logging.info("connection forcibly closed by client")
                    client.close()
                    return
                except ConnectionAbortedError as e:
                    logging.info("connection aborted")
                    client.close()
                    return
                except socket.timeout:
                    logging.info("socket timed out without receiving any data")
                    client.close()
                    return
                if chunk == '':
                    print("no data received after 10 seconds")
                    return
                chunks.append(chunk)
                received +=  len(chunk)
            data = "".join(chunks)

            msg = data.split(",")

            #print ("number of splits " + str(len(msg)))
            if msg[0] == "change":
                logging.info("Server: message received from client %s",msg)
                logging.info("Server: received change market message, new market is" + str(msg[1]))
                if self.currentmarket != str(msg[1]):
                    #self.ba.openmarket(msg[1],1)
                    self.currentmarket = str(msg[1])
                if self.currentBetdaqMarket != str(msg[2]):
                    self.bd.changeMarket(str(msg[2]))
                    self.currentBetdaqMarket = str(msg[2])
            elif  msg[0] == "PING":
                pass
            elif "horse:" in msg[0]:
                logging.info("Server: message received from client %s",msg)
                horse = msg[0]
                index = horse.find(":")
                horse = horse[index+1:]
                betType = str(msg[3])
                betNo = int(msg[4])
                settings = self.w.getServerBetSettings()
                odds = float(settings[0 +  (2 * betNo)])
                stake = float(settings[1+  (2 * betNo) ])
                betdaqOdds = float(settings[12 +  (2 * betNo)])
                betdaqStake = float(settings[13 +  (2 * betNo)])
                logging.info("Server: received remote bet %s %f %f %s %i %f %f",horse,odds,stake,betType,betNo,betdaqOdds,betdaqStake)
                fillOrKill = 0
                if settings[2] !="":
                    fillOrKill = int(settings[24])
                self.betThread.add_bet(horse,odds,stake,fillOrKill,betType)
                self.bd.placeBet(horse,betType,betdaqOdds,betdaqStake,fillOrKill)
        client.close()

    def place_bet(self):
        result = self.ba.placebet(self.index,self.betType,self.odds,self.stake)
        self.betThread.add_bet((result,time.time()))

def plusTicks(odds,ticks):
    o = odds
    if odds == 0 or odds == 1000:
        return odds
    for i in range(0,ticks):
        o = getNextOdds(o)
    return o

def getNextOdds(odds):
        oddsInc = 0.0
        if odds >=1 and odds <=1.99:
            oddsInc = 0.01
        if odds >=2 and odds <=2.98:
            oddsInc = 0.02
        if odds >=3 and odds <=3.95:
            oddsInc = 0.05
        if odds >=4 and odds <=5.9:
            oddsInc = 0.1
        if odds >=6 and odds <=9.8:
            oddsInc = 0.2
        if odds >=10 and odds <=19.5:
            oddsInc = 0.5
        if odds >=20 and odds <=29:
            oddsInc = 1
        if odds >=30 and odds <=48:
            oddsInc = 2
        if odds >=50 and odds <=95:
            oddsInc = 5
        if odds >=100 and odds <1000:
            oddsInc = 10
        odds = odds + oddsInc
        return round(odds,2)

