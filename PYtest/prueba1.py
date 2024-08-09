# -*- coding: utf-8 -*-

import time
import ADS1256
import RPi.GPIO as GPIO
import csv
from datetime import datetime

def ask_for_sps():
    print("Selecciona los SPS por defecto 200 (Samples Per Second):")
    print("1. 50 SPS")
    print("2. 60 SPS")
    print("3. 100 SPS")
    print("4. 200 SPS")
    print("5. 500 SPS")
    
    sps_choice = input("Elige una opcion (1-5, o presiona Enter para usar 200 SPS): ")
    sps_options = [50, 60, 100, 200, 500]
    if sps_choice.isdigit() and 1 <= int(sps_choice) <= 5:
        return sps_options[int(sps_choice) - 1]
    else:
        return 200

def ask_for_channels():
    print("Que canales deseas medir? (separados por coma, por ejemplo: 0,1,2). Si no seleccionas ninguno, se mediran los canales 0 a 5.")
    channels_input = input("Canales (o presiona Enter para usar los canales por defecto 0-5): ")
    if channels_input:
        channels = list(map(int, channels_input.split(',')))
        channels = [ch for ch in channels if 0 <= ch <= 7]  # Limita los canales de 0 a 7
    else:
        channels = [0, 1, 2, 3, 4, 5]  # Canales por defecto
    return channels

def ask_for_duration():
    duration_input = input("Cuanto tiempo deseas medir en minutos? (0 para continuo, o presiona Enter para 1 minuto por defecto): ")
    return float(duration_input) if duration_input else 1

def ask_for_filename(channels):
    filename = input("Introduce el nombre del archivo (deja en blanco para usar nombre por defecto): ")
    if not filename:
        channels_str = "_".join(map(str, channels))
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"canales_{channels_str}_prueba_{timestamp}.csv"
    else:
        filename += ".csv"
    return filename

def ask_to_display_data():
    display = input("Deseas ver los datos recolectados en pantalla? (s/n): ")
    return display.lower() == 's'

def save_data_interval(data, filename, channels):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        header = [f'Channel {ch}' for ch in channels]
        writer.writerow(header)
        samples = len(data[channels[0]])
        for i in range(samples):
            row = [data[ch][i] for ch in channels]
            writer.writerow(row)
    print(f"Datos guardados en {filename}")

try:
    ADC = ADS1256.ADS1256()
    ADC.ADS1256_init()
    
    sps = ask_for_sps()
    channels = ask_for_channels()
    duration = ask_for_duration()
    filename = ask_for_filename(channels)
    display_data = ask_to_display_data()
    
    continuous = duration == 0
    sample_rate = int(sps)
    total_samples = sample_rate * 60 * duration if not continuous else float('inf')

    data = {ch: [] for ch in channels}
    
    start_time = time.time()
    end_time = start_time + (duration * 60)  # Tiempo final basado en la duración en minutos
    next_interval_time = start_time + 30
    save_interval = 10 * 60  # 10 minutos
    file_index = 1

    samples_collected = 0

    while continuous or time.time() < end_time:
        ADC_Value = ADC.ADS1256_GetAll()
        for ch in channels:
            value = ADC_Value[ch] * 5.0 / 0x7fffff
            data[ch].append(value)
            if display_data:
                print(f"Channel {ch}: {value:.6f} V")
        
        samples_collected += 1
        
        if time.time() >= next_interval_time:
            print(f"Datos recolectados hasta ahora: {samples_collected}")
            next_interval_time += 30
        
        if (time.time() - start_time) >= save_interval:
            save_data_interval(data, filename, channels)
            data = {ch: [] for ch in channels}
            start_time = time.time()
            file_index += 1
    
    # Guardar los datos restantes
    if samples_collected > 0:
        save_data_interval(data, filename, channels)

    total_time = time.time() - start_time
    print(f"Recoleccion completada en {total_time:.2f} segundos")
    print(f"Total de muestras recolectadas: {samples_collected}")

except Exception as e:
    GPIO.cleanup()
    print(f"\r\nProgram end due to {e}")
    exit()
