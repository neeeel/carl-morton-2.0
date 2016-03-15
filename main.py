__author__ = 'neil'

import decimal

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


print(plusTicks(100,6))

print(int(""))