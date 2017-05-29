__author__ = 'neil'

import sqlite3
import pickle
import operator
import speech_recognition as sr
import os
import wave
import audioop
from collections import deque
import time
import math
import time

from pocketsphinx.pocketsphinx import *
from sphinxbase.sphinxbase import *

MODELDIR = "/speech recognition/"

lm = 'speech recognition/7971.lm'
dic = 'speech recognition/7971.dic'
mic = sr.Microphone()
running = True
saddleclothSelection = []
speechToNumber = {"one":1,"two":2,"three":3,"four":4,"five":5,"six":6,"seven":7,"eight":8,"nine":9,"ten":10,"eleven":11,"twelve":12,"thirteen":13,"fourteen":14,"fifteen":15,"sixteen":16,"seventeen":17,"eighteen":18,"nineteen":19,"twenty":20}

# obtain audio from the microphone
r = sr.Recognizer()

def get_microphone_energy():
    return r.get_energy_value()

def set_recogniser_settings(values):
    if not r is None:
        r.set_values(values)

def get_recogniser_settings():
    if not r is None:
        return r.get_values()
    return []

def stop_speech_recognition_thread():
    global running
    running = False

def get_next_saddlecloth_selection(consume=True):
    global saddleclothSelection
    if saddleclothSelection != []:
        if consume == True:
            return saddleclothSelection.pop(0)
        else:
            return saddleclothSelection[0]
    return ""

def add_item_to_saddlecloth_selection(clothNo):
    global saddleclothSelection
    saddleclothSelection.append(clothNo)

def clear_saddlecloth_queue():
    global saddleclothSelection
    saddleclothSelection = []


def speech_recognition_thread():
    global saddleclothSelection
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source=source)
        while running == True:
            #print("Say something!")
            start = time.time()*1000.0
            try:
                #print("listening on mic")
                audio = r.listen(source,timeout=0.5)
                # recognize speech using Sphinx
                try:
                    start2 = time.time()*1000.0
                    print("starting decipher at ",time.time()*1000.0 - start)
                    result = r.recognize_sphinx(audio,lm=lm,dic=dic)
                    print("took ",time.time()*1000.0 - start2," to decipher audio")
                    words = result.split(" ")
                    #print("Sphinx thinks you said " + result)
                    #print("time since start of listen",time.time()*1000.0 - start)
                    try:
                        for word in words:
                            saddleclothSelection.append(speechToNumber[word.lower()])
                        print(saddleclothSelection)
                    except Exception as e:
                        pass
                        ### couldnt find interpret the speech
                        ###
                except sr.UnknownValueError:
                    print("Sphinx could not understand audio")
                except sr.RequestError as e:
                    print("Sphinx error; {0}".format(e))
            except sr.WaitTimeoutError as e:
                #print("timed out")
                pass
            #print("time since phrase started",time.time()*1000.0 - start)
    print("ending speech recognition thread")

#speech_recognition_thread()