import time
import pyttsx3
import speech_recognition as sr
import eel


def speak(text):
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)  
    engine.setProperty('rate', 174)  
    print(voices)
    eel.DisplayMessage(text)
    engine.say(text)
    engine.runAndWait()


def takecommand():
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening...")
        eel.DisplayMessage("Listening...")
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source)

        audio = r.listen(source, 10, 6)


    try:
        print("Recognizing...")
        eel.DisplayMessage("Recognizing...")
        query = r.recognize_google(audio, language='en-UK')
        print(f"User said: {query}")
        eel.DisplayMessage(query)
        time.sleep(2)
        speak(query)
    except Exception as e:
        return ""
    

    return query.lower()

@eel.expose
def allCommands():
 
    try:
            query = takecommand()
            print(query)

            if "open" in query:
                from engine.features import openCommand
                openCommand(query)

            elif "on youtube" in query:
                from engine.features import playYoutube
                playYoutube(query)

            elif "send message" in query or "phone call" in query or "video call" in query:
                from engine.features import findContact, whatsApp, makeCall, sendMessage
                contact_no, name = findContact(query)
                if(contact_no != 0):
                    speak("Which mode you want to use whatsapp or mobile")
                    preferance = takecommand()
                    print(preferance)

                    if "mobile" in preferance:
                        if "send message" in query or "send sms" in query: 
                            speak("what message to send")
                            message = takecommand()
                            sendMessage(message, contact_no, name)
                        elif "phone call" in query:
                            makeCall(name, contact_no)
                        else:
                            speak("please try again")
                    elif "whatsapp" in preferance:
                        message = ""
                        if "send message" in query:
                            message = 'message'
                            speak("what message to send")
                            query = takecommand()
                                            
                        elif "phone call" in query:
                            message = 'call'
                        else:
                            message = 'video call'
                                            
                        whatsApp(contact_no, query, message, name)


            else:
                print("not run")

    except:
        print("error")

    eel.ShowHood()
