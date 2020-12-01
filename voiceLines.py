import os
import requests
import sys
import time
import json

from bs4 import BeautifulSoup as bs

numGods = 113

def main():

	global numGods

	print(numGodss())
	scaricaListaGods()
	print(numGodss())

	RANGx = 0
	RANGy = 500

	print()
	sc = input("Skin (S/n) ")

	flag = 1 if sc.lower() == 's' else 0
		

	In = input('Inserisci Nome: ')
	print()

	if In.lower() == 'all':
		RANGy = numGods

	else:
		for c, x in enumerate(getGods()):
			if In.lower() == x.lower():
				RANGx = c
				RANGy = RANGx + 1

		if RANGy == 500:
			RANGy = int(In)
		
	for x in range(RANGx, RANGy):
		scarica(x, flag)

def replaceString(string):

	if '?' in string:
		return string[:string.index('?')]

	else:
		return string
		

def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()


def voiceLinks(Id):

	godLink = godsLink(Id)


	god = '_'.join(godLink.replace('/', '').split('_')[:-1])

	ulr = 'https://smite.gamepedia.com' + godLink

	return(voicesLines('https://smite.gamepedia.com' + godLink, Id), god)


def godsLink(Id):

	r = requests.get("https://smite.gamepedia.com/God_voicelines")
	contenuto = bs(r.text,"html.parser")

	gods = []

	for x in contenuto.findAll("a"):
		if '_voicelines' in str(x.get('href')):
			gods.append(str(x.get('href')))

	gods = list(dict.fromkeys(gods[4:226]))

	return(gods[Id])

def skinVoicesLines(link):

	voicesLinks = []

	skinName = link[1:-11]
	
	r = requests.get('https://smite.gamepedia.com' + link)
	contenuto = bs(r.text,"html.parser")
	#print(link)

	for x in contenuto.findAll("a"):
		if 'https://static.wikia.nocookie.net' in str(x.get('href')):
			voicesLinks.append(str(x.get('href')))

	return(voicesLinks, skinName)




def skinVoiceLinks(god):

	skinsGodUrl = []

	r = requests.get('https://smite.gamepedia.com/Skin_voicelines')
	contenuto = bs(r.text,"html.parser")

	skinGodsUrl = []
	nameSkins = []

	for x in contenuto.findAll("span"):
		if str(x.get('id')).lower() == god.lower() + "_skins":
			UL = x.parent.next_sibling.next_sibling
			break

	for x in UL.findAll("a"):
		skinGodsUrl.append(str(x.get('href')))


	skinGodsUrl = list(dict.fromkeys(skinGodsUrl))


	for c, x in enumerate(skinGodsUrl):

		if "?" in x:
			skinGodsUrl.pop(c - 1)

	for link in skinGodsUrl:

		godUrl, nameSkin = skinVoicesLines(link)

		skinsGodUrl.append(godUrl)
		nameSkins.append(nameSkin)



	return(skinsGodUrl, nameSkins)


	
		


def voicesLines(link, Id):

	voicesLinks = []

	r = requests.get(link)
	contenuto = bs(r.text,"html.parser")

	for x in contenuto.findAll("a"):
		if 'https://static.wikia.nocookie.net' in str(x.get('href')):
			voicesLinks.append(str(x.get('href')))

	return(voicesLinks)

def getGods():

	direct = os.path.dirname(os.path.realpath(__file__))

	if not os.path.exists(direct + '\\gods'):

		os.mkdir(direct + '\\gods')

	if not os.path.exists(direct + '\\gods' + '\\gods.txt'):

		scaricaListaGods()
		

	with open(direct + '\\gods\\gods.txt', 'r') as f:
		data = json.load(f)
		f.close()

	gods = []

	for x in data['gods']:

		god = x['name']
		gods.append(god)


	return(gods)

def scaricaListaGods():

	godsJson = {}
	godsJson['gods'] = []

	direct = os.path.dirname(os.path.realpath(__file__))

	printProgressBar(0, numGods, prefix = 'Scaricando lista dei gods:', suffix = 'Completato', length = 50)

	for x in range(numGods):
		godsJson['gods'].append({"name": '_'.join(godsLink(x).replace('/', '').split('_')[:-1]).replace('_', ' '), "Id": x})
		printProgressBar(x, numGods - 1, prefix = 'Scaricando lista dei gods:', suffix = 'Completato', length = 50)
						
	with open(direct + '\\gods\\gods.txt', 'w') as outfile:
		json.dump(godsJson, outfile)
		outfile.close()

	print()

