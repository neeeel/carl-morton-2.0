__author__ = 'neil'

import win32com.client


class betdaqManager():

    def __init__(self):
        self.betNumber = 1
        fh = open("betdaqBets.txt","w") # clear the bet text file
        fh.close()

    def placeBet(self,horse,betType,odds,stake,fillOrKill):
        if self.betNumber ==1:
            fh = open("betdaqBets.txt","w")
            fh.close()
        fh = open("betdaqBets.txt","a")
        fh.write(str(self.betNumber) + "," + betType + "," +  horse + "," + str(odds) + "," + str(stake) + "," + str(fillOrKill) + "\n")
        print("placing betdaq bet on" + horse + " at " + str(odds) + " for " + str(stake))
        self.betNumber +=1
        fh.close()

    def changeMarket(self,market):
        self.betNumber = 1
        market = market.strip()
        fh = open("betdaqBets.txt","w")
        fh.close()
        if market == "":
            return
        if market.lower() == "no market":
            return
        print("market is ",market)
        temp = market.split(" ")
        course = temp[0].strip()
        temp = market.split("-")[1].strip()
        raceTime = temp.split(" ")[0].strip()
        print("new market",course,raceTime)
        fh =open("betdaqBets.txt","w")
        msg  = str("change," + str(course) + "," + str(raceTime) + "\n")
        fh.write(msg)
        fh.close

#test
#bd = betdaqManager()
#ba = win32com.client.Dispatch("BettingAssistantCom.Application.ComClass")
#print(ba.marketname)

#bd.changeMarket(ba.marketname)
#bd.placeBet("clayton","B",100,0.1)
