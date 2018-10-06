import win32com.client as wincl
from Speech import stt
from Answer import record_answer
speak = wincl.Dispatch("SAPI.SpVoice")
s1="EOQ"
s2="EOP"
s3="Q1"
def pread(q):                               #read out specified question
    f = open("Q" + str(q) + ".txt", "r+")
    for t in f:
        if s1 in t:
            speak.Speak("End of question")
        elif s3 in t:
            speak.Speak("Start of paper")
            speak.Speak(t)
        elif s2 in t:
            speak.Speak("This is the last question of the paper")
            break
        elif not t:
            break
        else:
            speak.Speak(t)
def read (q, arr):                               #read question with menu
    y = " "
    f = open("Q" + str(q) + ".txt", "r+")
    for t in f:
        if s1 in t:
            speak.Speak("End of question")
            speak.Speak("Choose option: 1. Repeat Question \n2. Record Answer\n 3. Mark as unsolved\n")
        elif s3 in t:
            speak.Speak("Start of paper")
            speak.Speak(t)
        elif s2 in t:
            speak.Speak("This is the last question of the paper")
            speak.Speak("Choose option: 1. Repeat Question \n2. Record Answer\n 3. Mark as unsolved\n")
        else:
            speak.Speak(t)
    try:
        y = stt()
        if int(y) == 1:
            read(q,arr)
        elif int(y) == 2:
            record_answer(q)        #record answer mechanism
            arr[q]=0
        elif int(y) == 3:
            arr[q] = 1
    except ValueError:
        speak.Speak("Please enter correct option. Question will be repeated")
        read(q, arr)
