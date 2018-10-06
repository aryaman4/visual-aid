import win32com.client as wincl
from Speech import stt
from Read import pread,read
from Answer import re_answer
speak = wincl.Dispatch("SAPI.SpVoice")
def unsolved (arr,c):      #answer unsolved questions
    uns=False
    for q in range(1, c + 1):
        if arr[q] == 1:
            uns=True
            speak.Speak("Question" + str(q) + "is unsolved. Would you like the question to be repeated?")
            ans = stt()
            if ans == "yes":
                read(q,arr)
            else:
                continue
    if not uns:
        speak.Speak("There are no unsolved questions.")
def revise (arr,c):
    rev=False
    for q in range(1, c + 1):
        if arr[q] == 0:
            rev=True
            speak.Speak("Question" + str(q) + "has been solved. Would you like the question to be repeated?")
            ans = stt()
            if ans == "yes":
                pread(q)            #read out answer to user
                re_answer(q)        #answer re-record mechanism
            else:
                continue
    if not rev:
        speak.Speak("There are no solved questions.")