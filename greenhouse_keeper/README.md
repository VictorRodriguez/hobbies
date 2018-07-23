# greenhouse_keeper
A really simple greenhouse keeper 

The idea is to take care of a backyard garden with less than 20 USD: 

    1. Get forecast from my current location
    2. Take desitions based on ML prediciton systems
    3. Send signals to remote actuator by WiFi signal

Install https://github.com/ZeevG/python-forecast.io

    ```
    pip install python-forecastio
    ```

Run as: 

    ```
    optional arguments:
    
    -h, --help       show this help message and exit
    --lat LATITUD
    --long LONGITUD
    --plot
    ```
Example:

    ```
    python forecast.py --lat 20.751902 --long -103.438930 --plot
    ```
![alttext](https://github.com/VictorRodriguez/greenhouse_keeper/blob/master/figure_1.png)


