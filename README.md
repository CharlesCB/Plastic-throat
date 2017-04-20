# Plastic-throat
### Module de synthèse vocale pour application musicale

Plastic Throat est un module de synthèse vocale construite sur le modèle source-filtre construite en langage Python à l’aide de la librairie Pyo. Il a d’abord été élaboré comme une classe Python pour ensuite devenir un PyoObject, c’est à dire une classe qui hérite de PyoObject. Plastic Throat reçoit la norme MIDI pour simuler le chant d’une voyelle choisie. L’utilisateur peux ajuster l’ «a ttack » et le « release » de l’enveloppe d’amplitude, le niveau de raucité, l’amplitude et la fréquence (vitesse) du trémolo et du vibrato ainsi que la voyelle chantée. 

Un exemple de ce que Plastic Throat peut faire est disponible avec le PyoObject, il suffit de choisir le port d’entrée MIDI et, grâce à la méthode ctr() des PyoObjects, une interface graphique permet de changer les différents paramètres. 

Lien vers Pyo: http://ajaxsoundstudio.com/software/pyo/
