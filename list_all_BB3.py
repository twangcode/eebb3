import tuotools as tt
from os import listdir
from os.path import isfile, join

FILEPATH = '/var/opt/lufgroup/apps/nova_lufcomp/novaStats_ma/data'
ALL_BB3_FILES = 'input/bb3_all.csv'

# get all S:BB3_TENXXX.data files:
def list_BB3_files():
	bb3_list_all = [f for f in listdir(FILEPATH) if isfile(join(FILEPATH, f))]
	return bb3_list_all

def categorize_bb3(bb3_list):
	category = []
	for bb3 in bb3_list:
		try:		
			category.append(bb3.split(':')[1])
		except:
			pass
	return set(category)
	 

def save_to_csv(filename, files):
	tt.list_to_csv(filename, files)
	
# save_to_csv(ALL_BB3_FILES, list_BB3_files())


def main():
	all_bb3_list = list_BB3_files()
	save_to_csv('input/list_BB3_ALL.csv', all_bb3_list)
	all_bb3_category = categorize_bb3(all_bb3_list)
	for bb3_category in all_bb3_category:
		bb3_list = [f for f in listdir(FILEPATH) if (':'+bb3_category+':') in f]
		filename = 'input/list_' + bb3_category + '.csv'
		save_to_csv(filename, bb3_list)

if __name__ == "__main__":
	main()
