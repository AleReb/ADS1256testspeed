import time
import ADS1256
import RPi.GPIO as GPIO
import csv

try:
    ADC = ADS1256.ADS1256()
    ADC.ADS1256_init()

    samples = 500*600
    data = {'channel_0': [], 'channel_1': [], 'channel_2': []}
    
    start_time = time.time()
    
    for _ in range(samples):
        ADC_Value = ADC.ADS1256_GetAll()
        data['channel_0'].append(ADC_Value[0]*5.0/0x7fffff)
        data['channel_1'].append(ADC_Value[1]*5.0/0x7fffff)
        data['channel_2'].append(ADC_Value[2]*5.0/0x7fffff)
    
    end_time = time.time()
    total_time = end_time - start_time

    with open('adc_values.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Channel 0', 'Channel 1', 'Channel 2'])
        for i in range(samples):
            writer.writerow([data['channel_0'][i], data['channel_1'][i], data['channel_2'][i]])
    
    print(f"Data collection and saving completed in {total_time:.2f} seconds")

except Exception as e:
    GPIO.cleanup()
    print(f"\r\nProgram end due to {e}")
    exit()
