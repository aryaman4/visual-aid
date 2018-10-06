import win32com.client as wincl
import speech_recognition as sr
speak = wincl.Dispatch("SAPI.SpVoice")
r=sr.Recognizer()
mic=sr.Microphone()
def stt():
    while True:
        with mic as source:
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source)
        try:
            phrase = r.recognize_google(audio)
            break
        except sr.UnknownValueError:
            speak.Speak("Could not recognize input. Please try again")

    return phrase
