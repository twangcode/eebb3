import data_parser as dp
from os import listdir
from os.path import isfile, join
import numpy as np
import pandas as pd
import csv
import tuotools as tt
import time

FILEPATH = '/var/opt/lufgroup/apps/nova_lufcomp/novaStats_ma/data'

def generate_factor_dict(dict_location):
	df = pd.read_csv(dict_location, header=None, sep=' ', names=['product', 'factor'], index_col=['product'])
	prod_dict = df.to_dict()
	return prod_dict['factor']

def look_up(prod, prod_dict):
	factor = 1.0
	temp_factor = ''
	while not prod[0].isalpha():
		temp_factor = temp_factor + prod[0]
		prod = prod[1:] 
	if prod in prod_dict:
		if temp_factor:
			return float(prod_dict[prod])
		else:
			return float(prod_dict[prod])
	else:
		return 0
	
def normalize(ratio_list):
	min_ratio = min(ratio_list)
	return [round(x /  min_ratio, 3) for x in ratio_list] 

def get_ratio(filename, prod_dict):
	# extract spread name
	spread_name = filename.split(':')[2][:-5]
	prod_list = spread_name.replace('+', ' ').replace('-', ' ').split(' ')
	ratio_list = []
	for prod in prod_list:
		if look_up(prod, prod_dict):
			ratio_list.append(look_up(prod, prod_dict))
	if ratio_list:
		ratio_list = normalize(ratio_list)
	return ratio_list
	
def scanner(input_filename, output_filename, entries, exits):
	#	generate factor dictionary for factor ratio calculation
	prod_dict = generate_factor_dict('output/symbol_list.data')
	#	read bb3 names and slippage into dataframe:
	bb3_list = pd.read_csv(input_filename, names=['name', 'slippage'])
	
	total_files = float(len(bb3_list.index))
	count = 0
	
	with open(output_filename, 'wb') as fout:
		writer = csv.writer(fout)
		for index, row in bb3_list.iterrows():
			count += 1
			test_spread = dp.spread(row['name'])
			ratio_list = get_ratio(row['name'], prod_dict)
			for entry in entries:
				for exit in exits:
					try:
						(sr, profit, num_trades) = test_spread.EE_Sharpe_Ratio(entry, exit, float(row['slippage']))
						if sr > 2:
							print row['name'], (entry, exit), (sr, profit, num_trades), "%6.2f" % (count/total_files * 100) + '%'
							writer.writerow([row['name'][2:-5], entry, entry*exit, '%6.2f' % sr, profit, num_trades, profit/num_trades*2., row['slippage'], ratio_list])
					except:
						pass
	fout.close()

def main():
	start_time = time.time()
	
	scanner('input/list_BB3_TEN.csv', 'output/BB3_filtered_TEN.csv', [1, 1.5, 2, 2.5, 3, 3.5, 4], [0.5, 0.75, 1])
	
	stop_point_1 = time.time()
	print 'BB3_TEN time is: ', '%6.2f seconds.' % (stop_point_1 - start_time) 

	scanner('input/list_BB3_FIX.csv', 'output/BB3_filtered_FIX.csv', [1, 1.5, 2, 2.5, 3, 3.5, 4], [0.5, 0.75, 1])
	
	stop_point_2 = time.time()
	print 'BB3_FIX time is: ', '%6.2f seconds.' % (stop_point_2 - stop_point_1) 
	
	scanner('input/list_BB3_FLY.csv', 'output/BB3_filtered_FLY.csv', [1, 1.5, 2, 2.5, 3, 3.5, 4], [0.5, 0.75, 1])
	
	stop_point_3 = time.time()
	print 'BB3_FLY time is: ', '%6.2f seconds.' % (stop_point_3 - stop_point_2) 
	
	scanner('input/list_BB3.csv', 'output/BB3_filtered.csv', [1, 1.5, 2, 2.5, 3, 3.5, 4], [0.5, 0.75, 1])
	
	print 'BB3 time is: ', '%6.2f seconds.' % (time.time() - stop_point_3) 	
	
def main_2():
	print get_ratio('S:BB3_FIX:2.0US5Y-US3Y-GE18.data')

if __name__ == '__main__':
	main()

	
	 
