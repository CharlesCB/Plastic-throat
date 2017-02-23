from pyo import *
import random

s = Server().boot()

# ténor (125 à 500 Hz)

o = [360,760,2530,3200]
a = [684,1256,2503]

class Synth:
    def __init__(self):
        self.env = Fader(fadein = 0.2, fadeout = 0.5).play()
        self.harms = random.randint(10,14)
        self.vibfreq = Sine(freq = 2, add = 1.5) 
        self.vibr = Sine(freq = self.vibfreq,add = 1, mul = 0.002)

        self.tremolo = Sine(freq = 2, add=1, mul = 0.01)
        
        self.bruit = PinkNoise(0.05)
        self.rauque = ButBP(self.bruit,freq = 1500)
        
        
        self.src = Blit(freq = 200 * self.vibr + self.rauque, harms = self.harms, mul = self.env * 2)
        self.lp = Biquad(self.src,freq = 350 * self.vibr, q = 1)
        
        self.bp1 = ButBP(self.lp, freq = o, q = 5)
        self.bp2 = ButBP(self.bp1, freq = o, q = 5)
        self.bp3 = ButBP(self.bp2, freq = o, q = 5).mix(2).out()


voix = Synth()

s.start()
s.gui(locals())
