'''
 !/usr/bin/env python
 -*- coding: utf-8 -*-
 @Time    : 2019/6/18 20:34
 @Author  : Tang
 @File    : data_2017-05-12_batchdata.py
 @Software: PyCharm
 @reference:https://github.com/rdbraatz/data-driven-prediction-of-battery-cycle-life-before-capacity-degradation
 @description:The data associated with each battery (cell) can be grouped into
    one of three categories: descriptors, summary, and cycle.
    Descriptors for each battery include charging policy, cycle life, barcode and
            channel. Note that barcode and channel are currently not available in
            the pkl files).
    Summary data include information on a per cycle basis, including cycle number,
    discharge capacity, charge capacity, internal resistance, maximum temperature,
    average temperature, minimum temperature, and chargetime.
    Cycle data include information within a cycle, including time, charge capacity,
    current, voltage, temperature, discharge capacity. We also include derived
    vectors of discharge dQ/dV, linearly interpolated discharge capacity and linearly
    interpolated temperature.
    每个电池的生命周期（cycle_life）不一样，每个电池的实验周期数（num of cycles)不一样
'''

import h5py
import scipy.io
import matplotlib.pyplot as plt
import numpy as np
import pickle


matFilename = 'H:\\Download\\2017-06-30_batchdata_updated_struct_errorcorrect.mat'
f = h5py.File(matFilename,'r+')
print(f.keys())

batch = f['batch']
print(batch.keys())

num_cells = batch['summary'].shape
print(num_cells)
print(f[batch['summary'][1,0]].keys())#第二个电池
print(f['batch']['cycle_life'].shape)#(48,1)
print(f['batch']['cycle_life'].dtype)#object
print(f['batch']['cycle_life'][0,0])
print(f[f['batch']['cycle_life'][0,0]].value)#==[[300]] .shape(1,1) float ：cycle_life每个电池都不一样大
print(np.hstack((f[f['batch']['cycle_life'][0,0]].value)))##[300]
print(batch['cycles'].shape)#(48,1)
cycles = f[f['batch']['cycles'][0,0]] #group object. use cycles['name']访问
print(cycles['I'].shape)#(326,1) 每个电池的实验循环次数 num of cycles of a cell.

