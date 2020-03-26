import requests,time,os,json
from bs4 import BeautifulSoup
Website_pages=['https://www.limetor.com/browse-torrents/Movies',
				'https://www.limetor.com/browse-torrents/TV-shows',
				'https://www.limetor.com/browse-torrents/Music',
				'https://www.limetor.com/browse-torrents/Games',
				'https://www.limetor.com/browse-torrents/Apps',
				'https://www.limetor.com/browse-torrents/Anime']

def Lime_torrent(url):
	

	path='/home/aman/Desktop/'
	catogary=Category(url)
	if not os.path.exists(path+catogary):
		os.makedirs(path+catogary)

	for i in range(1000):	
		if not os.path.exists(catogary+'_page='+str(i)+'.json'):

			request=requests.get(url+'/date/'+str(i))
			soup=BeautifulSoup(request.text,'html.parser')
			main_contain=soup.find('div',id='content')
			trs=main_contain.find_all('tr')
			
			flag=False
			Lime_list=[]
			for tr in trs:
				if flag==True:
					# find_name=tr.find('div',class_='tdleft')
					Find_hash=tr.find('div',class_='tt-name').a['href']
					hash_key=''
					# print(Find_hash)
					for key in Find_hash[29:]:
						if '.' in key:
							break
						else:
							hash_key+=key
					Magnet_link='magnet:?xt=urn:btih:'+hash_key # magnet link of data

					Find_name=tr.find('div',class_='tt-name')
					attribute=Find_name.find_all('a')
					Name=attribute[1].get_text().strip()
					
					find_size=tr.find_all('td',class_='tdnormal')
					size=find_size[1].get_text()  # Size of data

					seeders=tr.find('td',class_='tdseed').get_text() # Seeders of data

					Lime_dict={catogary:'','Magnet_link':'','Size':'','Seeders':''}  # Create Dictionary and save data in dictory format
					Lime_dict[catogary]=Name
					Lime_dict['Magnet_link']=Magnet_link
					Lime_dict['Size']=size
					Lime_dict['Seeders']=seeders

					Lime_list.append(Lime_dict)
					print(Lime_dict)
			
				else:
					flag=True
		with open(path+catogary+'/'+catogary+'_page='+str(i)+'.json','w+') as file:
			files=json.dump(Lime_list,file)	
		time.sleep(5)
def Category(url):
	
	name=''
	for i in url[40:]:
		name+=i
	return name # return Category Name like: movies, music, tv-shows etc.

User_choice=int(input('Enter a no to choose 0)Movies 1) TV-shows 2)Music 3)Games 4)Apps 5) Anime: '))
print(Lime_torrent(Website_pages[User_choice]))