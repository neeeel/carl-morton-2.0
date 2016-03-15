__author__ = 'neil'
import win32com.client,threading,betthread,time
import window

def incrementClothNo(selection):
    global ba
    clothNo = ba.getsaddlecloth(selection)
    print("current cloth no is ",clothNo)
    price_list = []
    count = 0
    prices = ba.getprices
    for p in prices:
        price_list.append((p.selection, ba.getsaddlecloth(p.selection)))
    price_list = sorted(price_list, key=lambda p: (p[1]))
    for p in price_list:
        print(p)
        if p[1] > clothNo:
            return p[0]
    return selection

def temp():
    count = 0
    while True:
        time.sleep(1)
        betThread.add_bet("w",count,2,5,"B")
        count+=1


betThread = betthread.betThread()
t = threading.Thread(target = temp)
t.start()
time.sleep(0.01)
t = threading.Thread(target = temp)
t.start()

