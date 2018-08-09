from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup

# grab the item name
link = "https://www.bloodborne-wiki.com/2015/03/third-umbilical-cord.html"

html_content = get(link).content
parsed_html = BeautifulSoup(html_content , 'html.parser')
table = parsed_html.find('table' , class_='wiki-blog-table-sheader1')
rows = table.find_all('tr')	
tds = rows[1].find_all('td') # the second row holds the info, the first is a header
name = tds[1].get_text() # the first td is an image, the second td is the name
print(name)

# grab the in game description
strings = parsed_html.find(string="In-Game Description") # find the in game description text
tr = strings.find_parent('tr') # nab the parent said text sits in
italicized_text = tr.find('i')
in_game_desc = italicized_text.get_text()
print(in_game_desc)

# grab the picture link
big_img = tr.find('img')
img_link = big_img.get('src')
print(img_link)

# grab the availability
string = tr.find('h3' , string='Availability')
unordered_list = string.find_next_sibling('ul')
list_items = unordered_list.find_all('li')
availability_list = []
for items in list_items:
	availability_list.append(items.get_text())
print(availability_list)


print("nabbed item")