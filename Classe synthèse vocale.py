from pyo import *
import random

s = Server().boot()

# ténor (125 à 500 Hz // 48 à 72 midi)

ou = [290, 750, 2300, 3080]
o = [360,760,2530,3200]
oo = [520, 900, 2510, 3310]
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
       # self.note = Notein(poly=10, scale=1, first=0, last=127)
       # self.pit = self.note['pitch']
        
        self.env = Fader(fadein = fadein, fadeout = fadeout).play()

        self.harms = Randi(min=35, max=40, freq=0.25)

        self.vibfreq = Sine(freq = 2, add = 1.5) 
        self.vibr = Sine(freq = self.vibfreq,add = 1, mul = 0.002 * self.env)

        self.tremolo = Sine(freq = 2, add=1, mul = 0.001)

        ### As-tu essaye de multiplier la source harmonique (Blit) par le bruit filtre?
        ### Bien dose, ca aide a donner le sentiment que les deux proviennent de la meme source.
        self.bruit = PinkNoise(0.05)
        self.rauque = ButBP(self.bruit,freq = 1500)

        self.src = Blit(freq = midiToHz(48) * self.vibr, harms = self.harms, mul = self.env).mix(2)
        self.src * self.rauque
        self.lp = Biquadx(self.src,freq = 350 * self.vibr, q = 1, stages=2, mul = 0.5)
        
        self.formants = Biquadx(self.lp, freq=vowel, q=5, stages=3, mul=0.3).mix(1).out()

voix = Synth(o)
s.start()
s.gui(locals())
