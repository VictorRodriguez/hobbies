# Examples of regression algorithms


## simple_2_points

This algorithm calculate the dist between the  new data - STDV and the prev data + STDV , example (LIB in this example):

![alt text](https://github.com/VictorRodriguez/hobbies/blob/master/regresion_algorithms/example_images/image.png)

Example if HIB with example_data/data.csv

![alt text](https://github.com/VictorRodriguez/hobbies/blob/master/regresion_algorithms/example_images/image_hib.png)

## Time Series Forecasting

The Long Short-Term Memory recurrent neural network has the promise of learning long sequences of observations. It seems a perfect match for time series forecasting, and in fact, it may be.

The change that i do is to add the STDV as part of the limit to define a valid regression or not 

Source : https://machinelearningmastery.com/time-series-forecasting-long-short-term-memory-network-python/

![alt text](https://github.com/VictorRodriguez/hobbies/blob/master/regresion_algorithms/example_images/image_time-series-LIB.png)

### TODO

* Explore : https://github.com/jaungiers/LSTM-Neural-Network-for-Time-Series-Prediction

