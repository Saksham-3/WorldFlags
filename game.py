import requests
import customtkinter as ctk
from PIL import Image, ImageTk
import random
from tkinter import messagebox
from ttkbootstrap import Style
import tkinter as tk
from constants import *


class FlagGuessingGame:
    def __init__(self, app):
        self.app = app
        self.app.geometry(screensize)

        self.score = 0
        self.lives = 5
        self.best_score = 0
        self.flag_url = ""
        self.answer = ""
        self.country_desc = ""
        self.capital = ""

        self.title = ctk.CTkLabel(self.app, text="Guess the country this flag originates from:", font=("Arial", 20))
        self.title.pack(padx=10, pady=10)

        self.flag_frame = ctk.CTkFrame(self.app)
        self.flag_frame.pack(pady=20)

        self.flag_image = ctk.CTkLabel(self.flag_frame,text="")
        self.flag_image.pack()

        self.desc_label = ctk.CTkLabel(self.app,font=("Arial", 16))
        self.desc_label.pack()

        self.capital_label = ctk.CTkLabel(self.app,font=("Arial", 16))
        self.capital_label.pack()

        self.input_var = ctk.StringVar()
        self.input = ctk.CTkEntry(self.app,font=("Arial", 14), textvariable=self.input_var, width=200)
        self.input.pack()

        self.submit = ctk.CTkButton(self.app, text="Submit", command=self.check_answer, font=("Arial", 14))
        self.submit.pack(pady=10)
        self.input.bind('<Return>', lambda event=None: self.check_answer())

        self.score_label = ctk.CTkLabel(self.app, text=f"Score: {self.score} | Lives: {self.lives}", font=("Arial", 20))
        self.score_label.pack()

        self.high_score_label = ctk.CTkLabel(self.app, text=f"Best Score: {self.best_score}", font=("Arial", 14))
        self.high_score_label.pack()

        self.reset_button = ctk.CTkButton(self.app, text="Play Again", command=self.reset_game, font=("Arial", 14))
        self.reset_button.pack_forget()

        self.flagAPI()

    def flagAPI(self):
        url = "https://restcountries.com/v3.1/all"
        response = requests.get(url)

        countries_data = response.json()

        filters = [country 
                   for country in countries_data if country.get('population', 0) > min_pop]
        
        if filters:
            country_data = random.choice(filters)
            self.answer = country_data.get("name", {}).get("common")
            self.flag_url = country_data.get("flags", {}).get("png")

            population = country_data.get('population', 'N/A')
            if isinstance(population, int) and population > 100000:
                population = "{:,}".format(population)

            self.country_desc = f"Population: {population} | Continent: {country_data.get('region', 'N/A')}"
            self.capital = country_data.get('capital')
            self.capital = self.capital[0]

            self.load_img(self.flag_url)
            self.display_desc(self.country_desc)
            self.display_capital(self.capital)

    def load_img(self, url):
        response = requests.get(url)

        with open("flag.png", "wb") as flag:
            flag.write(response.content)

        img = Image.open("flag.png")
        img = img.resize(image_size)
        img = ImageTk.PhotoImage(img)

        self.flag_image.configure(image=img)
        self.flag_image.image = img
        

    def display_desc(self, desc_text):
        self.desc_label.configure(text=desc_text)
        
    def display_capital(self, capital_text):
        self.capital_label.configure(text=f"Capital: {capital_text}")

        
    def check_answer(self):
        user_guess = self.input.get().title()
        print(user_guess)

        if user_guess == self.answer:
            messagebox.showinfo("Correct", "Congratulations! You guessed the country right!")
            self.score += 1
            self.input.delete(0, tk.END)  #clear input
        else:
            messagebox.showerror("Incorrect", f"Sorry, the correct country was {self.answer}. You lost 1 life!")
            self.lives -= 1
            self.input.delete(0, tk.END)  #clear input

        if self.score > self.best_score:
            self.best_score = self.score

        self.score_label.configure(text=f"Score: {self.score} | Lives: {self.lives}")
        self.high_score_label.configure(text=f"Best Score: {self.best_score}")

        if self.lives == 0:
            messagebox.showinfo("Game Over", f"Game Over! Your final score: {self.score}")
            self.reset_button.pack()
            self.input.configure(state='disabled')
            self.submit.configure(state='disabled')
        else:
            self.flagAPI()

    def reset_game(self):
        self.score = 0
        self.lives = 5
        self.score_label.configure(text=f"Score: {self.score} | Lives: {self.lives}")
        self.reset_button.pack_forget()
        self.flagAPI()
        self.input.delete(0, tk.END)  #clear input
        self.input.configure(state='normal')
        self.submit.configure(state='normal')

def main():
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")
    app = ctk.CTk()
    app.title("Guess the Flag!")
    game = FlagGuessingGame(app)
    app.mainloop()

if __name__ == "__main__":
    main()