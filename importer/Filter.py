import yaml
import codecs
import os
import shutil

def build_dict(directory):
	merged = directory + '/merged/'
	filelist = os.listdir(merged)

	# print(filelist)
	map_dict = {}
	for filename in filelist:
		fin = codecs.open(merged+filename,'r','utf-8')
		yml = yaml.load(fin)
		fin.close()

		pub_id = yml['id']
		del(yml['id'])
		map_dict[pub_id] = yml

	return map_dict

def filter(directory):
	dl = directory + '/dl/'
	nn = directory + '/nn/'
	map_dict = build_dict(directory)


	if not os.path.exists(directory+"/nn"):
		os.makedirs(directory+"/nn")
	filelist = os.listdir(dl)

	for filename in filelist:
		fin = codecs.open(dl+filename,'r','utf-8')
		yml = yaml.load(fin)
		fin.close()

		pub = {}
		try:
			pub = yml[list(yml.keys())[0]]
		except Exception as e:
			print("Error: "+ str(e) + " " + filename)

		exist = False
		try:
			for pub_data in list(map_dict.values()):
				if pub['url'] == pub_data['dblp']['id'] and pub['mdate'] == pub_data['dblp']['data']['mdate']:
					exist = True
					break
		except Exception as e:
			print("Error: "+ str(e) + " " + filename)

		if not exist:
			shutil.copyfile(dl+filename,nn+filename)
			# os.system("copy %s %s" % (dl+filename,nn+filename))