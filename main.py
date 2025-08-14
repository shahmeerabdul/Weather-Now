import requests
from plyer import notification
import pyttsx3
import speech_recognition as sr
import pyaudio

# Speak Function that Speaks out the Weather
def speak(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 180)
    engine.say(text)
    engine.runAndWait()

# This Function Fetches the Weather of a City from API Key
def weather(city):
    API_KEY = "aec5d76b2089614dac50cec7bf2753fe"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    try:
        response = requests.get(url)
        data = response.json()
        
        if data["cod"] != 200:
            return f"Sorry, I couldn't find weather for {city}."
        
        temp = data["main"]["temp"]
        description = data["weather"][0]["description"]
        country = data["sys"]["country"]
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]
        rain = data.get("rain", {}).get("1h", 0)  # Rain in last 1 hour (mm)

        # Weather-based message
        if "rain" in description.lower() or rain > 0:
            message = "Don't forget your umbrella!"
        elif temp > 30:
            message = "It's quite hot! Stay hydrated."
        elif temp < 10:
            message = "It's cold outside! Wear something warm."
        else:
            message = "The weather looks pleasant. Enjoy your day!"

        # Full weather report
        weather_report = (
            f"The weather in {city}, {country} is {description} "
            f"with a temperature of {temp}°C, humidity at {humidity}%, "
            f"wind speed of {wind_speed} meter per second, and rain expectation of {rain} mm. "
            f"{message}"
        )

        # Print weather details
        print(weather_report)

        # Send notification
        notification.notify(
            title=f"Weather in {city}",
            message=weather_report,
            timeout=10
        )

        return weather_report

    except Exception as e:
        return "Sorry, I had trouble fetching the weather."

# This Recognizes Your Voice
if __name__ == "__main__":
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Hello buddy! Hope You are Well")
        speak("Hello buddy! Hope You are Well")
        print("Which City Weather Do You want to Know?")
        speak("Which City Weather Do You want to Know?")
        audio = recognizer.listen(source)
        try:
            city = recognizer.recognize_google(audio)
            print(f"Heard: {city}")
        
            weather_report = weather(city)
            speak(weather_report)
        except:
            print("Sorry, I couldn't understand you.")
            speak("Sorry, I couldn't understand you.")
