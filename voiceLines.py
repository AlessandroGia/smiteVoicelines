import os
import requests
import sys
import time

from bs4 import BeautifulSoup as bs

def main():

	cont = 0

	print('Inserisci Id: ')


	urls, god = voiceLinks(int(input()))

	direct = os.path.dirname(os.path.realpath(__file__))
	directVoices = direct + '\\voices'

	if not os.path.exists(directVoices):
		os.mkdir(directVoices)

	directGod = directVoices + '\\' + god

	if not os.path.exists(directGod):
		os.mkdir(directGod)

	for url in urls:

		fileVoice = url.split('/')[7]

		pathFileVoice = directGod + '\\' + fileVoice
		#dirVoice = fileVoice.split('.')[0])

		if not os.path.exists(pathFileVoice):
				r = requests.get(url)

				with open(pathFileVoice, "wb") as o:
					cont += 1
					#o.write(r.content)
					#o.close()
					#sys.stdout.write("\r{0}>".format("="*cont))
					#sys.stdout.flush()


	print(cont)

	print(directGod)

	print(god)
	#print(url)
	#r = requests.get(url)

	#with open("download.ogg", "wb") as o:
	#    o.write(r.content)



def voiceLinks(Id):

	godLink = godsLink(Id)

	god = '_'.join(godLink.replace('/', '').split('_')[:-1])

	ulr = 'https://smite.gamepedia.com' + godLink

	return(voicesLines('https://smite.gamepedia.com' + godsLink(Id), Id), god)


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

	return(voicesLinks)

	

main()


