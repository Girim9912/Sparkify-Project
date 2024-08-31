#!/usr/bin/python3

import pickle


with open("top_ten_songs.pickle","rb") as f:
	top_songs = pickle.load(f)

with open("top_ten_artists.pickle","rb") as f:
	top_artists = pickle.load(f)


wrapper = """<html>
<head>
<title> Top Ten Artists and Songs of November 2018 </title>
</head>
<h1> Top Ten Artists and Songs of November 2018 </h1>
<h2> Songs! </h2>
<body>
	"""
def make_table(week,data,theme):
	wrap=""
	start_wrap="""<h3> %s </h3>
	<table>
	<tr>
		<th>Hits</th>
		<th>"""
	start_wrap+=theme
	start_wrap+="""</th>
	</tr>
"""
	wrap = start_wrap % (week)
	
	middle_wrap="""
	<tr>
		<td>%s</td>
		<td>%s</td>
	</tr>"""
	for d in data:
		mid_wrap = middle_wrap % (d[1], d[0])
		wrap+=mid_wrap

	end_wrap="""
	</table>
"""
	wrap+=end_wrap
	return(wrap)

whole=wrapper
for week in top_songs:
	whole+= make_table(week[0],week[1],"Songs")

whole+="""
<h1>Artists!</h1>
"""
for week in top_artists:
	whole+=make_table(week[0],week[1],"Artist")

end_wrapper="""
</body>
"""

whole+=end_wrapper

with open("page.html","w") as p:
	p.write(whole)
	p.close()
