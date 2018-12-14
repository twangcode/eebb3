import pandas as pd
import time


filename = 'output/symbol_list.data'

# Read the symbol_list.data file into a dictionary for ADR factor look up
def generate_ratio_dict(data_file='output/symbol_list.data'):
	df = pd.read_csv(data_file, header=None, sep=' ', names=['product', 'factor'], index_col=['product'])
	ratio_dict = df.to_dict()
	return ratio_dict['factor']

# Look up a product in the ADR factor dictionary
def look_up(prod, ratio_dict):
	if prod in ratio_dict:
		return float(ratio_dict[prod])
	else:
		return 'nan'

def look_up_file(prod):
	df = pd.read_csv('output/symbol_list.data', header=None, sep=' ', names=['product', 'factor'], index_col=['product'])
	return df.loc[prod]['factor']

def main():
	start_time = time.time()
	ratio_dict = generate_ratio_dict()
	for symbol in ratio_dict.keys():
		look_up(symbol, ratio_dict)
	runtime = time.time() - start_time

	start_time_2 = time.time()
	for symbol in ratio_dict.keys():
		print look_up_file(symbol)
	runtime_2 = time.time() - start_time
	
	print "\nFirst method total runtime is: {:3f} seconds\n".format(runtime)
	print "\nSecond method total runtime is: {:3f} seconds\n".format(runtime_2)
	
if __name__ == "__main__":
	main()
	

	
