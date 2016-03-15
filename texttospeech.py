__author__ = 'neil'

import threading, win32com.client
import pythoncom
import time

# Asynchronous Text to Speech


class TTS(object):
    def __init__(self):
        self.speaker = win32com.client.Dispatch("SAPI.SpVoice")
        self.text = ""
        pythoncom.CoInitialize()
        self.previous = []
        self.queue = []
        self.allowSpeech = True
        self.selection = ""
        self.clothNo = 0
        self.selectionChanged = False
        self.keyPressedAt = time.time()
        self.lastSpokeAt = time.time()
        self.active = True
        self.ba = win32com.client.Dispatch("BettingAssistantCom.Application.ComClass")
        self.lastKeyPressed = ""
        self.t = threading.Thread(target = self.run)
        self.t.start()

    def set_text(self,text):
        self.text = text

    def keyPressed(self,key,clothNo):
        print("current cloth no is ",self.clothNo)
        if key=="0" or key== "1":
            print("in texttospeech.keypressed FAV key was pressed, new clothno is ",clothNo)
            self.clothNo = clothNo
            print("setting self.clothno to ",self.clothNo)
            print("setting last pressed key to",key)
            self.selectionChanged = True
            self.keyPressedAt = time.time()
            self.lastKeyPressed = key
            #self.lastSpokeAt = time.time()
        else:
            if self.clothNo != clothNo:
                print("in texttospeech.keypressed, new clothno is ",clothNo)
                self.clothNo = clothNo
                print("setting self.clothno to ",self.clothNo)
                print("setting last pressed key to",key)
                self.selectionChanged = True
                self.keyPressedAt = time.time()
                self.lastKeyPressed = key
                #self.lastSpokeAt = time.time()

    def getNameFromSaddleCloth(self,clothNo):
        prices = self.ba.getprices
        for p in prices:
            cloth = self.ba.getsaddlecloth(p.selection)
            if cloth == clothNo:
                return p.selection
        return ""

    def run(self):
        while self.active == True:
            if (time.time() * 1000) -( self.keyPressedAt * 1000) < 200:
                #self.lastSpokeAt = time.time()
                print("Last spoke ",str((time.time() * 1000) -( self.lastSpokeAt * 1000)) + " milliseconds")
                #wait to see if another key is pressed
                #if self.lastKeyPressed == "0" or self.lastKeyPressed == "1" or self.lastKeyPressed == "10" or self.lastKeyPressed == "11":
            else:
                if self.selectionChanged == True:
                    self.selectionChanged = False
                    prices =self.ba.getprices
                    self.selection = self.getNameFromSaddleCloth(self.clothNo)
                    if self.selection == "":
                        s = str(self.clothNo) + ", NO!"
                        t = threading.Thread(target = self.talk,args= (s,))
                        t.start()
                        #self.lastSpokeAt = time.time()
                    else:
                        for p in prices:
                            if p == None:
                                return
                            if p.selection == self.selection:
                                s = str(self.clothNo) + ", " +   str(p.backodds1)
                                self.talk(s)
                else:
                    #print("comparison",(time.time() * 1000) -( self.lastSpokeAt * 1000) >= 2000 and (self.allowSpeech == True))
                    if (time.time() * 1000) -( self.lastSpokeAt * 1000) >= 1300 and (self.allowSpeech == True):
                        #print("triggered new speak",time.time(),self.lastSpokeAt,(time.time() * 1000) -( self.lastSpokeAt * 1000))
                        #print("      comparison",(time.time() * 1000) -( self.lastSpokeAt * 1000) >= 2500 and (self.allowSpeech == True))
                        if self.clothNo !=0:
                            prices =self.ba.getprices
                            self.selection = self.getNameFromSaddleCloth(self.clothNo)
                            if self.selection == "":
                                s = str(self.clothNo) + ", NO!"
                                self.talk(s)
                                #self.lastSpokeAt = time.time()
                            else:
                                for p in prices:
                                    if p == None:
                                        return
                                    if p.selection == self.selection:
                                        s = str(p.backodds1)
                                        self.talk(s)
            time.sleep(0.1)
        print("exiting TTS thread")

    def reset(self):
        self.clothNo = 0

    def kill(self):
        self.active = False

    def speakCurrentPrice(self):
        self.lastSpokeAt = 0

    def talk(self,text):
        t = time.time()
        self.allowSpeech = False
        self.lastSpokeAt = time.time()
        #print("setting allow speech to False",time.time(),self.lastSpokeAt)
        self.speaker.speak(text)
        #print("talking took",(time.time() * 1000) -( t * 1000))
        self.lastSpokeAt = time.time()
        self.allowSpeech = True
        #print("resetting allow speech to true",time.time(),self.lastSpokeAt)

