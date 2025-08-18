import tkinter as tk
from tkinter import ttk, messagebox
import threading
import speech_recognition as sr
from main import weather, speak

# Create GUI window
root = tk.Tk()
root.title("WeatherNow")
root.geometry("650x550")
root.config(bg="#1e1e2f")

# Fonts & Colors
BG_COLOR = "#1e1e2f"
CARD_COLOR = "#2e2e44"
TEXT_COLOR = "#ffffff"
ACCENT_COLOR = "#4e9fff"

# Title
title_label = tk.Label(root, text="🌦 WeatherNow", font=("Segoe UI", 20, "bold"), fg=ACCENT_COLOR, bg=BG_COLOR)
title_label.pack(pady=15)

# Weather Card
card_frame = tk.Frame(root, bg=CARD_COLOR, bd=0, relief="flat")
card_frame.pack(pady=15, fill="x", padx=20)

weather_label = tk.Label(
    card_frame, text="Initializing...", 
    font=("Segoe UI", 14), fg=TEXT_COLOR, bg=CARD_COLOR, 
    wraplength=500, justify="center"
)
weather_label.pack(pady=20)

# History Section
history_label = tk.Label(root, text="Search History", font=("Segoe UI", 14, "bold"), fg=ACCENT_COLOR, bg=BG_COLOR)
history_label.pack()

history_listbox = tk.Listbox(root, font=("Segoe UI", 12), bg=CARD_COLOR, fg=TEXT_COLOR, width=50, height=6, borderwidth=0, highlightthickness=0)
history_listbox.pack(pady=10)

def update_weather_card(report):
    weather_label.config(text=report)

def add_to_history(city):
    if city:
        history_listbox.insert(tk.END, city)

def ask_city():
    """Ask user for city name via voice recognition"""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        speak("Hello there!")
        update_weather_card("Hello There!")
        
        speak("Which city weather do you want to know?")
        update_weather_card("Which City Weather Do You want to Know?")
        
        try:
            audio = recognizer.listen(source, timeout=5)
            city = recognizer.recognize_google(audio)
            update_weather_card(f"Heard: {city}")
            return city
        except:
            update_weather_card("Sorry, I couldn't understand you.")
            speak("Sorry, I couldn't understand you.")
            return None

def fetch_weather(city=None):
    """Fetch weather either from entry or from mic"""
    if not city:
        city = city_var.get().strip()

    if not city:
        messagebox.showwarning("Input Error", "Please enter a city or use microphone.")
        return

    report = weather(city)  # Call weather() from main.py
    if "Sorry" in report:
        messagebox.showerror("Error", report)
        return

    speak(report)  # Speak the report
    update_weather_card(report)
    add_to_history(city)

def mic_flow():
    """Run full microphone flow in thread"""
    city = ask_city()
    if city:
        fetch_weather(city)

# Search Frame
search_frame = tk.Frame(root, bg=BG_COLOR)
search_frame.pack(pady=10)

city_var = tk.StringVar()

city_entry = ttk.Entry(search_frame, textvariable=city_var, font=("Segoe UI", 14), width=25)
city_entry.grid(row=0, column=0, padx=5)

search_btn = ttk.Button(search_frame, text="Get Weather", command=lambda: fetch_weather(city_var.get()))
search_btn.grid(row=0, column=1, padx=5)

mic_btn = ttk.Button(search_frame, text="🎤 Speak City", command=lambda: threading.Thread(target=mic_flow).start())
mic_btn.grid(row=0, column=2, padx=5)

# Start GUI
update_weather_card("Click 'Get Weather' or '🎤 Speak City' to begin")
root.mainloop()


