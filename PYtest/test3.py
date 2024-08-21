import time
import ADS1256
import RPi.GPIO as GPIO
import csv
from datetime import datetime

def ask_for_sps():
    print("Select SPS (Samples Per Second), default is 200:")
    print("1. 50 SPS")
    print("2. 60 SPS")
    print("3. 100 SPS")
    print("4. 200 SPS")
    print("5. 500 SPS")
    
    sps_choice = input("Choose an option (1-5, or press Enter to use 200 SPS): ")
    sps_options = [50, 60, 100, 200, 500]
    if sps_choice.isdigit() and 1 <= int(sps_choice) <= 5:
        return sps_options[int(sps_choice) - 1]
    else:
        return 200

def ask_for_channels():
    print("Which channels do you want to measure? (separated by comma, e.g., 0,1,2). Default is channels 0-5.")
    channels_input = input("Channels (or press Enter to use the default 0-5): ")
    if channels_input:
        channels = list(map(int, channels_input.split(',')))
        channels = [ch for ch in channels if 0 <= ch <= 7]  # Limit channels to 0-7
    else:
        channels = [0, 1, 2, 3, 4, 5]  # Default channels
    return channels

def ask_for_duration():
    duration_input = input("How long do you want to measure in minutes? (0 for continuous, or press Enter for 1 minute): ")
    return float(duration_input) * 60 if duration_input else 60

def ask_for_filename(channels):
    filename = input("Enter the file name (leave blank to use default name): ")
    if not filename:
        channels_str = "_".join(map(str, channels))
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"channels_{channels_str}_test_{timestamp}.csv"
    else:
        filename += ".csv"
    return filename

def ask_to_display_data():
    display = input("Do you want to display the collected data on the screen? (y/n): ")
    return display.lower() == 'y'

def main():
    try:
        ADC = ADS1256.ADS1256()
        ADC.ADS1256_init()

        sampling_freq = ask_for_sps()
        channels = ask_for_channels()
        duration = ask_for_duration()  # In seconds
        filename = ask_for_filename(channels)
        display_data = ask_to_display_data()

        interval = 1.0 / sampling_freq  # Time interval between each sample
        total_samples = int(duration * sampling_freq)  # Total number of samples

        start_perf = time.perf_counter()
        start_real_time = time.time()

        count = 0
        buffer = []

        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            header = ["T (s)"] + [f'Channel {ch}' for ch in channels] + ['T.real']
            writer.writerow(header)

            while count < total_samples:
                ADC_Value = ADC.ADS1256_GetSelectedChannels(channels)
                current_real_time = time.time()

                row = [round(count * interval, 6)] + ADC_Value + [current_real_time]

                if display_data and count % 100 == 0:  # Display every 100 samples
                    for i, ch in enumerate(channels):
                        print(f"Channel {ch}: {ADC_Value[i]:.6f} V")

                buffer.append(row)

                if len(buffer) >= 100:
                    writer.writerows(buffer)
                    buffer.clear()

                next_time = start_perf + (count + 1) * interval
                sleep_time = next_time - time.perf_counter()
                if sleep_time > 0:
                    time.sleep(sleep_time)

                count += 1

            if buffer:
                writer.writerows(buffer)

            end_real_time = time.time()
            end_perf = time.perf_counter()

        print(f'Start time (hh:mm:ss.ss): {time.strftime("%H:%M:%S", time.localtime(start_real_time))}')
        print(f'End time (hh:mm:ss.ss): {time.strftime("%H:%M:%S", time.localtime(end_real_time))}')
        print(f'Samples: {count} @ {sampling_freq} sps in {duration/60} mins')
        print(f'Time difference elapsed: {end_real_time - start_real_time:.6f} sec')
        print(f'Time elapsed perf_counter: {end_perf - start_perf:.6f} sec')

    except Exception as e:
        GPIO.cleanup()
        print(f"\r\nProgram terminated due to {e}")
        exit()
    finally:
        GPIO.cleanup()

if __name__ == "__main__":
    main()
