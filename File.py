import win32com.client as wincl
import os
import re
import numpy as np
from Speech import stt
from Read import read
from Revise import revise,unsolved
from Scan import scan
scan()
file = open("text.txt", "r+")
speak = wincl.Dispatch("SAPI.SpVoice")
eoqRegex1=re.compile(r'Q\d')
eoqRegex2=re.compile(r'Q\s.')
s1="EOQ"
s2="EOP"
s3="Q1"
c=1
start=False
try:
    f=open("Q"+str(c)+".txt","x")
except FileExistsError:
    print("")
f = open("Q"+str(c)+".txt","w")

for x in file:
    mo1 = eoqRegex1.search(x)
    mo2=eoqRegex2.search(x)
    if mo1!=None or mo2!=None:
        start=True
    if start:
        if mo1!=None or mo2!=None:
            if s3 not in x:
                f.write("EOQ\n")
                f.close()
                c = c + 1
                try:
                    f = open("Q" + str(c) + ".txt", "x")
                except FileExistsError:
                    print("")
                f = open("Q" + str(c) + ".txt", "w")
                f.write(x)
            else:
                f.write(x)
        elif s1 in x:
            break
        elif s2 in x:
            f.write(x)
            f.close()
            break
        else:
            f.write(x)
file.close()
arr=np.zeros(30,dtype=int)
m=1
while m<c+1:
    read(m,arr)
    m=m+1

while True:
    speak.Speak("Would you like to know which questions remain unsolved or revise your answers? Answering no will end the paper")
    answer=stt()
    if answer=="no":
        break
    else:
        speak.Speak("Choose Option: 1. Revise answers\n2. Unsolved Questions\n")
        ans=stt()
        if int(ans)==2:
            unsolved(arr,c)
        elif int(ans)==1:
            revise(arr,c)
        else:
            speak.Speak("Enter correct option")

for q in range(1,c+1):
    s = "Q" + str(q) + ".txt"
    os.remove(s)
file=open("Answers.txt","x")
file=open("Answers.txt","r+")
for q in range(1,c+1):
    try:
        d=open("A"+str(q)+".txt","r+")
        file.write("A"+str(q)+". ")
        for text in d:
            file.write(text)
        file.write("\n")
        d.close()
        os.remove("A"+str(q)+".txt")
    except FileNotFoundError:
        file.write("A"+str(q)+". ")
        file.write("Unsolved\n")
file.close()
speak.Speak("Thank you for taking this test.")