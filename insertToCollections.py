
import pymongo
import os
import json
import itertools

client = pymongo.MongoClient("mongodb://localhost:27017/")
mydb =client["db"]
col = mydb["songs"]

dire = r"/home/ec2-user/log_data/"
week = 1
day =1
for filename in os.listdir(dire):
	with open(dire + filename) as f:
		stuList = []
		print('#####', filename)
		for jsonObj in f:
			dic = json.loads(jsonObj)
			dic['week']= week
			stuList.append(dic)
		col.insert_many(stuList)
		day += 1
		if day == 8:
			week += 1
			day = 1
