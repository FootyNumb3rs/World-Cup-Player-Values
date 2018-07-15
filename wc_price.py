from selenium import webdriver 
from selenium.webdriver.support.ui import Select
import pprint as pp
import time
from selenium.webdriver.common.keys import Keys
import pandas as pd
from matplotlib import pyplot as plt
import sqlite3
from incf.countryutils import transformations
import pycountry_convert as pc

def scrape_transfermarkt_table(url,driver,team):
	all_data = []
	driver.get(url)
	time.sleep(3)
	table = driver.find_element_by_class_name('items').find_element_by_tag_name('tbody')
	for i,tr in enumerate(table.find_elements_by_tag_name('tr')):
		row_data = []
		if i%3 != 0:
			continue
		for j, td in enumerate(tr.find_elements_by_tag_name('td')):
			if j not in [1,2,5,7]: # These rows contain useless data
				row_data.append(td.text)
		
		row_data.append(team)
		all_data.append(row_data)
		print(row_data)
	return(all_data)


def scrape_transfermarkt_teams(url,driver):
	all_data = []
	driver.get(url)
	table = driver.find_elements_by_class_name('items')[0].find_element_by_tag_name('tbody')
	for i,tr in enumerate(table.find_elements_by_tag_name('tr')):
		row_data = []
		for j, td in enumerate(tr.find_elements_by_tag_name('td')):
			if j == 1: # These rows contain useless data
				all_data.append((td.find_element_by_tag_name('a').text,
					td.find_element_by_tag_name('a').get_attribute('href')))
				break
	return(all_data)

def get_price(price):
	if 'Mill' in price:
		return(int(price.split(' ')[0].split(',')[0])*10**6)

	if 'Th' in price:
		return(int(price.split(' ')[0].split(',')[0])*10**3)

def get_continent(country):
	ex = {'England':'Europe'}
	cn_codes  = {'AF':'Africa',
				 'AS':'Asia',
				 'EU':'Europe',
				 'NA':'North America',
				 'OC':'Oceania',
				 'SA':'South America'}
	pc_dict = pc.map_countries()
	try:
		a3 = pc_dict[country]['alpha_2'] 
		cn = pc.country_alpha2_to_continent_code(a3)
		return(cn_codes[cn])
	except:
		return(ex[country])

def simplify_position(position):
	if 'Midfield' in position:
		return 'Midfielder'

	if 'Back' in position:
		return 'Defender'

	if position in ['Right Wing','Left Wing',
	'Centre-Forward','Secondary Striker']:
			return 'Forward'

	else:
		return('Keeper')


'''
driver2 = webdriver.Chrome()
url2='https://www.transfermarkt.com/weltmeisterschaft-2018/teilnehmer/pokalwettbewerb/WM18'
driver =  webdriver.Chrome()

team_links = scrape_transfermarkt_teams(url2,driver2)
dfs = []
for team, link in team_links:
	dfs.append(pd.DataFrame(scrape_transfermarkt_table(link,driver,team)))
df = pd.concat(dfs)
df.to_csv('transfermarkt.csv',index=False)
'''


# Appropriating Data 
'''
df.columns = ['Number','Player','Position','Age','Price','Country']

df.Price = df.Price.apply(get_price)
df.Country = df.Country.str.replace("'",'')
df['Continent'] = df.Country.apply(get_continent)
'''

'''
df['Position2'] =  df.Position.apply(simplify_position)
df.to_csv('transfermarkt.csv',index=False)
df.Price = df.Price
'''

## Getting Wikipedia Links
'''
df = pd.read_csv('transfermarkt.csv',header=0)
df2 = pd.read_csv('all_players.csv',header = 0).loc[:,['Wiki','Num','Origin']]
df3=[]

for country, c_df in df.groupby('Country'):
	t_df2 = df2[df2['Origin'] == country]
	c_df.Num = c_df.Num.astype(int)
	t_df2.Num = t_df2.Num.astype(int)
	
	try:
		df3.append(c_df.merge(t_df2,left_on='Player',right_on='Player',how='outer'))
	except

df3 = pd.concat(df3)
'''

## Convert to US Dollars
df = pd.read_csv('transfermarkt.csv',header=0)
df.Value = df.Value*1.17
df.to_csv('transfermarkt.csv',index=False)