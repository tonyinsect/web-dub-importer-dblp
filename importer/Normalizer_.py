import yaml
import os
import codecs


def normalize(directory):
	nn = directory+'/nn/'
	meta = directory + '/meta/'
	rtm = directory + '/rtm/'
	metalist = sorted(os.listdir(meta))
	filelist = os.listdir(nn)

	'''
	this part is loading the authors.yml into our work space
	'''
	fin = codecs.open(meta+'authors.yml','r','utf-8')
	authordict = yaml.load(fin)
	fin.close()

	tempdict = {}
	for key,value in authordict.items():
		name = value['name']
		# print(name)ß
		if len(name) > 2:
			tempdict[name[1]+' '+name[2]+' '+name[0]] = key
		elif len(name) == 2:
			tempdict[name[1]+' '+name[0]] = key
		else:
			print(name)
	authordict = tempdict


	'''
	this part is loading the *paper.yml s in our work space
	'''
	fin = open(meta+'conferencepapers.yml','r')
	cpdict = yaml.load(fin)
	fin.close()
	cpdict_r = {}
	for key,value in cpdict.items():
		cpdict_r[value['title'].lower()] = key
		# print(value['title'])

	fin = open(meta+'journalpapers.yml','r')
	jpdict = yaml.load(fin)
	fin.close()
	jpdict_r = {}
	for key,value in jpdict.items():
		jpdict_r[value['title'].lower()] = key

	fin = open(meta+'conferences.yml','r')
	cdict = yaml.load(fin)
	fin.close()
	cdict_r = {}
	
	
	'''
	to find our author and paper title
	'''
	count = 0
	for filename in filelist:
		fin = codecs.open(nn+filename,'r','utf-8')
		yml = yaml.load(fin)
		fin.close()
		# print(yml)
		pub = {}
		try:
			pub = yml[list(yml.keys())[0]]
		except AttributeError:
			print(filename)

		jc = pub['url'].split('/')[1]
		crossref = ''
		if 'crossref' in pub: 
			crossref = pub['crossref'].split('/')
		if jc == 'conf':
			tempdict = cpdict_r
		else:
			tempdict = jpdict_r
		# print(pub)
		# try:
		# 	print(tempdict[pub['title'].lower()[0:-1]])
		# 	flag = True
		# 	for author in pub['authors']:
		# 		if author in authordict:
		# 			print ('find:' + author+'   '+authordict[author])
		# 		else:
		# 			splited = author.split(' ')
		# 			if len(splited) < 3:
		# 				flag = False
		# 				print ('not find:'+author)
		# 			elif (splited[0]+' '+splited[2]) in authordict:
		# 				print ('find:' + author+'   '+authordict[author])
		# 			else:
		# 				flag = False
		# 				print ('not find:'+author+'      '+splited[0]+' '+splited[2])

			'''
			if crossref[1]+' '+crossref[2] not in cdict_r:
				print(crossref[1]+' '+crossref[2])
				flag = False
			'''

			# if flag:
			# 	try:
			# 		tempdict = {}
			# 		tempdict['authors'] = []
			# 		for author in pub['authors']:
			# 			tempdict['authors'].append(authordict[author])
			# 		tempdict['title'] = pub['title']
			# 		# tempdict['conference'] = cdict_r[crossref[1]+' '+crossref[2]]
			# 		tempdict['pages'] = pub['pages']
			# 		tempdict['officialurl'] = ''
			# 		tempdict['localthumb'] = ''
			# 		tempdict['localpdf'] = ''
			# 		tempdict['localvideo'] = ''

			# 		fout = codecs.open(rtm+filename,'w','utf-8')
			# 		# out = yaml.dump({'id_conferencepaper_'+crossref[1]+crossref[2]:tempdict}, default_flow_style=False, default_style='"')
			# 		out = yaml.dump({'id_conferencepaper_'+str(count):tempdict}, default_flow_style=False, default_style='"')
			# 		fout.write(out)
			# 		fout.close()
			# 		count = count + 1
			# 	except IndexError:
			# 		print('Error: '+filename)

			
			print('\n\n')
		except KeyError:
			pass
		# 	flag = True
		# 	for a_id in normalized['authors']:

		# for author in pub['authors']:
		# 	if author in authordict:
		# 		print ('find:' + author+'   '+authordict[author]+'\n')
		# 	# else:
		# 	# 	print ('not find:'+author+'\n')

	# print(count)


def find(dictionary, inkey, invalue):
	if dictionary == None or value == None:
		return None
	for key,value in dictionary.items():
		if value[inkey] == invavlue:
			return 

	