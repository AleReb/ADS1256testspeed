
# Recolección de Datos ADC con Raspberry Pi 

Este proyecto recoge datos analógicos de varios canales utilizando el módulo ADC ADS1256 conectado a un Raspberry Pi. Los datos recopilados se guardan en un archivo CSV para su posterior análisis. El script ofrece opciones para configurar la tasa de muestreo, los canales a medir y la duración de la recolección de datos. También proporciona una opción para mostrar los datos en tiempo real.

## Requisitos

- Raspberry Pi (cualquier modelo con soporte GPIO)
- Módulo ADC ADS1256
- Python 3
- Biblioteca ADS1256
- Biblioteca RPi.GPIO

## Configuración

1. **Conecta el módulo ADS1256 al Raspberry Pi** siguiendo las instrucciones del fabricante.

2. **Instala las bibliotecas de Python necesarias** si no están ya instaladas:
    ```bash
    sudo apt-get update
    sudo apt-get install python-pip
    sudo pip install RPi.GPIO
    sudo pip install spidev
    ```

3. **Descarga la biblioteca ADS1256** desde su [repositorio](https://github.com/AleReb/ADS1256testspeed).

4. **Clona este repositorio** en tu Raspberry Pi:
    ```bash
    git clone https://github.com/AleReb/ADS1256testspeed.git
    cd ADS1256testspeed/PYtest
    ```

## Uso

1. **Ejecuta el script** para comenzar a recopilar datos:
    ```bash
    sudo python test3.py
    ```

2. **El script te pedirá las siguientes configuraciones:**
   - **Tasa de Muestreo (SPS):** Puedes elegir entre 50 SPS, 60 SPS, 100 SPS, 200 SPS o 500 SPS. El valor predeterminado es 200 SPS si no se selecciona ninguna opción.
   - **Canales a Medir:** Ingresa los canales que deseas medir (por ejemplo, 0,1,2). Si no se ingresan canales, se usarán por defecto los canales 0 a 5.
   - **Duración:** Ingresa el tiempo en minutos para la recolección de datos (por ejemplo, 1 para 1 minuto). Ingresa `0` para medición continua. El valor predeterminado es 1 minuto si no se ingresa un tiempo.
   - **Nombre del Archivo de Salida:** Especifica un nombre para el archivo CSV de salida. Si se deja en blanco, se generará un nombre predeterminado basado en los canales usados y la fecha y hora actuales.
   - **Visualización de Datos en Tiempo Real:** Puedes elegir mostrar los datos en tiempo real en la pantalla.

3. **El script recopilará datos** según tus configuraciones y los guardará en un archivo CSV.

4. **Los datos recopilados se guardan en un archivo CSV** con un nombre especificado por ti o generado por el script. El archivo CSV tendrá un formato similar a este:
    ```
    T (s), Canal 0, Canal 1, Canal 2, T.real
    0.000001, value0_0, value0_1, value0_2, 1626884190.123456
    0.000002, value1_0, value1_1, value1_2, 1626884190.223456
    ...
    ```

5. **Después de completar la recolección de datos**, el script mostrará el tiempo total que tomó la recolección y el número total de muestras recopiladas.

## Explicación del Script
El script `test3.py` realiza los siguientes pasos:

1. **Inicialización:** El script inicializa el módulo ADC ADS1256 conectado al Raspberry Pi. Luego solicita al usuario varias configuraciones, incluyendo la tasa de muestreo, los canales a medir, la duración de la medición, el nombre del archivo de salida y si desea ver los datos en tiempo real.

2. **Recolección de Datos:** El script recopila datos de los canales seleccionados, convirtiendo los valores crudos del ADC en valores de voltaje. Periódicamente guarda los datos recopilados en un archivo CSV, asegurando que los datos no se pierdan durante sesiones largas de medición.

3. **Salida:** Los datos recopilados se guardan en un archivo CSV, que se puede analizar posteriormente. Al final de la medición, el script muestra la duración total y el número de muestras recolectadas.
## **Cambios Realizados**

### **Modificaciones en ADS1xx.py:**

- **Función `ADS1256_GetSelectedChannels`:** Se añadió una nueva función llamada `ADS1256_GetSelectedChannels` que permite leer únicamente los canales especificados en una lista. Esto mejora la eficiencia del código al evitar la lectura innecesaria de todos los canales cuando solo se necesitan algunos.

### **Modificaciones en test4.py:**

- **Selección Dinámica de Canales:** El script `test4.py` ahora utiliza la función `ADS1256_GetSelectedChannels` para leer únicamente los canales solicitados por el usuario, mejorando significativamente el rendimiento y reduciendo el tiempo de ejecución para configuraciones con pocos canales, se mantiene el read all en ads1256.py para hacer purebas rapidas con el codigo main.py.
- **Interfaz de Usuario Mejorada:** El script solicita al usuario que ingrese los canales a medir, lo que permite una mayor flexibilidad y personalización en la recolección de datos.
- **Optimización de Escritura en CSV:** Los datos recolectados se almacenan en un buffer y se escriben en el archivo CSV en lotes, lo que reduce el impacto en el rendimiento y asegura que los datos no se pierdan en sesiones largas de medición.

## Manejo de Errores

El script incluye un bloque try-except para manejar cualquier excepción que pueda ocurrir durante la ejecución. Si ocurre un error, limpia los pines GPIO y muestra el mensaje de error.

## Ejemplo de Salida
Start time (hh:mm:ss.ss): 23:50:52
End time (hh:mm:ss.ss): 23:55:52
Samples: 150000 @ 500 sps in 5.0 mins
Time difference elapsed: 300.001060 sec
Time elapsed perf_counter: 300.001065 sec

