from pyo import *
import random

ou = [290, 750, 2300, 3080, 4080]
o = [360,760,2530,3200, 4200]
oo = [520, 900, 2510, 3310, 4310]
aa = [710, 1230, 2700, 3700, 4700]
a = [750, 1450, 2590, 3280, 4280]
ee = [590, 1770, 2580, 3480, 4480]
oee = [570, 1560, 2560, 3450, 4450]
oe = [500, 1330, 2370, 3310, 4310]
eu = [350, 1350, 2250, 3170, 4170]
e = [420, 2050, 2630, 3340, 4340]
u = [250, 1750, 2160, 3060, 4060]
i = [250, 2250, 2980, 3280, 4280]


class PlasticThroat(PyoObject):
    
    def __init__(self, vowel = aa, attack = 0.05, release = 0.1, hoarse = 0.05,
                    vibfreq = 2, vibamp = 0.001,tremfreq = 2, tremamp = 0.001,mul=1,add=0,):
        PyoObject.__init__(self,mul,add)
        self._vowel = vowel
        self._hoarse = hoarse
        self._vibfreq = vibfreq
        self._vibamp = vibamp
        self._tremfreq = tremfreq
        self._tremamp = tremamp
                
        vowel,attack,release,hoarse,vibfreq,vibamp,tremfreq,tremamp,mul,add, lmax = convertArgsToLists(vowel,attack,release,hoarse,vibfreq,vibamp,tremfreq,tremamp,mul,add)

        self._jitter = Noise(mul = 0.0001, add= 1)
        self._note = Notein(poly=5, scale=1, first=0, last=127)
        self._pit = self._note['pitch']
        self._amp = MidiAdsr(self._note['velocity'], attack = attack, release = release)
        
        self._env = MidiAdsr(self._note['velocity'], attack = attack * 2, release = release)

        self._harms = Randi(min=50, max=55, freq=0.25)

        self._vibr = Sine(freq = vibfreq * self._jitter ,add = 1, mul = vibamp * self._env * self._jitter) 

        self._tremolo = Sine(freq = tremfreq * self._jitter, add=1, mul = tremamp * self._jitter)

        self._bruit = PinkNoise(mul = hoarse)
        self._rauque = ButBP(self._bruit,freq = 1500, add=1) 

        self._src = Blit(freq = self._pit * self._vibr, harms = self._harms, mul = self._amp * self._tremolo)

        self._sum = Denorm(self._src * self._rauque)

        self._lp = Biquadx(self._sum,freq = 300, q = 1, stages=2, mul = 0.1) 
   
        if vowel == ou:
            self.q = [5,5,6,5,6]
        elif vowel == o:
            self.q = [4,4,6,5,5]
        elif vowel == oo:
            self.q = [5,6,5,6,5]
        elif vowel == aa:
            self.q = [5,5,5,6,6]
        elif vowel == a:
            self.q = [6,4,5,5,5]
        elif vowel == ee:
            self.q = [6,6,5,4,4]
        elif vowel == oee:
            self.q = [6,6,5,4,4]
        elif vowel == oe:
            self.q = [5,5,5,5,5]
        elif vowel == eu:
            self.q = [6,5,4,4,5]
        elif vowel == e:
            self.q = [4,5,6,6,6]
        elif vowel == u:
            self.q = [4,5,5,6,5]
        elif vowel == i:
            self.q = [4,4,5,6,6]
        else:
            print "Error, this vowel does not exist"

     
        self._f1 = Biquadx(self._lp, freq=SigTo(vowel[0],time = 0.1), q=SigTo(self.q[0],time = 0.1), stages=3, mul= 3,add=add)
        self._f2 = Biquadx(self._lp, freq=SigTo(vowel[1],time = 0.1), q=SigTo(self.q[1],time = 0.1), stages=3, mul= 3,add=add)
        self._f3 = Biquadx(self._lp, freq=SigTo(vowel[2],time = 0.1), q=SigTo(self.q[2],time = 0.1), stages=3, mul= 3,add=add)
        self._f4 = Biquadx(self._lp, freq=SigTo(vowel[3],time = 0.1), q=SigTo(self.q[3],time = 0.1), stages=3, mul= 3,add=add)
        self._f5 = Biquadx(self._lp, freq=SigTo(vowel[4],time = 0.1), q=SigTo(self.q[4],time = 0.1), stages=3, mul= 3,add=add)

        self._formants = self._f1.mix(1) + self._f2.mix(1) + self._f3.mix(1) + self._f4.mix(1)

        self._base_objs = self._formants.getBaseObjects()

    def setVowel(self,x, port = 0.5):
        if x == ou:
            q = [5,5,6,5,6]
        elif x == o:
            q = [4,4,6,5,5]
        elif x == oo:
            q = [5,6,5,6,5]
        elif x == aa:
            q = [5,5,5,6,6]
        elif x == a:
            q = [6,4,5,5,5]
        elif x == ee:
            q = [6,6,5,4,4]
        elif x == oee:
            q = [6,6,5,4,4]
        elif x == oe:
            q = [5,5,5,5,5]
        elif x == eu:
            q = [6,5,4,4,5]
        elif x == e:
            q = [4,5,6,6,6]
        elif x == u:
            q = [4,5,5,6,5]
        elif x == i:
            q = [4,4,5,6,6]
        else:
            print "Error, this vowel does not exist"  
                 
        self._f1.freq.value = x[0]
        self._f1.freq.time = self._f1.q.time = port
        self._f1.q.value = q[0]
        self._f2.freq.value = x[1]
        self._f2.freq.time = self._f2.q.time = port
        self._f2.q.value = q[1]
        self._f3.freq.value = x[2]
        self._f3.freq.time = self._f3.q.time = port
        self._f3.q.value = q[2]
        self._f4.freq.value = x[3]
        self._f4.freq.time = self._f4.q.time = port
        self._f4.q.value = q[3]
        self._f5.freq.value = x[4]
        self._f5.freq.time = self._f5.q.time = port
        self._f5.q.value = q[4]
        
    def setAttack(self,x):
        self._amp.attack = x
        self._env.attack = x * 2

    def setRelease(self,x):
        self._amp.release = self._env.release = x
        
    def setHoarse(self,x):
        self._bruit.mul = x
        
    def setVibfreq(self,x):
        self._vibr.freq = x * self._jitter

    def setVibamp(self,x):
        self._vibr.mul = x * self._env * self._jitter

    def setTremfreq(self,x):
        self._tremolo.freq = x * self._jitter

    def setTremamp(self,x):
        self._tremolo.mul = x * self._jitter

    def out(self,chnl=0,inc=1,dur=0,delay=0):
        self._formants.out()
        return PyoObject.out(self,chnl,inc,dur,delay)
    
    @property
    def vowel(self):
        return self._vowel
    @vowel.setter
    def vowel(self,x,port=0.1):
        self.setVowel(x,port)

    @property
    def hoarse(self): 
        return self._hoarse
    @hoarse.setter
    def hoarse(self, x): 
        self.setHoarse(x)
    
    @property
    def vibfreq(self): 
        return self._vibfreq
    @vibfreq.setter
    def vibfreq(self, x): 
        self.setVibfreq(x)
        
    @property
    def vibamp(self): 
        return self._vibamp
    @vibamp.setter
    def vibamp(self, x): 
        self.setVibamp(x)
        
    @property
    def tremfreq(self): 
        return self._tremfreq
    @tremfreq.setter
    def tremfreq(self, x): 
        self.setTremfreq(x)

    @property
    def tremamp(self): 
        return self._tremamp
    @tremamp.setter
    def tremamp(self, x): 
        self.setTremamp(x)
        
    def ctrl(self, map_list=None, title=None, wxnoserver=False):
        self._map_list = [SLMap(0.001, 5, "lin", "hoarse", self._hoarse),
                            SLMap(0.001, 1000, "log", "vibfreq", self._vibfreq),
                            SLMap(0.0001, 0.5, "log", "vibamp", self._vibamp),
                            SLMap(0.001, 1000, "log", "tremfreq", self._tremfreq),
                            SLMap(0.0001, 0.5, "log", "tremamp", self._tremamp),SLMapMul(self._mul)]
        PyoObject.ctrl(self, map_list, title, wxnoserver)

if __name__ == "__main__":
    s = Server()
    s.setMidiInputDevice(3) 
    s.boot()

    voix = PlasticThroat()
    reverb = WGVerb(voix,bal = 0.25).out()
    voix.ctrl()

    s.start()
    s.gui(locals())
