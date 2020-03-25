import requests,time,os,json
from bs4 import BeautifulSoup
from pprint import pprint

list_torrent_site=['https://ettv.online/torrents.php?parent_cat=Movies',
					'https://ettv.online/torrents.php?parent_cat=Music',
					'https://ettv.online/torrents.php?parent_cat=Books',
					'https://ettv.online/torrents.php?parent_cat=Adult',
					'https://ettv.online/torrents.php?parent_cat=Software',
					]

def Site_scrape(url):

	path='/home/aman/Desktop/'
	Name=Directory_Name(url)
	if not os.path.exists(path+Name):
		os.makedirs(path+Name)
	for i in range(1000):
		request=requests.get(url+'&page='+str(i))
		soup=BeautifulSoup(request.text,'html.parser')
		table=soup.find('table',class_='table table-hover table-bordered')
		trs=table.find_all('tr')

		flag=0
		book_list=[]
		for tr in trs:
			if flag==1:
				nowrap=tr.b.get_text() #Name of book
				tds=tr.find_all('td')

				for td in tds:
					if 'MB' in td.get_text() or 'GB' in td.get_text() or 'KB' in td.get_text():
						size=td.get_text() #Size
				colour=tr.find('font',color='green').b.get_text() # Seeders
				hash_key=tr.find('td',nowrap='nowrap').a['href']
				hash_request=requests.get('https://ettv.online/'+hash_key)
				hash_soup=BeautifulSoup(hash_request.text,'html.parser')
				download_box=hash_soup.find('div',id='downloadbox')

				hash_vlign=''
				if download_box!=None:
					hash_vlign=download_box.find('td',valign='top').a['href']
				
				hashkey=''
				for key in hash_vlign[20::]:
					if key=='&':
						break
					else:
						hashkey+=key
				Download_key='magnet:?xt=urn:btih:'+hashkey # Hashkey
				
				
				torrent_books={Name:'','Seeders':'','Hash_key':'','Size':''}
				torrent_books[Name]=nowrap
				torrent_books['Seeders']=colour
				torrent_books['Hash_key']=Download_key
				torrent_books['Size']=size
				book_list.append(torrent_books)	
				pprint(book_list)

				time.sleep(3)

			else:
				flag=1

		with open(path+Name+'/page='+str(i)+'.json','w+') as file:
			files=json.dump(book_list,file,indent=2)


def Directory_Name(url):
	print(url)
	name=''
	for i in url[44:]:
		name+=i
	return name
print('0:Movies','1:Music','2:Books','3:Adult','4:Software')
User_choice=int(input())
url=list_torrent_site[User_choice]
Site_scrape(url)