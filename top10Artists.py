import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient['db']
mycol = mydb['artists']

pipeline = [
    {
        "$group": {
            "_id": {
                "week": "$week",
                "artist": "$artist"
            },
            "artistCount": {
                "$sum": 1
            }
        }
    },
    {
        "$sort": {
            "artistCount": -1
        }
    },
    {
        "$group": {
            "_id": "$_id.week",
            "artists": {
                "$push": {
                    "artistName": "$_id.artist",
                    "count": "$artistCount"
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

finalArtists = dict()

for x in mydb.songs.aggregate(pipeline):
    x = dict(x)
    finalArtists[x['_id']] = []
    for y in x['artists'][:10]:  # Changed to get the top 10 artists
        finalArtists[x['_id']].append(dict(y)['artistName'])

html = "<html><div class='box'><h1>Top 10 Artists per week</h1>"
for key in sorted(finalArtists):
    html += '<h1>Week ' + str(key) + '</h1><ol>'
    for y in finalArtists[key]:
        html += '<li>' + str(y) + '</li>'
    html += '</ol>'
html += '</div></html>'
print(html)

