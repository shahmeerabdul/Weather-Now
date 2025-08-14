import tkinter as tk
from tkinter import ttk, messagebox
import requests
from main import weather, speak  # Import your weather() and speak() from main.py
import os

# Create GUI window
root = tk.Tk()
root.title("Weather Assistant")
root.geometry("600x500")
root.config(bg="#1e1e2f")

# Fonts & Colors
BG_COLOR = "#1e1e2f"
CARD_COLOR = "#2e2e44"
TEXT_COLOR = "#ffffff"
ACCENT_COLOR = "#4e9fff"

# Title
title_label = tk.Label(root, text="🌦 Weather Assistant", font=("Segoe UI", 20, "bold"), fg=ACCENT_COLOR, bg=BG_COLOR)
title_label.pack(pady=15)

# Search Frame
search_frame = tk.Frame(root, bg=BG_COLOR)
search_frame.pack(pady=10)

city_var = tk.StringVar()

city_entry = ttk.Entry(search_frame, textvariable=city_var, font=("Segoe UI", 14), width=25)
city_entry.grid(row=0, column=0, padx=5)

def fetch_weather():
    city = city_var.get().strip()
    if not city:
        messagebox.showwarning("Input Error", "Please enter a city name.")
        return
    
    report = weather(city)  # Call your main.py function
    if "Sorry" in report:
        messagebox.showerror("Error", report)
        return
    
    speak(report)  # Speak the report
    update_weather_card(report)

search_btn = ttk.Button(search_frame, text="Get Weather", command=fetch_weather)
search_btn.grid(row=0, column=1, padx=5)

# Weather Card
card_frame = tk.Frame(root, bg=CARD_COLOR, bd=0, relief="flat")
card_frame.pack(pady=15, fill="x", padx=20)

weather_label = tk.Label(card_frame, text="Enter a city to see the weather", font=("Segoe UI", 14), fg=TEXT_COLOR, bg=CARD_COLOR, wraplength=500, justify="center")
weather_label.pack(pady=20)

def update_weather_card(report):
    weather_label.config(text=report)

# History Section
history_label = tk.Label(root, text="Search History", font=("Segoe UI", 14, "bold"), fg=ACCENT_COLOR, bg=BG_COLOR)
history_label.pack()

history_listbox = tk.Listbox(root, font=("Segoe UI", 12), bg=CARD_COLOR, fg=TEXT_COLOR, width=50, height=6, borderwidth=0, highlightthickness=0)
history_listbox.pack(pady=10)

def add_to_history(city):
    history_listbox.insert(tk.END, city)

search_btn.config(command=lambda: [fetch_weather(), add_to_history(city_var.get())])

# Run App
root.mainloop()

