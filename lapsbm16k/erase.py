import os
from os import listdir
from os.path import isfile, join

mypath = "/home/marcelo/Datanuvem/vosk-test/treinamento/kaldi/egs/meu_teste_1/s5/corpus/train"
onlyfolder = [folder for folder in listdir(mypath) 
    if not isfile(join(mypath, folder))]
onlyfiles = []

for f in onlyfolder:
    #onlyfiles.append(listdir(f))
    files = [file for file in listdir(f)]    
    for a in files:
        if a.endswith("txt"):
            onlyfiles.append(mypath+'/'+f+'/'+a)
for f in onlyfiles:
    with open(f,'r') as reader:
        lines =reader.readlines()
    for a in lines:
        with open(f,'w') as writer:
            writer.write(a.lower())
	
