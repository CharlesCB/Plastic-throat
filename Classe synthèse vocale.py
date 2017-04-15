#!/usr/bin/env python
# encoding: utf-8
from pyo import *
import random

s = Server()

# ténor (125 à 500 Hz // 48 à 72 midi)

ou = (290, 750, 2300, 3080, 4080)
o = (360,760,2530,3200, 4200)
oo = (520, 900, 2510, 3310, 4310)
aa = (710, 1230, 2700, 3700, 4700)
a = (750, 1450, 2590, 3280, 4280)
ee = (590, 1770, 2580, 3480, 4480)
oee = (570, 1560, 2560, 3450, 4450)
oe = (500, 1330, 2370, 3310, 4310)
eu = (350, 1350, 2250, 3170, 4170)
e = (420, 2050, 2630, 3340, 4340)
u = (250, 1750, 2160, 3060, 4060)
i = (250, 2250, 2980, 3280, 4280)

qou = [7,6,6,5,6]
class Synth:
    def __init__(self, vowel = ou, fadein = 0.001, fadeout = 0.1, hoarse = 0.1, 
                            vibfreq = 2, vibamp = 0.003,tremfreq = 2, tremamp = 0.001):
                                
        self.jitter = Noise(mul = 0.0001, add= 1)
        self.note = Notein(poly=5, scale=1, first=0, last=127)
        self.pit = self.note['pitch']
        self.amp = MidiAdsr(self.note['velocity'], attack=fadein, release=fadeout, mul=1)
        
        self.env = MidiAdsr(self.note['velocity'], attack = fadein * 2, release=fadeout)

        self.harms = Randi(min=50, max=55, freq=0.25) 

        self.vibr = Sine(freq = vibfreq * self.jitter ,add = 1, mul = vibamp * self.env * self.jitter) 

        self.tremolo = Sine(freq = tremfreq * self.jitter, add=1, mul = tremamp * self.jitter)

        self.bruit = PinkNoise(mul = hoarse)
        self.rauque = ButBP(self.bruit,freq = 1500, add=1) 

        self.src = Blit(freq = self.pit * self.vibr, harms = self.harms, mul = self.amp * self.tremolo)
        
        ## à paufiner
        self.sum = Denorm(self.src * self.rauque)

        self.lp = Biquadx(self.sum,freq = 400, q = 1, stages=2, mul = 0.1) 
        
        ## liste pour q
        
        self.f1 = Biquadx(self.lp, freq=vowel[0], q=qou[0], stages=3, mul=2)
        self.f2 = Biquadx(self.lp, freq=vowel[1], q=qou[1], stages=3, mul=2)
        self.f3 = Biquadx(self.lp, freq=vowel[2], q=qou[2], stages=3, mul=2)
        self.f4 = Biquadx(self.lp, freq=vowel[3], q=qou[3], stages=3, mul=2)
        self.f5 = Biquadx(self.lp, freq=vowel[4], q=qou[4], stages=3, mul=2)

        self.formants = self.f1.mix(1) + self.f2.mix(1) + self.f3.mix(1) + self.f4.mix(1) + self.f5.mix(1)

    def setVowel(self,x):
        self.f1.freq = x[0]
        self.f2.freq = x[1]
        self.f3.freq = x[2]
        self.f4.freq = x[3]
        
    def setFadein(self,x):
        self.amp.attack = x
        self.env.attack = x * 2

    def setFadeout(self,x):
        self.amp.release = self.env.release = x
        
    def setHoarse(self,x):
        self.bruit.amp = x
        
    def setVibfreq(self,x):
        self.vibr.freq = x * self.jitter

    def setVibamp(self,x):
        self.vibr.amp = x * self.env * self.jitter

    def setTremfreq(self,x):
        self.tremolo.freq = x * self.jitter

    def setVTremamp(self,x):
        self.tremolo.amp = x * self.jitter

    def out(self):
        self.formants.out()
        return self
        
s.setMidiInputDevice(3) 
s.boot()

voix = Synth().out()

s.start()
s.gui(locals())
