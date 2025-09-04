import speech_recognition as sr
import wikipedia
import datetime
import pyttsx3


class GeneralQuestionAnswering:
    def __init__(self):
        wikipedia.set_lang("en")
        self.engine = pyttsx3.init()
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[1].id if len(voices) > 1 else voices[0].id)
        self.listener = sr.Recognizer()

    def talk(self, text):
        """Speak the given text using text-to-speech."""
        print(f"Nova: {text}")
        self.engine.say(text)
        self.engine.runAndWait()

    def take_command(self):
        """Listen for a voice command and return it as text."""
        with sr.Microphone() as source:
            print("Listening...")
            self.listener.adjust_for_ambient_noise(source)
            audio = self.listener.listen(source)
        try:
            command = self.listener.recognize_google(audio)
            print(f"You said: {command}")
            return command
        except sr.UnknownValueError:
            print("Sorry, I didn't catch that.")
            return ""
        except sr.RequestError:
            print("Sorry, there was a network error.")
            return ""

    def answer(self, user_input):
        """Process user input and return a response."""
        user_input_lower = user_input.lower()

        if "hello" in user_input_lower or "hi" in user_input_lower:
            return "Hello! How can I help you today?"
        
        elif "your name" in user_input_lower:
            return "I'm Nova!"
        
        elif "who are you" in user_input_lower:
            return "I'm Nova, your personal AI assistant."
        
        elif "how are you" in user_input_lower:
            return "I'm doing great, thank you for asking! How are you?"
        
        elif "date" in user_input_lower:
            return f"Today's date is {datetime.date.today().strftime('%B %d, %Y')}."

        elif "time" in user_input_lower:
            return f"The current time is {datetime.datetime.now().strftime('%H:%M:%S')}."

        elif "how can you help" in user_input_lower:
            return "I can answer your questions, provide information, and assist you with tasks."

        elif "stop" in user_input_lower or "exit" in user_input_lower or "goodbye" in user_input_lower or "bye" in user_input_lower:
            return "Goodbye!"

        else:
            try:
                summary = wikipedia.summary(user_input, sentences=2)
                return summary
            except wikipedia.exceptions.DisambiguationError as e:
                return f"Your question is too broad. Try being more specific. Here are some suggestions: {', '.join(e.options[:3])}"
            except wikipedia.exceptions.PageError:
                return "Sorry, I couldn't find any information on that topic."
            except Exception as e:
                return f"Oops! Something went wrong: {str(e)}"


if __name__ == "__main__": 
    assistant = GeneralQuestionAnswering()
    while True:
        command = assistant.take_command()
        if not command.strip():
            continue
        response = assistant.answer(command)
        assistant.talk(response)
    
        if any(word in response.lower() for word in ["goodbye", "bye", "stop", "exit"]):
            break
