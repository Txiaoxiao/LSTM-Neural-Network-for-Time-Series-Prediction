'''
 !/usr/bin/env python
 -*- coding: utf-8 -*-
 @Time    : 2019/6/18 20:34
 @Author  : Tang
 @File    : data_2017-06-30_batchdata.py
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
import csv
import pandas as pd

def main_try(matFilename):
    f = h5py.File(matFilename, 'r+')
    print(f.keys())

    batch = f['batch']
    print(batch.keys())

    num_cells = batch['summary'].shape
    print(num_cells)
    print(f[batch['summary'][1, 0]].keys())  # 第二个电池
    print(f['batch']['cycle_life'].shape)  # (48,1)
    print(f['batch']['cycle_life'].dtype)  # object
    print(f['batch']['cycle_life'][0, 0])
    print(f[f['batch']['cycle_life'][0, 0]].value)  # ==[[300]] .shape(1,1) float ：cycle_life每个电池都不一样大
    print(np.hstack((f[f['batch']['cycle_life'][0, 0]].value)))  ##[300]
    print(batch['cycles'].shape)  # (48,1)
    cycles = f[f['batch']['cycles'][0, 0]]  # group object. use cycles['name']访问
    print(cycles['I'].shape)  # (326,1) 每个电池的实验循环次数 num of cycles of a cell.

def rul_csv(matFilename):
    f = h5py.File(matFilename, 'r+')
    print(f.keys())

    batch = f['batch']
    print(batch.keys())
    num_cells = batch['summary'].shape[0]
    bat_dict = {}
    for i in range(num_cells):
        cl = f[batch['cycle_life'][i, 0]].value
        policy = f[batch['policy_readable'][i, 0]].value.tobytes()[::2].decode()
        summary_IR = np.hstack(f[batch['summary'][i, 0]]['IR'][0, :].tolist())
        summary_QC = np.hstack(f[batch['summary'][i, 0]]['QCharge'][0, :].tolist())
        summary_QD = np.hstack(f[batch['summary'][i, 0]]['QDischarge'][0, :].tolist())
        summary_TA = np.hstack(f[batch['summary'][i, 0]]['Tavg'][0, :].tolist())
        summary_TM = np.hstack(f[batch['summary'][i, 0]]['Tmin'][0, :].tolist())
        summary_TX = np.hstack(f[batch['summary'][i, 0]]['Tmax'][0, :].tolist())
        summary_CT = np.hstack(f[batch['summary'][i, 0]]['chargetime'][0, :].tolist())
        summary_CY = np.hstack(f[batch['summary'][i, 0]]['cycle'][0, :].tolist())
        summary = {'IR': summary_IR, 'QC': summary_QC, 'QD': summary_QD, 'Tavg':
            summary_TA, 'Tmin': summary_TM, 'Tmax': summary_TX, 'chargetime': summary_CT,
                   'cycle': summary_CY}
        # print(summary.keys())
        cycles = f[batch['cycles'][i, 0]]
        # cycle_dict = {}
        # for j in range(cycles['I'].shape[0]):##此处有问题
        #     I = np.hstack((f[cycles['I'][j, 0]].value))
        #     Qc = np.hstack((f[cycles['Qc'][j, 0]].value))
        #     Qd = np.hstack((f[cycles['Qd'][j, 0]].value))
        #     Qdlin = np.hstack((f[cycles['Qdlin'][j, 0]].value))
        #     T = np.hstack((f[cycles['T'][j, 0]].value))
        #     Tdlin = np.hstack((f[cycles['Tdlin'][j, 0]].value))
        #     V = np.hstack((f[cycles['V'][j, 0]].value))
        #     dQdV = np.hstack((f[cycles['discharge_dQdV'][j, 0]].value))
        #     t = np.hstack((f[cycles['t'][j, 0]].value))
        #     cd = {'I': I, 'Qc': Qc, 'Qd': Qd, 'Qdlin': Qdlin, 'T': T, 'Tdlin': Tdlin, 'V': V, 'dQdV': dQdV, 't': t}
        #     cycle_dict[str(j)] = cd

        cell_dict = {'cycle_life': cl, 'charge_policy': policy, 'summary': summary}#, 'cycles': cycle_dict
        key = 'b2c' + str(i)
        bat_dict[key] = cell_dict
    print(bat_dict.keys())
    # plt.plot(bat_dict['b2c0']['summary']['cycle'], bat_dict['b2c0']['summary']['QD'])
    # plt.show()

# DONE:
#  write to csv file. 11 columns.
#  header = ['cell','cycle_life','charge_policy','cycle','IR','Tavg','Tmin','Tmax','chargetime','QD',]
#  cell,cycle_life,cycle,charge_policy,IR,Tavg,Tmin,Tmax,chargetime,QC,QD
#     csv_file='../data/2017_06_30_batchdatainrow.csv'

    for i in range(len(bat_dict)):
        csv_file='../data/2017_06_30_cell{0}_data.csv'.format(i)
        cell_key = 'b2c'+str(i)
        writeToCSV(csv_file,bat_dict[cell_key],i)
    writeToCSV(csv_file,bat_dict['b2c0'],0)

def soc_csv(matFilename):
    f = h5py.File(matFilename, 'r+')
    print('keys: ',f.keys())
    batch = f['batch']
    print('batch_keys: ',batch.keys())
    cycles = batch['cycles']
    print('shape of batch.cycles:',cycles.shape)

    cycle_0 = f[cycles[0,0]]
    print('cycle_0_keys: ',cycle_0.keys())
    Qdlin = cycle_0['Qdlin']
    print('cycle_0_Qdlin: ',Qdlin)



def writeToCSV(csv_file,cell_data,cel_num):
    cell = cel_num
    cycle_life =int(cell_data['cycle_life'])
    charge_policy = str(cell_data['charge_policy'])
    summary = cell_data['summary']
    cycle = summary['cycle']
    IR = summary['IR']
    Tavg = summary['Tavg']
    Tmin = summary['Tmin']
    Tmax = summary['Tmax']
    chargetime = summary['chargetime']
    QC = summary['QC']
    QD = summary['QD']

    r_num = cycle.size#row number
    lable1 = QD[1:].tolist()
    lable1.append(lable1[-1])
    cell_list = list()
    for i in range(r_num):
        cell_list.append([cell,cycle_life,charge_policy,cycle[i],IR[i],Tavg[i],Tmin[i],Tmax[i],chargetime[i],QD[i],lable1[i]])

    header = ['cell','cycle_life','charge_policy','cycle','IR','Tavg','Tmin','Tmax','chargetime','QD','label']

    data = pd.DataFrame(columns=header,data=cell_list)
    data.to_csv(csv_file,index=False)

def writeDicToCsvInRows(csv_file, csv_columns, bat_dict):
    with open(csv_file,'w') as csvfile:
        for cell,cell_dict in bat_dict.items():
            csvfile.write('cell,{0}\n'.format(cell))
            csvfile.write('cycle_life,{0}\n'.format(cell_dict['cycle_life']))
            csvfile.write('charge_policy,{0}\n'.format(cell_dict['charge_policy']))
            dict_data = cell_dict['summary']
            for k, v in dict_data.items():
                csvfile.write('{0},{1}\n'.format(k, v.tolist()))
    return

if __name__ == '__main__':

    matFilename = 'H:\\Data\\2017-06-30_batchdata_updated_struct_errorcorrect.mat'
    # rul_csv(matFilename)
    #test()
    soc_csv(matFilename)

