import os
import requests

from bs4 import BeautifulSoup as bs

def main():

	print('Inserisci Id: ')
	url = voiceLinks(int(input()))
	print(url)
	r = requests.get(url)

	with open("download.ogg", "wb") as o:
	    o.write(r.content)



def voiceLinks(Id):

	ulr = 'https://smite.gamepedia.com' + godsLink(Id)

	return(voicesLines('https://smite.gamepedia.com' + godsLink(Id), Id))


def godsLink(Id):

	r = requests.get("https://smite.gamepedia.com/God_voicelines")
	contenuto = bs(r.text,"html.parser")

	gods = []

	for x in contenuto.findAll("a"):
		if '_voicelines' in str(x.get('href')):
			gods.append(str(x.get('href')))

	gods = list(dict.fromkeys(gods[4:226]))

	return(gods[Id])


def voicesLines(link, Id):

	voicesLinks = []

	r = requests.get(link)
	contenuto = bs(r.text,"html.parser")

	for x in contenuto.findAll("a"):
		if 'https://static.wikia.nocookie.net' in str(x.get('href')):
			voicesLinks.append(str(x.get('href')))


	for x in voicesLinks:
		print(x)

	return(voicesLinks[Id])

main()
