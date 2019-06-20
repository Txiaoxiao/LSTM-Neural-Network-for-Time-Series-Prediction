# LSTM Neural Network for Battery Remaining Useful Lifetime(RUL) Prediction

LSTM built using the Keras Python package to predict battery remaining using lifetime(RUL).


2019.06.20: Only data processing part is working.

##.py file
#### utils.py: 
    transform .mat to .csv. of NASA battery data.
#### data_2017_06_30_batchdata.py:
    transform .mat to .csv of data from https://github.com/rdbraatz/data-driven-prediction-of-battery-cycle-life-before-capacity-degradation/blob/master. 
    Paper: "data-driven-prediction-of-battery-cycle-life-before-capacity-degradation"
    

## Requirements

Install requirements.txt file to make sure correct versions of libraries are being used.

* Python 3.5.x
* TensorFlow 1.10.0
* Numpy 1.15.0
* Keras 2.2.2
* Matplotlib 2.2.2