import requests as req
import xmltodict
import re
import folium
from folium import plugins
import pandas as pd
import pymongo 
import time



    
    
client=pymongo.MongoClient()
db=client.earthquake





def getxml():
	url = 'http://www.ssn.unam.mx/rss/ultimos-sismos.xml'
	data=req.get(url).content
	return xmltodict.parse(data)



    
    
    
    
def earth():
	
	d=getxml()
	
	for i in range(len(d['rss']['channel']['item'])):
		
		data_get=d['rss']['channel']['item'][i]['description'].split('>')[1:4]
		
		fecha=re.findall('\d+-\d+-\d+', data_get[0])[0]
		hora=re.findall('\d+:\d+:\d+', data_get[0])[0]
		lat=re.findall('-?\d+.\d+', data_get[1])[0]
		lon=re.findall('-?\d+.\d+', data_get[1])[1]
		prof=re.findall('\d+.\d+ \w+', data_get[2])[0]
		
		inten=float(d['rss']['channel']['item'][i]['title'].split(',')[0])
		
		data={'Fecha':fecha, 'Hora':hora,
			  'Latitud':float(lat), 'Longitud':float(lon),
			  'Profundidad':prof, 'Intensidad':inten}
		print (data)
		db.ssnUnam.update(data, data, upsert=True)





while 1:
	earth()
	print ('paso1')
	print ()
	time.sleep(10)
	print ('paso2')
	print ()
