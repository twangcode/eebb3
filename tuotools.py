# csv_to_list(filename): 			convert csv file (filename) to a list and return it
# list_to_csv(filename, mylist): 	write list (mylist) to a csv file (filename)

from os import listdir
from os.path import isfile, join
import data_parser as dp
import pandas as pd
import csv

#	convert csv file (filename) to a list and return it
def csv_to_list(filename):
	mylist = []
	with open(filename, 'r') as fin:
		reader = csv.reader(fin)
		for row in reader:
			mylist.append(row[0])
	return mylist
		
# 	write list (mylist) to a csv file (filename)
def list_to_csv(filename, mylist):
	with open(filename, 'wb') as fout:
		writer = csv.writer(fout)
		for data in sorted(mylist):
			writer.writerow([data])
