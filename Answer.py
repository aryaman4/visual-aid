import win32com.client as wincl
from Speech import stt
import os
speak = wincl.Dispatch("SAPI.SpVoice")
def record_answer(q):
    speak.Speak("Please record answer now")
    a = open("A" + str(q) + ".txt", "x")
    a = open("A" + str(q) + ".txt", "r+")
    ra=stt()
    a.write(ra)
    a.close()
def re_answer(q):
    t=open("t.txt","x")
    t=open("t.txt","r+")
    speak.Speak("Re-record answer now")
    ra=stt()
    t.write(ra)
    t.close()
    os.remove("A"+str(q)+".txt")
    os.renames("t.txt","A"+str(q)+".txt")