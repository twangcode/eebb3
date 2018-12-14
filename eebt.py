import pandas as pd
import spread

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

# extract each product and its coefficient in the spread
# Returns a ratio list
def generate_ratio_list(spread_name, ratio_dict):
	ratio_list = []
	default_coefficient = 1.0
	
	# First, break down the spread name into pieces:
	block_list = spread_name.replace('+', ' ').replace('-', ' ').split(' ')
	# Second, for each piece, extract product name, coefficient and calculate coeff*ratio
	for block in block_list:
		coefficient = ''
		while not block[0].isalpha():
	 		coefficient = coefficient + block[0]
	 		block = block[1:]
	 	# Get the product name: 
	 	# after get rid of the coefficient, what's left is the product name
	 	prod_name = block
	 	# Get the coefficient:
	 	if not coefficient:
	 		coefficient = default_coefficient
	 	else:
	 		coefficient = float(coefficient)
	 	# Get the ratio:
	 	ratio = look_up(block, ratio_dict)
	 	if ratio is 'nan': 
	 		return "You don't have {} in the database".format(prod_name)
	 	# Calculate coefficient * ratio
	 	ratio_list.append(coefficient * ratio)

	# Normalize ratio_list and return it 	
	return [round(x / min(ratio_list), 3) for x in ratio_list]
	
class ee_backtest():
	def __init__(self, spread, entry, exit, slippage, sharpe_threshold):
		self.name = spread.name
		[self.sharpeRatio, self.total_profit, self.num_trades] = spread.EE_Sharpe_Ratio(entry, exit, slippage)
		