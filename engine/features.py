import os
import re
from shlex import quote
import sqlite3
import struct
import subprocess
from time import time
import webbrowser
from playsound import playsound
import eel
import pvporcupine
import pyaudio
import pyautogui
from engine.command import speak
from engine.config import ASSISTANT_NAME


import pywhatkit as kit

from engine.helper import extract_yt_term, remove_words

conn = sqlite3.connect("Nova.db")
cursor = conn.cursor()

@eel.expose
def playAssistantSound():
    music_dir = "www\\assets\\audio\\start_sound.mp3"
    playsound(music_dir)

def openCommand(query):
    query = query.replace(ASSISTANT_NAME, "")
    query = query.replace("open", "")
    query.lower()

    app_name = query.strip()

    if app_name != "":

        try:
            cursor.execute(
                'SELECT path FROM sys_command WHERE name IN (?)', (app_name,))
            results = cursor.fetchall()

            if len(results) != 0:
                speak("Opening "+query)
                os.startfile(results[0][0])

            elif len(results) == 0: 
                cursor.execute(
                'SELECT url FROM web_command WHERE name IN (?)', (app_name,))
                results = cursor.fetchall()
                
                if len(results) != 0:
                    speak("Opening "+query)
                    webbrowser.open(results[0][0])

                else:
                    speak("Opening "+query)
                    try:
                        os.system('start '+query)
                    except:
                        speak("not found")
        except:
            speak("some thing went wrong")

       

def playYoutube(query):
    search_term = extract_yt_term(query)
    speak("playing "+search_term+" on Youtube")
    kit.playonyt(search_term)
    

def hotword():
    porcupine=None
    paud=None
    audio_stream=None
    try:
       
         
        porcupine=pvporcupine.create(keywords=["Nova","alexa"]) 
        paud=pyaudio.PyAudio()
        audio_stream=paud.open(rate=porcupine.sample_rate,channels=1,format=pyaudio.paInt16,input=True,frames_per_buffer=porcupine.frame_length)
        
        
        while True:
            keyword=audio_stream.read(porcupine.frame_length)
            keyword=struct.unpack_from("h"*porcupine.frame_length,keyword)

          
            keyword_index=porcupine.process(keyword)

            
            if keyword_index>=0:
                print("hotword detected")

               
                import pyautogui as autogui
                autogui.keyDown("win")
                autogui.press("j")
                time.sleep(2)
                autogui.keyUp("win")
                
    except:
        if porcupine is not None:
            porcupine.delete()
        if audio_stream is not None:
            audio_stream.close()
        if paud is not None:
            paud.terminate()


def findContact(query):
    
    words_to_remove = [ASSISTANT_NAME, 'make', 'a', 'to', 'phone', 'call', 'send', 'message', 'wahtsapp', 'video']
    query = remove_words(query, words_to_remove)

    try:
        query = query.strip().lower()
        cursor.execute("SELECT mobile_no FROM contacts WHERE LOWER(name) LIKE ? OR LOWER(name) LIKE ?", ('%' + query + '%', query + '%'))
        results = cursor.fetchall()
        print(results[0][0])
        mobile_number_str = str(results[0][0])

        if not mobile_number_str.startswith('+94'):
            mobile_number_str = '+94' + mobile_number_str

        return mobile_number_str, query
    except:
        speak('not exist in contacts')
        return 0, 0
    
def whatsApp(mobile_no, message, flag, name):
    

    if flag == 'message':
        target_tab = 13
        Nova_message = "message send successfully to "+name

    elif flag == 'call':
        target_tab = 8
        message = ''
        Nova_message = "calling to "+name

    else:
        target_tab = 7
        message = ''
        Nova_message = "staring video call with "+name

    encoded_message = quote(message)
    print(encoded_message)
    
    whatsapp_url = f"whatsapp://send?phone={mobile_no}&text={encoded_message}"

    
    full_command = f'start "" "{whatsapp_url}"'

    
    subprocess.run(full_command, shell=True)
    time.sleep(5)
    subprocess.run(full_command, shell=True)
    
    pyautogui.hotkey('ctrl', 'f')

    for i in range(1, target_tab):
        pyautogui.hotkey('tab')

    pyautogui.hotkey('enter')
    speak(Nova_message)
