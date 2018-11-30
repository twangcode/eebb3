import data_parser as dp
from os import listdir
from os.path import isfile, join
import numpy as np
import pandas as pd
import csv
import tuotools as tt
import time

FILEPATH = '/var/opt/lufgroup/apps/nova_lufcomp/novaStats_ma/data'

def scanner(input_filename, output_filename, entries, exits):
	#	read bb3 names and slippage into dataframe:
	bb3_list = pd.read_csv(input_filename, names=['name', 'slippage'])
	
	total_files = float(len(bb3_list.index))
	count = 0
	
	with open(output_filename, 'wb') as fout:
		writer = csv.writer(fout)
		for index, row in bb3_list.iterrows():
			count += 1
			for entry in entries:
				for exit in exits:
					try:
						(sr, profit, num_trades) = dp.spread(join(FILEPATH, row['name'])).EE_Sharpe_Ratio(entry, exit, float(row['slippage']))
						if sr > 2:
							print row['name'], (entry, exit), (sr, profit, num_trades), "%6.2f" % (count/total_files * 100) + '%'
							writer.writerow([row['name'][2:-5], entry, exit, entry*exit, '%6.2f' % sr, profit, num_trades, profit/num_trades*2.])
					except:
						pass
	fout.close()

def main():
	start_time = time.time()
	
	scanner('input/list_BB3_TEN.csv', 'output/BB3_filtered_TEN.csv', [1, 1.5, 2, 2.5, 3, 3.5, 4], [0.5, 0.75, 1])
	
	stop_point_1 = time.time()
	print 'BB3_TEN time is: ', '%6.2f seconds.' % (stop_point_1 - start_time) 

	scanner('input/list_BB3_FIX.csv', 'output/BB3_filtered_FIX.csv', [2, 3, 4], [0.5, 0.75, 1])
	
	stop_point_2 = time.time()
	print 'BB3_FIX time is: ', '%6.2f seconds.' % (stop_point_2 - stop_point_1) 
	
	scanner('input/list_BB3_FLY.csv', 'output/BB3_filtered_FLY.csv', [2, 3, 4], [0.5, 0.75, 1])
	
	stop_point_3 = time.time()
	print 'BB3_FLY time is: ', '%6.2f seconds.' % (stop_point_3 - stop_point_2) 
	
	scanner('input/list_BB3.csv', 'output/BB3_filtered.csv', [2, 3, 4], [0.5, 0.75, 1])
	
	print 'BB3 time is: ', '%6.2f seconds.' % (time.time() - stop_point_3) 	
	
if __name__ == '__main__':
	main()

	
	 
