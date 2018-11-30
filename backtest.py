import sys, getopt
import data_parser as dp
import pandas as pd

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

def main(argv):
	
### read filename, slippage, sharpe_threshold from argument:	
	filename = ''
	slippage = 10
	sharpe_threshold = 0
	try:
		opts, args = getopt.getopt(argv, 'hi:s:r:')
	except getopt.GetoptError:
		print 'backtest.py -i filename -s slippage -r sharpe_threshold'
		sys.exit(2)
	
	for opt, arg in opts:
		if opt == '-h':
			print 'backtest.py -i filename -s slippage -r sharpe_threshold'
			sys.exit(1)
		elif opt == '-i':
			filename = arg
		elif opt == '-s':
			slippage = arg
		elif opt == '-r':
			sharpe_threshold = arg
		else:
			usage()
			sys.exit(2)

### generate factor dict for ratios:
	prod_dict = generate_factor_dict('output/symbol_list.data')
	ratio_list = get_ratio(filename, prod_dict)
	print ratio_list
			
### Backtest starts:
	entries = [1, 1.5, 2, 2.5, 3, 3.5, 4]
	exits = [0.5, 0.75, 1.0]
	print 'File name is: ', filename
	print 'slippage is: ', slippage
	print 'sharpe_threshold is: ', sharpe_threshold

	test_spread = dp.spread(filename)
	for entry in entries:
		for exit in exits:
			try:
				(sr, profit, num_trades) = test_spread.EE_Sharpe_Ratio(entry, exit, float(slippage))
				if sr > float(sharpe_threshold):
					print (entry, entry*exit), '\t', ("%6.2f" % sr,\
											profit, num_trades,\
											"%6.2f" % (profit/num_trades*2))
			except:
				print "file IO error"
				print 'backtest.py -i filename -s slippage -r sharpe_threshold' 
				sys.exit(2)
				
		
	
if __name__ == "__main__":
	main(sys.argv[1:])
