from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import json


# function to handle potential inconsistencies in the way "In-Game Description" appears on the wiki
def str_search_case_insensitive(s):
	lowercase_hyphen = "in-game description"
	lowercase_no_hyphen = "in game description"
	return s.lower() == lowercase_hyphen or s.lower() == lowercase_no_hyphen or lowercase_no_hyphen in s.lower()

	
	



# materials is subdivided on the wiki into two separate pages, upgrade materials and ritual materials
upgrades_url = 'https://www.bloodborne-wiki.com/p/upgrade-materials.html'
ritual_materials_url = 'https://www.bloodborne-wiki.com/p/ritual-materials.html'



# grab link to every upgrade material, then grab link to every ritual item
links = []

# first, upgrades
response = get(upgrades_url).content
html = BeautifulSoup(response , 'html.parser')
table = html.find('table' , class_='wiki-blog-table-sheader1')
rows = table.find_all('tr')
for row in rows:
	a_tag = row.find('a')
	if a_tag:
		link = a_tag.get('href')
		if link:
			links.append(link)

# now we grab ritual item links
response = get(ritual_materials_url).content
html = BeautifulSoup(response , 'html.parser')
tables = html.find_all('table' , class_='wiki-blog-table-sheader1')
# only first two tables have links we need
for i in range(2):
	rows = tables[i].find_all('tr')
	for row in rows:
		a_tag = row.find('a')
		if a_tag:
			link = a_tag.get('href')
			if link:
				links.append(link)


print(len(links)) # print for viaual approximation of success

links = set(links) # removes any potential duplicates




'''
	The following is the general structure of a material
		consumable_name = {
			picture : "link_to_picture"
			in_game_desc : "text"
			availability : []
		}
		
'''
materials = {}

for link in links:
	current_item = {}

	# grab the item name
	try:
		html_content = get(link).content
		parsed_html = BeautifulSoup(html_content , 'html.parser')
		table = parsed_html.find('table' , class_='wiki-blog-table-sheader1')
		rows = table.find_all('tr')	
		tds = rows[1].find_all('td') # the second row holds the info, the first is a header
		name = tds[1].get_text() # the first td is an image, the second td is the name
		current_item['name'] = name
	except Exception as e:
		print("Error Scraping link: " , link)
		print("Exception took place scraping name attribute")
		print(e)


	# grab the in game description
	try:
		strings = parsed_html.find(string=str_search_case_insensitive) # find the in game description text
		tr = strings.find_parent('tr') # nab the parent said text sits in
		italicized_text = tr.find('i')
		in_game_desc = italicized_text.get_text()
		current_item['description'] = in_game_desc
	except Exception as e:
		print("Error Scraping link: " , link)
		print("Exception took place scraping in game description attribute")
		print(e)

	# grab the picture link
	try:
		big_img = strings.find_next('img')
		img_link = big_img.get('src')
		current_item['img_link'] = img_link
	except Exception as e:
		print("Error Scraping link: " , link)
		print("Exception took place scraping img address attribute")
		print(e)

	# grab the availability
	try:
		string = parsed_html.find('h3' , string='Availability')
		unordered_list = string.find_next('ul') # switch this over to find next
		list_items = unordered_list.find_all('li')
		availability_list = []
		for items in list_items:
			availability_list.append(items.get_text())
		current_item['availability_list'] = availability_list
	except Exception as e:
		print("Error Scraping link: " , link)
		print("Exception took place scraping availability attribute")
		print(e)

	# add this item record into the larger dict of items
	materials[name] = current_item

	print("nabbed item")

# now that we've gotten all the items, dump them as a json file
with open('JSON/materials.json' , 'w') as f:
	json.dump(materials , f)





