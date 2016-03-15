__author__ = 'neil'

import threading
import time,win32com

class betThread(object):

    def __init__(self):
        self.ba = win32com.client.Dispatch("BettingAssistantCom.Application.ComClass")
        self.bets = []
        self.betQueue = []
        self.currentMarketID = ""
        self.lock = threading.Lock()
        self.finish = False
        self.t = threading.Thread(target = self.process)
        self.t.start()

    def add_bet(self,horse,odds,stake,fillOrKill,betType):
        self.lock.acquire()
        print("add bet aquired lock")
        self.betQueue.append((horse,odds,stake,fillOrKill,betType))
        print("betthread received bet",betType,horse, odds, stake,self.betQueue)
        self.lock.release()
        print("add bet released lock")


    def process(self):
        while not self.finish:
            if self.currentMarketID  != self.ba.marketID:
                self.currentMarketID = self.ba.marketID
                print("setting current market ID to " ,self.currentMarketID)
            count  = 0
            self.lock.acquire()
            #print("process acquired lock")
            #print("bet queue length",len(self.betQueue))
            while len(self.betQueue) > 0:
                print("before popping, bet queue was",self.betQueue)
                bet = self.betQueue.pop(0)
                print("processing",bet,self.betQueue)
                index = self.get_index(bet[0])
                if index != -1:
                    result = self.ba.placebet(index,bet[4],bet[1],bet[2])
                    print(" in bet thread, placing bet ",bet[0], bet[1],bet[2],self.betQueue)
                    fillOrKill = int(bet[3])
                    self.bets.append((result,time.time(),fillOrKill))
                    #print("in bet thread, removing bet ",bet,self.betQueue)
                count += 1
            self.lock.release()
            #print("process released lock")
            if self.finish == True:
                break
            curr_time = time.time()
            count= 0
            for b in self.bets:
                if curr_time - float(b[1]) >= int(b[2]):
                    print("in betThread, cancelling " + str(b[0]))
                    self.ba.cancelbet(b[0])
                    del self.bets[count]
                count+=1
            time.sleep(0.01)

    def close(self):
        print("stopping bet thread")
        self.finish = True
        self.t.join
        print("stopped")

    def get_index(self,horse):
        index = 0
        prices = self.ba.getprices
        if prices == None:
            return -1
        for p in prices:
            if p.selection.lower() == horse.lower():
                return index
            index += 1
        return -1


