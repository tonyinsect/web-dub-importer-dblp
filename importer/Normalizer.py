import yaml
import os
import codecs


def search_conf_id(cdict, temp_id, year):
    for key, value in cdict.items():
        if key == 'conference_series':
            continue
        if value['series'] == temp_id and value['year'] == int(year):
            return key
    return None

def search_conf_title(cpdict,title):
	for key,value in cpdict.items():
		if value['title'].lower() == title:
			return True
	return False


def normalize(directory):
    nn = directory + '/nn/'
    meta = directory + '/meta/'
    rtm = directory + '/rtm/'
    filelist = os.listdir(nn)

    # loading the authors.yml
    fin = codecs.open(meta + 'authors.yml', 'r', 'utf-8')
    authordict = yaml.load(fin)
    fin.close()
    tempdict = {}
    for key, value in authordict.items():
        name = value['name']
        # print(name)ß
        if len(name) > 2:
            tempdict[name[1] + ' ' + name[2] + ' ' + name[0]] = key
        elif len(name) == 2:
            tempdict[name[1] + ' ' + name[0]] = key
        else:
            print(name)
    authordict = tempdict

    # load conference.yml
    fin = open(meta + 'conferences.yml', 'r')
    cdict = yaml.load(fin)
    fin.close()


    fin = open(meta + 'conferencepapers.yml','r')
    cpdict = yaml.load(fin)
    fin.close()

    fin = open(meta + 'map.yml','r')
    mapdict = yaml.load(fin)
    fin.close()


    count = 0

    print(filelist)

    for filename in filelist:
        if filename == '.DS_Store':
            continue
        fin = codecs.open(nn + filename, 'r', 'utf-8')
        yml = yaml.load(fin)
        fin.close()

        pub = {}
        try:
            pub = yml[list(yml.keys())[0]]
        except AttributeError:
            print(filename)
        # if 'James Fogarty' not in pub['authors']:
        # 		continue


        if pub['url'].split('/')[1] == 'conf':

            try:
                print(pub['title'][0:-1])
                flag = True


                # try to find title in cpdict
                if search_conf_title(cpdict,pub['title'].lower()[0:-1]):
                	print('find title')
                else:
                	print('not find title')

                # try to find all authors
                for author in pub['authors']:
                    if author in authordict:
                        print('find:' + author + '   ' + authordict[author])
                    elif author in mapdict:
                        print('find:' + author + '   ' + mapdict[author])
                    else:
                        splited = author.split(' ')
                        if len(splited) < 3:
                            flag = False
                            print('not find:' + author)
                        elif (splited[0] + ' ' + splited[2]) in authordict:
                            print(
                                'find:' + author + '   ' + authordict[splited[0] + ' ' + splited[2]])
                        else:
                            flag = False
                            print(
                                'not find:' + author + '      ' + splited[0] + ' ' + splited[2])

                # try to find conference id
                print(pub['url'])
                temp_id = 'id_' + pub['url'].split('/')[2]
                real_id = search_conf_id(cdict, temp_id, pub['year'])
                if real_id == None:
                    temp_id = pub['url'].split('/')[3].split('.')[0]
                    index = 0
                    while index < len(temp_id):
                        if temp_id[index] < 'a' or temp_id[index] > 'z':
                            break
                        index = index+1
                    temp_id = 'id_'+temp_id[0:index]
                    print(temp_id)
                    real_id = search_conf_id(cdict,temp_id,pub['year'])
                print(str(real_id)+' '+str(flag)+'\n\n')

                if flag:
                    try:
                        tempdict = {}
                        tempdict['authors'] = []
                        for author in pub['authors']:
                            if author in authordict:
                                tempdict['authors'].append(authordict[author])
                            else:
                                tempdict['authors'].append(mapdict[author])
                        tempdict['title'] = pub['title']
                        # tempdict['conference'] = cdict_r[crossref[1]+' '+crossref[2]]
                        tempdict['pages'] = pub['pages']
                        tempdict['conference'] = real_id
                        tempdict['officialurl'] = ''
                        tempdict['localthumb'] = ''
                        tempdict['localpdf'] = ''
                        tempdict['localvideo'] = ''

                        fout = codecs.open(rtm + filename, 'w', 'utf-8')
                        # out = yaml.dump({'id_conferencepaper_'+crossref[1]+crossref[2]:tempdict}, default_flow_style=False, default_style='"')
                        paper_id = 'id_conferencepaper_'+real_id.split('_')[2]+'_'+tempdict['authors'][0].split('_')[2]
                        out = yaml.dump(
                            {paper_id: tempdict}, default_flow_style=False)
                        fout.write(out)
                        fout.close()
                        count = count + 1
                    except IndexError:
                        print('Error: ' + filename)
            except Exception as e:
                print(e)
            	
    print(count)
