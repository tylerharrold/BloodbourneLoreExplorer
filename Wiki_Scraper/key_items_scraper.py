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

	
	



# url for wiki list of all right handed weapons
url = "https://www.bloodborne-wiki.com/p/keys.html"

response = get(url).content

# parse the html of the list page such that i have a link to every relevant weapon, store these links in a list
links = []
html = BeautifulSoup(response , 'html.parser')
tables = html.find_all('table' , class_='wiki-blog-table-sheader1')

for table in tables:
	rows = table.find_all('tr')
	for row in rows:
		tag = row.find('a')
		if tag:
			link = tag.get('href')
			if link:
				links.append(link)

links = set(links) # removes any potential duplicates


'''
	The following is the general structure of a Consumable
		consumable_name = {
			picture : "link_to_picture"
			in_game_desc : "text"
			availability : []
		}
		
'''
key_items = {}
for link in links:
	current_item = {}

	print(link)

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
	key_items[name] = current_item

	print("nabbed item")

# now that we've gotten all the items, dump them as a json file
with open('JSON/key_items.json' , 'w') as f:
	json.dump(key_items , f)





