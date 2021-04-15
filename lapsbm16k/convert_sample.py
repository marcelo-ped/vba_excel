import os
from os import listdir
from os.path import isfile, join

mypath = "/home/marcelo/Datanuvem/vosk-test/treinamento/kaldi/egs/meu_teste_1/s5/corpus/lapsbm16k-master"
onlyfolder = [folder for folder in listdir(mypath) 
    if not isfile(join(mypath, folder))]
onlyfiles = []

for f in onlyfolder:
    #onlyfiles.append(listdir(f))
    files = [file for file in listdir(f)]    
    for a in files:
        if a.endswith("wav"):
            onlyfiles.append(mypath+'/'+f+'/'+a)
for f in onlyfiles:
    cmd = "sox " + f +" -r 16000 "+f.replace(".wav", "-enc.wav")
    os.system(cmd)
