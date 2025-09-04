import datetime
import requests
import pyttsx3
import sys

def get_current_time():
    now = datetime.datetime.now()
    return now.strftime("The current time is %I:%M %p.")

def get_current_date():
    today = datetime.date.today()
    return today.strftime("Today is %B %d, %Y.")

def get_location():
    try:
        res = requests.get("https://ipinfo.io/json")
        if res.status_code == 200:
            data = res.json()
            loc = data.get("loc", None)
            city = data.get("city", "your area")
            if loc:
                lat, lon = loc.split(",")
                return lat, lon, city
    except Exception:
        pass
    return None, None, "your area"

def get_weather_live(api_key):
    lat, lon, city = get_location()
    if lat and lon:
        url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            temp = data['main']['temp']
            desc = data['weather'][0]['description']
            return f"The current weather in {city} is {desc} with a temperature of {temp}°C."
        else:
            return "Sorry, I couldn't fetch the weather information right now."
    else:
        return "Sorry, I couldn't determine your location."

def speak(text):
    engine = pyttsx3.init()
    # Set female voice
    voices = engine.getProperty('voices')
    for voice in voices:
        if "female" in voice.name.lower() or "zira" in voice.name.lower():
            engine.setProperty('voice', voice.id)
            break
    engine.say(text)
    engine.runAndWait()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        api_key = sys.argv[1]
    else:
        api_key = "a344b11b2c9c0b4ff020f783b7cf44ba"
    date_text = get_current_date()
    time_text = get_current_time()
    weather_text = get_weather_live(api_key)
    print(date_text)
    print(time_text)
    print(weather_text)
    speak(date_text)
    speak(time_text)
    speak(weather_text)