#!/usr/bin/python3
import pymongo
import re
import pickle
## Make database
db_name="log_database"

print("Assuming the week ends on Sunday.")

songs=[]

#takes top ten in dictionary that's not empty
def pick_ten(flat):
	count=0
	top=[]
	for f in flat:
		if (f!=None):
			count+=1
			top.append((f,flat[f]))
			if count>=10:
				return top

client = pymongo.MongoClient("mongodb://localhost:27017/")
tuple=[]
with client:
	db = client[db_name]
	for table_name in sorted(db.collection_names()):
		##groups all unique songs and count, sort
		group={'$group':{
				'_id':{'song':"$song"},
				'count':{'$sum':1}
				}}
		sort={'$sort':{'count':-1}}
		agr = [group,sort]

		val = list(db[table_name].aggregate(agr))
		songs.append((table_name,val))
	##unfortunately these dictionaries need to be ravel somehow, as well
	##as partitioned into weeks. Apparently Nov 01 2018 starts on a Friday
	top_ten=[]
	switch=False
	for x in enumerate(songs):
		if (x[0]+3)%7==5 or x[0]==29:
			if x[0]==29:
				switch=True
			top_ten.append(x[1])
			if switch==True:
				end_date=x[1][0]
			pattern='2018-11-[\d][\d]'
			start_date = re.match(pattern,start_date)
			end_date= re.match(pattern,end_date)
			string = ["Week ",str((int(x[0]/7)+1))," : ",start_date.group()," through ",end_date.group()]
			string = "".join(string)
			flatten={}
			for t in top_ten:
				for s in t[1]:
					if s['_id']['song'] not in flatten:
						flatten[s['_id']['song']]=s['count']
					else:	
						flatten[s['_id']['song']]+=s['count']
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
	with open('top_ten_songs.pickle',"wb") as pkl:
		pickle.dump(tuple,pkl)
		pkl.close()
