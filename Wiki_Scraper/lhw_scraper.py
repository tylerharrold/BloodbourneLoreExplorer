from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import json

# url for wiki list of all left handed weapons
url = "https://www.bloodborne-wiki.com/p/firearms.html"

response = get(url).content

# parse the html of the list page such that i have a link to every relevant weapon, store these links in a list
links = []
html = BeautifulSoup(response , 'html.parser')
table = html.find('table' , class_='wiki-blog-table-sheader1')

a_tags = table.find_all('a')

for tag in a_tags:
	link = tag.get('href')
	if link:
		links.append(link)

for link in links:
	print(link)


# go into every link and scrap info from that page

''' 
	The following is the general structure of a Left Handed Weapon
		weapon_name = {
			picture : "link_to_picture"
			in_game_desc : "text"
			availability : []
		}
'''
left_handed_weapons = {}
for link in links:
	current_item = {}

	# grab the item name
	html_content = get(link).content
	parsed_html = BeautifulSoup(html_content , 'html.parser')
	table = parsed_html.find('table' , class_='wiki-blog-table-sheader1')
	rows = table.find_all('tr')	
	tds = rows[1].find_all('td') # the second row holds the info, the first is a header
	name = tds[1].get_text() # the first td is an image, the second td is the name
	current_item['name'] = name

	# grab the in game description
	strings = parsed_html.find(string="In-Game Description") # find the in game description text
	tr = strings.find_parent('tr') # nab the parent said text sits in
	italicized_text = tr.find('i')
	in_game_desc = italicized_text.get_text()
	current_item['description'] = in_game_desc

	# grab the picture link
	big_img = tr.find('img')
	img_link = big_img.get('src')
	current_item['img_link'] = img_link

	# grab the availability
	string = tr.find('h3' , string='Availability')
	unordered_list = string.find_next_sibling('ul')
	list_items = unordered_list.find_all('li')
	availability_list = []
	for items in list_items:
		availability_list.append(items.get_text())
	current_item['availability_list'] = availability_list

	# add this item record into the larger dict of items
	left_handed_weapons[name] = current_item

	print("nabbed item")

# now that we've gotten all the items, dump them as a json file
with open('left_handed_weapons.json' , 'w') as f:
	json.dump(left_handed_weapons , f)









