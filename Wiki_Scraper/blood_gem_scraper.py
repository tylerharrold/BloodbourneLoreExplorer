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
url = "https://www.bloodborne-wiki.com/p/blood-gems.html"

response = get(url).content

# parse the html of the list page such that i have a link to every relevant weapon, store these links in a list
links = []
html = BeautifulSoup(response , 'html.parser')

# there is only a small amount of unique gems that we want to scrape
h3 = html.find('h3' , string='Unique Gems')

table = h3.find_next('table' , class_='wiki-blog-table-sheader1')
rows = table.find_all('tr')
for row in rows:
	a_tag = row.find('a')
	if a_tag:
		link = a_tag.get('href')
		if link:
			links.append(link)


links = set(links) # removes any potential duplicates


'''
	The following is the general structure of a blood gem
		blood_gem_name = {
			picture : "link_to_picture"
			in_game_desc : "text"
			availability : []
		}
		
'''
blood_gems = {}
for link in links:
	current_item = {}

	print(link)

	# grab the item name
	html_content = get(link).content
	parsed_html = BeautifulSoup(html_content , 'html.parser')
	table = parsed_html.find('table' , class_='wiki-blog-table-sheader1')
	rows = table.find_all('tr')	
	tds = rows[1].find_all('td') # the second row holds the info, the first is a header
	name = tds[1].get_text() # the first td is an image, the second td is the name
	current_item['name'] = name

	
	if name == "Third Umbilical Cord":
		continue

	# grab the in game description
	strings = parsed_html.find(string=str_search_case_insensitive) # find the in game description text
	tr = strings.find_parent('tr') # nab the parent said text sits in
	italicized_text = tr.find('i')
	in_game_desc = italicized_text.get_text()
	current_item['description'] = in_game_desc

	# grab the picture link
	big_img = strings.find_next('img')
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
	blood_gems[name] = current_item

	print("nabbed item")

# now that we've gotten all the items, dump them as a json file
with open('JSON/blood_gems.json' , 'w') as f:
	json.dump(blood_gems , f)





