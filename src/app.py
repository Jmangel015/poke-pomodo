import time
import tkinter as tk


class ChronometerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Cronómetro")
        self.geometry("300x150")
        self.config(bg="#121212")

        self.label = tk.Label(self, text="Presiona el botón para iniciar", font=("Arial", 16), bg="#121212", fg="white")
        self.label.pack(pady=20)

        self.start_button = tk.Button(self, text="Iniciar", command=self.start_chronometer, font=("Arial", 12),
                                      bg="#1f1f1f", fg="white")
        self.start_button.pack(pady=5, padx=10, side=tk.LEFT)

        self.pause_button = tk.Button(self, text="Pausa", command=self.pause_chronometer, state=tk.DISABLED,
                                      font=("Arial", 12), bg="#1f1f1f", fg="white")
        self.pause_button.pack(pady=5, padx=10, side=tk.LEFT)

        self.stop_button = tk.Button(self, text="Detener", command=self.stop_chronometer, state=tk.DISABLED,
                                     font=("Arial", 12), bg="#1f1f1f", fg="white")
        self.stop_button.pack(pady=5, padx=10, side=tk.LEFT)

        self.elapsed_time = 0
        self.running = False
        self.start_time = None
        self.pause_time = None

    def start_chronometer(self):
        if not self.running:
            self.label.config(text="Iniciar", fg="white")
            self.start_button.config(state=tk.DISABLED)
            self.pause_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.NORMAL)
            self.running = True
            if self.start_time is None:
                self.start_time = time.time()
            else:
                self.start_time += time.time() - self.pause_time
            self.update_chronometer()

    def update_chronometer(self):
        if self.running:
            elapsed_time = time.time() - self.start_time + self.elapsed_time
            minutes, seconds = divmod(elapsed_time, 60)
            hours, minutes = divmod(minutes, 60)
            self.label.config(text=f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}", fg="white")
            self.after(1000, self.update_chronometer)

    def pause_chronometer(self):
        if self.running:
            self.running = False
            self.pause_time = time.time()
            elapsed_time = self.pause_time - self.start_time + self.elapsed_time
            minutes, seconds = divmod(elapsed_time, 60)
            hours, minutes = divmod(minutes, 60)
            self.label.config(text=f"{int(hours):02}:{int(minutes):02}:{int(seconds):02} - Pausado", fg="white")
            self.start_button.config(text="Continuar", state=tk.NORMAL)
            self.pause_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)

    def stop_chronometer(self):
        self.running = False
        self.start_button.config(text="Iniciar", state=tk.NORMAL)
        self.pause_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.DISABLED)
        if self.start_time is not None:
            total_time = time.time() - self.start_time + self.elapsed_time
            minutes, seconds = divmod(total_time, 60)
            hours, minutes = divmod(minutes, 60)
            self.label.config(text=f"Tiempo total: {int(hours):02}:{int(minutes):02}:{int(seconds):02}", fg="white")
        self.elapsed_time = 0
        self.start_time = None


if __name__ == "__main__":
    app = ChronometerApp()
    app.mainloop()
