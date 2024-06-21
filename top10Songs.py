import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient['db']
mycol = mydb['songs']

pipeline = [
    {
        "$group": {
            "_id": {
                "week": "$week",
                "song": "$song"
            },
            "songCount": {
                "$sum": 1
            }
        }
    },
    {
        "$sort": {
            "songCount": -1
        }
    },
    {
        "$group": {
            "_id": "$_id.week",
            "songs": {
                "$push": {
                    "songName": "$_id.song",
                    "count": "$songCount"
                }
            },
        }
    },
    {
        "$sort": {
            "_id": 1
        }
    }
]

finalSongs = dict()

for x in mydb.songs.aggregate(pipeline):
    x = dict(x)
    finalSongs[x['_id']] = []
    for y in x['songs'][:10]:  # Changed to get the top 10 songs
        finalSongs[x['_id']].append(dict(y)['songName'])

html = "<html><div class='box'><h1>Top 10 Songs per week</h1>"
for key in sorted(finalSongs):
    html += '<h1>Week ' + str(key) + '</h1><ol>'
    for y in finalSongs[key]:
        html += '<li>' + str(y) + '</li>'
    html += '</ol>'
html += '</div></html>'
print(html)

