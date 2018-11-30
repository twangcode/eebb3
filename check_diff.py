# Check if there's new BB3 add to the list
# compare_list(list_1, list_2):		compare two lists (list_1, list_2), return the difference as list
######################################################################################################
# The file reads 'data/all_bb3_list.csv' and compare it to the BB3_list published on lockwood and check if there's any difference
# if there is, it will return the difference. Otherwise it will tell the user there's no difference


from os import listdir
from os.path import isfile, join
import data_parser as dp
import csv
import tuotools as tt
import list_all_BB3 as laB

FILEPATH = '/var/opt/lufgroup/apps/nova_lufcomp/novaStats_ma/data'
		
# compare two lists (list_1, list_2), return the difference as list		
def compare_list(list_1, list_2):
	return list(set(list_1) - set(list_2))

def main():
	files = laB.list_BB3_files()
	files_2 = tt.csv_to_list('input/list_BB3_ALL.csv')
	diff = compare_list(files, files_2)
	if not diff:
		print "No new BB3s added"
	else:
		print diff
		

if __name__ == '__main__':
	main()
