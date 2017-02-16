from pyo import *
import random

s = Server().boot()

# ténor (125 à 500 Hz)

o = [360,760,2530,3200]
class Synth:
    def __init__(self):
        self.env = Fader(fadein = 0.2, fadeout = 0.5).play()
        self.harms = random.randint(10,14)
        self.vibfreq = Sine(freq = 2, add = 1.5) 
        self.vibr = Sine(freq = self.vibfreq,add = 1, mul = 0.002)

        self.tremolo = Sine(freq = 2, add=1, mul = 0.01)

        self.src = Blit(freq = 300 * self.vibr, harms = self.harms, mul = self.env)
        self.lp = Biquad(self.src,freq = 350 * self.vibr, q = self.vibfreq)

        bruit = PinkNoise(mul=0.05)
       # eq = EQ(self.src,freq = [684,1256,2503])
        self.bp = ButBP(self.lp, freq = o, q = 3).out()

s.start()
s.gui(locals())