import yaml
import os
import codecs

def patcher(directory):
	rtm = directory + '/rtm/'
	meta = directory + '/meta/'

	data_files = [
		'authors',
		'conferencepapers',
		'conferences',
		'journalpapers',
		'journals',
		'workshoppapers',
		'workshops',
	]

	data = {}
	for data_current in data_files:
		filename = meta + '{}.yml'
		with codecs.open(filename.format(data_current),'r','utf-8') as f:
			data[data_current] = yaml.load(f)

	filelist = os.listdir(rtm)

	for filename in filelist:
		fin = codecs.open(rtm + filename, 'r', 'utf-8')
		yml = yaml.load(fin)
		fin.close()

		if yml['well_edit']:
			for new_author in yml['new']['authors']:
				for key,value in new_author.items():
					data['authors'][key] = value



	for data_current in data_files:
		filename = meta + '{}.yml'
		with codecs.open(filename.format(data_current),'w','utf-8') as f:
			out = yaml.dump(data[data_current], default_flow_style=False)
			f.write(out)