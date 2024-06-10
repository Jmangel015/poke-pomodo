import io
import random
import time
import threading
import tkinter as tk
import pandas as pd
import os
import requests
from PIL import Image, ImageTk
import pokebase as poke


class TimerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.pokImageLabel = None
        self.pokNameLabel = None
        self.title("Temporizador")
        self.geometry("400x250")
        self.config(bg="#121212")

        self.label = tk.Label(self, text="Introduce el tiempo y presiona Iniciar", font=("Arial", 12), bg="#121212",
                              fg="white")
        self.label.pack(pady=10)

        self.entry = tk.Entry(self, font=("Arial", 12))
        self.entry.pack(pady=10)

        self.start_button = tk.Button(self, text="Iniciar", command=self.start_timer, font=("Arial", 12),
                                      bg="#1f1f1f", fg="white")
        self.start_button.pack(pady=5, padx=10, side=tk.LEFT)

        self.pause_button = tk.Button(self, text="Pausa", command=self.pause_timer, state=tk.DISABLED,
                                      font=("Arial", 12), bg="#1f1f1f", fg="white")
        self.pause_button.pack(pady=5, padx=10, side=tk.LEFT)

        self.stop_button = tk.Button(self, text="Detener", command=self.stop_timer, state=tk.DISABLED,
                                     font=("Arial", 12), bg="#1f1f1f", fg="white")
        self.stop_button.pack(pady=5, padx=10, side=tk.LEFT)

        self.remaining_time = 0
        self.running = False
        self.start_time = None
        self.pause_time = None

        self.poke_images = []

    def start_timer(self):
        try:
            time_input = self.entry.get()
            hours, minutes, seconds = map(int, time_input.split(':'))
            self.remaining_time = hours * 3600 + minutes * 60 + seconds
            self.start_button.config(state=tk.DISABLED)
            self.pause_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.NORMAL)
            self.running = True
            self.label.config(text=self.format_time(self.remaining_time))
            self.update_timer()

            threading.Thread(target=self.search_poke).start()

        except ValueError:
            self.label.config(text="Formato inválido. Usa HH:MM:SS")

    def update_timer(self):
        if self.running:
            if self.remaining_time > 0:
                self.remaining_time -= 1
                self.label.config(text=self.format_time(self.remaining_time))
                self.after(1000, self.update_timer)
            else:
                self.label.config(text="Tiempo finalizado")
                self.running = False
                self.start_button.config(state=tk.NORMAL)
                self.pause_button.config(state=tk.DISABLED)
                self.stop_button.config(state=tk.DISABLED)
                self.save_time_to_csv()

    def pause_timer(self):
        if self.running:
            self.running = False
            self.pause_time = time.time()
            self.start_button.config(text="Continuar", state=tk.NORMAL)
            self.pause_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)

    def stop_timer(self):
        self.running = False
        self.start_button.config(text="Iniciar", state=tk.NORMAL)
        self.pause_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.DISABLED)
        self.remaining_time = 0
        self.label.config(text="Introduce el tiempo y presiona Iniciar")

    def save_time_to_csv(self):
        total_seconds = self.entry.get().split(":")
        total_seconds = int(total_seconds[2]) + int(total_seconds[1]) * 60 + int(total_seconds[0]) * 3600

        today = pd.Timestamp.now().date()
        day_of_week = today.strftime('%A')
        day_of_month = today.day

        if os.path.exists("tiempos_de_estudio.csv"):
            df_existing = pd.read_csv("tiempos_de_estudio.csv")

            if not df_existing.empty and df_existing["Fecha"].iloc[-1] == str(today):
                df_existing.at[len(df_existing) - 1, "Total Segundos"] += total_seconds

                # Convert total seconds to hours, minutes, and seconds
                total_time = df_existing.at[len(df_existing) - 1, "Total Segundos"]
                hours, remainder = divmod(total_time, 3600)
                minutes, seconds = divmod(remainder, 60)

                df_existing.at[len(df_existing) - 1, "Horas"] = hours
                df_existing.at[len(df_existing) - 1, "Minutos"] = minutes
                df_existing.at[len(df_existing) - 1, "Segundos"] = seconds
            else:
                hours, remainder = divmod(total_seconds, 3600)
                minutes, seconds = divmod(remainder, 60)
                new_row = {"Fecha": today,
                           "Día de la Semana": day_of_week,
                           "Día del Mes": day_of_month,
                           "Horas": hours,
                           "Minutos": minutes,
                           "Segundos": seconds,
                           "Total Segundos": total_seconds}
                df_existing = pd.concat([df_existing, pd.DataFrame([new_row])], ignore_index=True)

            df_existing.to_csv("tiempos_de_estudio.csv", index=False)
        else:
            hours, remainder = divmod(total_seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            df_today = pd.DataFrame({"Fecha": [today],
                                     "Día de la Semana": [day_of_week],
                                     "Día del Mes": [day_of_month],
                                     "Horas": [hours],
                                     "Minutos": [minutes],
                                     "Segundos": [seconds],
                                     "Total Segundos": [total_seconds]})
            df_today.to_csv("tiempos_de_estudio.csv", index=False)

    def format_time(self, seconds):
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"

    def search_poke(self):
        pokemon = poke.pokemon(random.randint(1, 151))
        name = pokemon.name.capitalize()
        image_url = pokemon.sprites.front_default

        response = requests.get(image_url)
        if response.status_code == 200:
            image_data = response.content
            image = Image.open(io.BytesIO(image_data))
            image = image.resize((150, 150), Image.LANCZOS)  # Ajusta el tamaño de la imagen
            photo = ImageTk.PhotoImage(image)
            self.poke_images.append(photo)  # Agrega la imagen a la lista

            self.update_poke_label(name, len(self.poke_images) - 1)  # Pasa el índice de la imagen en la lista

    def update_poke_label(self, name, index):
        textPokeName = f"Haz encontrado un: {name}"
        if self.pokNameLabel:
            self.pokNameLabel.config(text=textPokeName)
        else:
            self.pokNameLabel = tk.Label(self, text=textPokeName, font=("Arial", 12), bg="#121212", fg="white")
            self.pokNameLabel.pack(pady=10, anchor="center")

        if self.pokImageLabel:
            self.pokImageLabel.config(image=self.poke_images[index])  # Obtén la imagen de la lista
        else:
            self.pokImageLabel = tk.Label(self, image=self.poke_images[index], bg="#121212")
            self.pokImageLabel.pack(pady=10)
            self.pokImageLabel.image = self.poke_images[index]
            self.pokImageLabel.pack(pady=(0, 20))


if __name__ == "__main__":
    app = TimerApp()
    app.mainloop()
