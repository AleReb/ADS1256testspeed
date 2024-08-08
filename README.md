# ADC Data Collection with Raspberry Pi

This project collects analog data from three channels using the ADS1256 ADC connected to a Raspberry Pi. The collected data is then saved into a CSV file for further analysis.

## Requirements

- Raspberry Pi (any model with GPIO support)
- ADS1256 ADC module
- Python 3
- ADS1256 library
- RPi.GPIO library

## Setup

1. **Connect the ADS1256 module to the Raspberry Pi** following the manufacturer's instructions.

2. **Install the necessary Python libraries** if not already installed:
    ```bash
    pip install RPi.GPIO
    ```

3. **Download the ADS1256 library** from its [repository]([https://github.com/AleReb/ADS1256testspeed](https://github.com/AleReb/ADS1256testspeed)).

4. **Clone this repository** to your Raspberry Pi:
    ```bash
    git clone https://github.com/AleReb/ADS1256testspeed.git
    cd ADS1256testspeed
    ```

## Usage

1. **Run the script** to start collecting data:
    ```bash
    python test.py
    ```

2. **The script will collect data from three channels** for a duration of approximately 10 minutes (500 samples per second for 600 seconds).

3. **The collected data is saved into `adc_values.csv`** in the following format:
    ```
    Channel 0, Channel 1, Channel 2
    value0_0, value0_1, value0_2
    value1_0, value1_1, value1_2
    ...
    ```

## Script Explanation

The `test.py` script performs the following steps:

1. Initializes the ADS1256 ADC module.
2. Sets the number of samples to be collected (500 samples per second for 600 seconds).
3. Collects data from three channels and converts it to voltage values.
4. Saves the collected data into a CSV file (`adc_values.csv`).
5. Prints the total time taken for data collection and saving.

## Error Handling

The script includes a try-except block to handle any exceptions that may occur during execution. If an error occurs, it cleans up the GPIO pins and prints the error message.

## Example Output

After running the script, you should see an output similar to this:
