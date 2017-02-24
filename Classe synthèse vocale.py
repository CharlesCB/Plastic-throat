from pyo import *
import random

s = Server().boot()

# ténor (125 à 500 Hz)

ou = [290, 750, 2300, 3080]
o = [360,760,2530,3200]
oo = [520, 900, 2510, 3310,]
aa = [710, 1230, 2700, 3700] 
a = [750, 1450, 2590, 3280]
ee = [590, 1770, 2580, 3480]
oee = [570, 1560, 2560, 3450]
oe = [500, 1330, 2370, 3310]
eu = [350, 1350, 2250, 3170]
e = [420, 2050, 2630, 3340]
u = [250, 1750, 2160, 3060]
i = [250, 2250, 2980, 3280]


class Synth:
    def __init__(self, vowel = o, fadein = 0.2, fadeout = 0.5):
        self.env = Fader(fadein = fadein, fadeout = fadeout).play()
        self.harms = random.randint(20,25)
        self.vibfreq = Sine(freq = 2, add = 1.5) 
        self.vibr = Sine(freq = self.vibfreq,add = 1, mul = 0.002)

        self.tremolo = Sine(freq = 2, add=1, mul = 0.01)
        
        self.bruit = PinkNoise(0.05)
        self.rauque = ButBP(self.bruit,freq = 1500)
        
        
        self.src = Blit(freq = 200 * self.vibr + self.rauque, harms = self.harms, mul = self.env * 2).mix(2)
        self.lp = Biquad(self.src,freq = 350 * self.vibr, q = 1)
        
        self.bp1 = ButBP(self.lp, freq = vowel, q = 5, mul = 1.5)
        self.bp2 = ButBP(self.bp1, freq = vowel, q = 5, mul = 1.5)
        self.bp3 = ButBP(self.bp2, freq = vowel, q = 5, mul = 1.5)
        
        self.reverb = Freeverb(self.bp3).out()


voix = Synth()

s.start()
s.gui(locals())
