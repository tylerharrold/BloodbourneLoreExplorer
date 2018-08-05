from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup

def simple_get(url):
	try:
		with closing(get(url, stream=True)) as resp:
			if is_good_response(resp):
				return resp.content
			else:
				return None
	except RequestException as e:
		log_error('Error during requests to {0} : {1}'.format(url, str(e)))
		return None

def is_good_response(resp):
	# ensures we got an OK response, the content type as read by requests is not None, and 
	# html is in the content type
	content_type = resp.headers['Content-Type'].lower()
	return (resp.status_code == 200
			and content_type is not None
			and content_type.find('html') > -1)

def log_error(e):
	print(e)


# lets see if i can just scrape a list of all the trick weapons in the base game
def get_trick_weapon_names():
	# we need the address for the page with trick weapons
	url = 'https://bloodborne.wiki.fextralife.com/Weapons'
	response = simple_get(url)

	if response is not None:
		html = BeautifulSoup(response, 'html.parser')
		print("this html is of type:" , type(html))
		count = 0

		links = html.find_all('a' , class_="wiki_link")

		for link in links:
			print(link.get_text())
		
		'''
		for tr in html.select('tr'):
			link = tr.select('.wiki_link')
			print("this link is of type:" , type(link))
			
			if link:
				print(link.get_text())
				print('------------------------------')
		'''	
		
		