#!/usr/bin/python3
import pymongo
import json
from os.path import isfile, join
from os import listdir

## Make database
client = pymongo.MongoClient("mongodb://localhost:27017/")

#checking for database existence
db_name="log_database"

def drop_db(client,db_name):
	dblist = client.list_database_names()
	if db_name in dblist:
		print("Database exists. Deleting database? Y/N.")
		cin = input()
		if cin.lower()=="y":
			client.drop_database(db_name)
			print("Database has been deleted.")
			return True
		else:
			print("Database has not been deleted.")
			return False
	else:
		print("Database now exists.")
		return True

#Get file names in said directory
def generate_dir(json_dir):
	return [f for f in listdir(json_dir)]

#opens directory and adds the data to a new table
def import_data(json_dir,file,col):
	with open(json_dir+file) as f:
		data = [json.loads(sample) for sample in f]
		col.insert_many(data)
		print(file,"file is finished.")

#option to delete db
opt = drop_db(client,db_name)

db = client[db_name]
json_dir="log_data/2018/11/"
files = sorted(generate_dir(json_dir))

#Create db
if opt==True:
	for file in files:
		col = db[file]
		import_data(json_dir,file,col)
print("\n")
print("Database name:",db_name)
col_sort = sorted(db.collection_names())

summ=0
for c in col_sort:
	x = db[c].find()
	x = [i for i in x]
	print("Collection name:",c,"documents:",len(x))
	summ+=len(x)
print(summ)
