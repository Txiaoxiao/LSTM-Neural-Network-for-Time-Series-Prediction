import datetime as dt
import h5py
import numpy as np
import scipy
from scipy import io
import matplotlib.pyplot as plt
import pandas as pd
class Timer():

	def __init__(self):
		self.start_dt = None

	def start(self):
		self.start_dt = dt.datetime.now()

	def stop(self):
		end_dt = dt.datetime.now()
		print('Time taken: %s' % (end_dt - self.start_dt))

class Transform():
	##Tang
	def __init__(self,filepath,filename):
		self.matData =scipy.io.loadmat(filepath)[filename]
		self.filename = filename

	# def mat2csv(self, filepath):
	# 	features_struct =scipy.io.loadmat(filepath)
	# 	print(features_struct.keys())
	# 	features = features_struct['B0005']
	# 	print(len(features['cycle'][0,0][0]))#616
	# 	print(len(features['cycle'][0,0][0,0]))#4
	# 	print(np.squeeze(features['cycle'][0,0][0,0]['type']))#charge
	# 	print(np.squeeze(features['cycle'][0,0][0,1]['type']))##discharge
	# 	print(np.squeeze(features['cycle'][0, 0][0, 1]['data'][0,0]).dtype.names)##('Voltage_measured', 'Current_measured', 'Temperature_measured', 'Current_load', 'Voltage_load', 'Time', 'Capacity')
	def get_totalCycle(self):
		return len(self.matData['cycle'][0, 0][0])

	def plot_data(self, cycleNum, dataNameList):
		# visulisation of data specified by List: dataNameList
		fig1 = plt.figure()
		fig1.add_subplot(111)
		dataTime = self.get_data(cycleNum, 'Time')
		#print(dataTime)
		for dataName in dataNameList:
			data = self.get_data(cycleNum, dataName)
			print(data)
			plt.plot(dataTime, data, label=dataName)
		plt.xlabel('Time')
		plt.legend(loc='best')
	plt.grid()

	def get_data(self, cycleNum, dataName):
		#       cycle number: the index of cycles to extact(level 2)
		#       dataName: the name of data (Level 3)
		try:
			return np.squeeze(self.matData['cycle'][0, 0][0, cycleNum]['data'][0, 0][dataName])
		except:
			print('MatFileLoader-get_data: Wrong value for data column name')


	def format_data_to_dic(self, cycleNum):
		#        convert the multilevel data to a single level dictionary
		dataNameList = self.get_data_names(cycleNum)
		dic = {'cycleIndex': cycleNum, 'type': self.get_type, 'ambient_temperature': self.get_ambient_temperature}
		for dataName in dataNameList:
			dic[dataName] = self.get_data(cycleNum, dataName)
		return dic

	def get_type(self, cycleNum):
		return np.squeeze(self.matData['cycle'][0, 0][0, cycleNum]['type'])

	def get_time(self, cycleNum):
		return np.squeeze(self.matData['cycle'][0, 0][0, cycleNum]['time'])

	def get_ambient_temperature(self, cycleNum):
		return np.squeeze(self.matData['cycle'][0, 0][0, cycleNum]['ambient_temperature'])

	def get_data_names(self,cycleNum):
		return self.matData['cycle'][0,0][0,cycleNum]['data'][0,0].dtype.names

	def get_capacity(self):
		cyclelsit = list()
		capacityList = list()
		begin = True
		pre_capacty=0
		for cycleNum in range(self.get_totalCycle()):
			if self.get_data_names(cycleNum).__contains__('Capacity'):
				capacity = self.get_data(cycleNum,'Capacity').tolist()
				capacityList.append(capacity)
				#capacityList.append([cycleNum,capacity])
		return capacityList

def B_Mat2Csv():
	dataNames = {'B0005','B0006','B0007','B0018'}
	# columns = ['cycle','capacity']
	columns = ['capacity']
	for file in dataNames:
		filepath = '../data/'+file+'.mat'
		print(filepath)
		trans = Transform(filepath,file)
		capacityList = trans.get_capacity()
		#print(capacityList)
		data = pd.DataFrame(columns=columns,data=capacityList)
		data.to_csv('../data/'+file+'_cycle_capacity.csv',index=False)

if __name__ == '__main__':
	# filepath = '../data/B0005.mat'
	# trans = Transform(filepath)
	#data = trans.mat2csv(filepath)
	#dataNameList = trans.get_data_names(cycleNum=24)
	#print(dataNameList)
	# trans.plot_data(1,dataNameList)
	# x,y = trans.get_capacity()
	# print(y)
	# plt.plot(x,y)
	# plt.show()


	# capacitylist = trans.get_capacity()
	# #print(capacitylist)
	# columns = {'cycle','capacity','prediction'}
	# data = pd.DataFrame(columns=columns,data= capacitylist)
	# print(data)
	# data.to_csv('../data/B0005_cycle_capacity.csv',encoding='gbk')

	#B_Mat2Csv()

	fp = '../data/2017-06-30_batchdata.mat'
	mat=h5py.File(fp)
	print(mat.keys())