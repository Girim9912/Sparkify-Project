#!/usr/bin/python3
import pymongo
import re
import pickle
## Make database
db_name="log_database"

print("Assuming the week ends on Sunday.")

artists=[]

#takes top ten in dictionary that's not empty
def pick_ten(flatten):
	count=0
	top=[]
	for f in flatten:
		if f!=None:
			count+=1
			top.append((f,flatten[f]))
			if count>10:
				return top

client = pymongo.MongoClient("mongodb://localhost:27017/")
with client:
	field="artist"
	db = client[db_name]
	for table_name in sorted(db.collection_names()):
		##groups all unique songs and count, sort, and limit of 11
		group={'$group':{
				'_id':{field:"$artist"},
				'count':{'$sum':1}
				}}
		sort={'$sort':{'count':-1}}

		agr = [group,sort]

		val = list(db[table_name].aggregate(agr))
		artists.append((table_name,val))

	tuple=[]
	##unfortunately these dictionaries need to be ravel somehow, as well
	##as partitioned into weeks. Apparently Nov 01 2018 starts on a Thursday
	top_ten=[]
	switch=False
	for x in enumerate(artists):
		if (x[0]+3)%7==5 or x[0]==29:
			if x[0]==29:
				switch=True
			top_ten.append(x[1])
			if switch==True:
				end_date=x[1][0]
				switch=False
			pattern='2018-11-[\d][\d]'
			start_date = re.match(pattern,start_date)
			end_date= re.match(pattern,end_date)
			string = ["Week ",str((int(x[0]/7)+1))," : ",start_date.group()," through ",end_date.group()]
			string = "".join(string)
			flatten={}
			for t in top_ten:
				for s in t[1]:
					if s['_id'][field] not in flatten:
						flatten[s['_id'][field]]=s['count']
					else:
						flatten[s['_id'][field]]+=s['count']
			flatten = {k: v for k, v in sorted(flatten.items(), key=lambda item: item[1],reverse=True)}

			tuple.append((string,pick_ten(flatten)))
			top_ten=[]
			switch=False
		else:
			if switch==False:
				start_date=x[1][0]
				switch=True
			top_ten.append(x[1])	
	#saving to pickle
	with open('top_ten_artists.pickle',"wb") as pkl:
		pickle.dump(tuple,pkl)
		pkl.close()