def scarica(Id, flag):

	urls, god = voiceLinks(Id)

	if flag:

		urlsSkin, nameSkin = skinVoiceLinks(god)


		for c, links in enumerate(urlsSkin):
			scaricaSkinVoiceLines(links, nameSkin[c], god)


	else:

		scaricaDeafultVoiceLines(urls, god)

	#scaricaSkinVoiceLines(urls, god) if flag else scaricaDeafultVoiceLines(urls, god)


def scaricaSkinVoiceLines(urls, nameSkin, god):

	if urls:

		cont = 0

		#print(urls, god)

		l = len(urls)

		direct = os.path.dirname(os.path.realpath(__file__))

		directVoices = direct + '\\voices'
		if not os.path.exists(directVoices):
			os.mkdir(directVoices)

		directGod = directVoices + '\\' + god.lower()
		if not os.path.exists(directGod):
			os.mkdir(directGod)

		directDefault = directGod + '\\' + replaceString(nameSkin.lower())
		if not os.path.exists(directDefault):
			os.mkdir(directDefault)


		printProgressBar(0, l, prefix = 'Scaricando ' + nameSkin.replace('_', ' ') + ' voicepacks:', suffix = 'Completato', length = 50)

		for url in urls:

			fileVoice = url.split('/')[7]

			pathFileVoice = directDefault + '\\' + fileVoice
			#dirVoice = fileVoice.split('.')[0])

			if not os.path.exists(pathFileVoice):

					if cont == 0:
						root, dirs, files = next(os.walk(directDefault, topdown = True))
						lenFiles = len(files)
						l = l - lenFiles

					r = requests.get(url) 

					with open(pathFileVoice, "wb") as o:

						cont += 1
						o.write(r.content)
						printProgressBar(cont, l, prefix = 'Scaricando ' + nameSkin.replace('_', ' ') + ' voicepacks:', suffix = 'Completato', length = 50)
						o.close()
		if not cont:
			printProgressBar(1, 1, prefix = 'Scaricando ' + nameSkin.replace('_', ' ') + ' voicepacks:', suffix = 'Completato', length = 50)

		if cont:
			print('Scaricati: ' + str(cont))
		print()





def scaricaDeafultVoiceLines(urls, god):

	cont = 0

	#print(urls, god)

	l = len(urls)

	direct = os.path.dirname(os.path.realpath(__file__))

	directVoices = direct + '\\voices'
	if not os.path.exists(directVoices):
		os.mkdir(directVoices)

	directGod = directVoices + '\\' + god.lower()
	if not os.path.exists(directGod):
		os.mkdir(directGod)

	directDefault = directGod + '\\default'
	if not os.path.exists(directDefault):
		os.mkdir(directDefault)


	printProgressBar(0, l, prefix = 'Scaricando ' + god.replace('_', ' ') + ' voicepacks:', suffix = 'Completato', length = 50)

	for url in urls:

		fileVoice = url.split('/')[7]

		pathFileVoice = directDefault + '\\' + fileVoice
		#dirVoice = fileVoice.split('.')[0])

		if not os.path.exists(pathFileVoice):

				if cont == 0:
					root, dirs, files = next(os.walk(directDefault, topdown = True))
					lenFiles = len(files)
					l = l - lenFiles

				r = requests.get(url) 

				with open(pathFileVoice, "wb") as o:

					cont += 1
					o.write(r.content)
					printProgressBar(cont, l, prefix = 'Scaricando ' + god.replace('_', ' ') + ' voicepacks:', suffix = 'Completato', length = 50)
					o.close()
	if not cont:
		printProgressBar(1, 1, prefix = 'Scaricando ' + god.replace('_', ' ') + ' voicepacks:', suffix = 'Completato', length = 50)

	if cont:
		print('Scaricati: ' + str(cont))
	print()


def numGodss():

	direct = os.path.dirname(os.path.realpath(__file__))

	if not os.path.exists(direct + '\\gods'):

		os.mkdir(direct + '\\gods')

	if not os.path.exists(direct + '\\gods' + '\\gods.txt'):

		scaricaListaGods()
		

	with open(direct + '\\gods\\gods.txt', 'r') as f:
		data = json.load(f)
		f.close()

	return(data['gods'][-1]['Id'] + 1)



main()