import time

def chronometer ():
    print("presiona aqui")
    input()
    print("Inicio")
    start_time = time.time()

    try:
        while True:
            elapsed_time = time.time() - start_time
            minutes, seconds = divmod(elapsed_time, 60)
            hours, minutes = divmod(minutes, 60)
            print(f'\r{int(hours):02}:{int(minutes):02}:{int(seconds):02}', end="")
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nCronometro detenido")
        end_time = time.time()
        total_time = end_time - start_time
        minutes, seconds = divmod(total_time, 60)
        hours, minutes = divmod(minutes, 60)
        print(f"Tiempo total: {int(hours):02}:{int(minutes):02}:{int(seconds):02}")


if __name__ == "__main__":
    chronometer()