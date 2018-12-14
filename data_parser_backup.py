import pandas as pd 
import numpy as np 
from os import listdir
from os.path import isfile, join
from datetime import datetime

FILEPATH = '/var/opt/lufgroup/apps/nova_lufcomp/novaStats_ma/data'
OLDPATH = '/var/opt/lufgroup/apps/nova_lufcomp/novaStats_ma/data_full_20181117'

# Parse 'S:BB3xxx.data' file
def data_reader(filename):
	df = pd.read_csv(filename, sep=' ', header=None, parse_dates=[[0,1]], \
		usecols=[0, 1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29], index_col='0_1')
	df.columns = ['N_points', 'Price', \
					'6H_EMA', '6H_SMA', '6H_STDDEV', \
					'12H_EMA', '12H_SMA', '12H_STDDEV', \
					'2D_EMA', '2D_SMA', '2D_STDDEV', \
					'5D_EMA', '5D_SMA', '5D_STDDEV']
	df.index.names = ['Date']
	return df

class spread():
	def __init__(self, filename):
		self.name = filename[2:-5]
		old_data = data_reader(join(OLDPATH, filename))
		new_data = data_reader(join(FILEPATH, filename))
		self.data = pd.concat([old_data, new_data]).drop_duplicates().last('6M')
	
	def print_name(self):
		print self.name
	def get_name(self):
		return self.name
	def print_data(self):
		print self.data
	def get_data(self, start_dt=None, end_dt=None):
		if not start_dt and not end_dt:
			start = pd.to_datetime(start_dt)
			end = pd.to_datetime(end_dt)
			return self.data[start_dt:end_dt]
		else:
			 return self.data

	def EE_Sharpe_Ratio(self, entry, exit, slippage=10):
		data = self.data
		data['UpperBand'] = data['2D_EMA'] + data['2D_STDDEV'] * entry
		data['LowerBand'] = data['2D_EMA'] - data['2D_STDDEV'] * entry
		data['LongExit'] = data['LowerBand'] + data['2D_STDDEV'] * entry * exit
		data['ShortExit'] = data['UpperBand'] - data['2D_STDDEV'] * entry * exit
		# generate trades according to bands
		data['Position'] = None
		data['Position'] = np.where(data['Price'] > (data['UpperBand'] + slippage), -1, None)
		data['Position'] = np.where(data['Price'] < (data['LowerBand'] - slippage), 1, data['Position'])
		data['Position'] = np.where((data['Price'] > (data['LongExit'] + slippage)) & (data['Price'] < (data['ShortExit'] - slippage)), 0, data['Position'])
		data['Position'] = data['Position'].fillna(method='ffill')
		data['Position'] = data['Position'].fillna(0)
		data['Trade'] = data['Position'] - data['Position'].shift(1)
		data['Trade'] = np.where(data['Trade'].isnull(), data['Position'], data['Trade'])
		num_trades = data['Trade'].abs().sum()
		# calculate cumulated pnl:
		data['Cost'] = data['Trade'] * data['Price']
		data['MarketValue'] = data['Price'] * data['Position']
		data['cumPnL'] = data['MarketValue'] - data['Cost'].cumsum()
		total_profit = data['cumPnL'].tail(1).values[0]
		# calculate pnl and sharpe ratio
		data['PnL'] = data['cumPnL'] - data['cumPnL'].shift(1)
		sharpeRatio = data['PnL'].mean() / data['PnL'].std() * np.sqrt(len(data))
		return sharpeRatio, total_profit, num_trades

def test_run():
	filename = 'S:BB3_TEN:GBL-ZN+XE6.data'
	spread(filename).print_data()

if __name__ == '__main__':
	test_run()
