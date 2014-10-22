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


def search_author_id(adict, name):
    split = name.split(' ')
    id_list = []
    for key, value in adict.items():
        count = 0
        for word in split:
            if word in value['name']:
                count = count + 1
        if count >= len(value['name']) - 1:
            id_list.append(key)
    return id_list


def build_dict(directory):
    nn = directory + '/nn/'
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
        with open(filename.format(data_current)) as f:
            data[data_current] = yaml.load(f)

    tempdict = {}
    for key, value in data['authors'].items():
        name = value['name']
        # print(name)ß
        if len(name) > 2:
            tempdict[name[1] + ' ' + name[2] + ' ' + name[0]] = key
        elif len(name) == 2:
            tempdict[name[1] + ' ' + name[0]] = key
        else:
            print(name)
    authordict = tempdict

    filelist = os.listdir(nn)

    tempdict = {}
    for filename in filelist:
        fin = codecs.open(nn + filename, 'r', 'utf-8')
        yml = yaml.load(fin)
        fin.close()

        pub = {}
        try:
            pub = yml[list(yml.keys())[0]]
        except AttributeError:
            print(filename)
        if 'James Fogarty' not in pub['authors']:
            continue

        # if pub['url'].split('/')[1] == 'conf':
        #     temp_id = 'id_' + pub['url'].split('/')[2]
        #     real_id = search_conf_id(data['conferences'], temp_id, pub['year'])
        #     if real_id == None:
        #         print(temp_id)
        #         continue

        un_find_author = []
        for author in pub['authors']:
            if author in authordict:
                print('find:' + author + '   ' + authordict[author])
                tempdict[author] = authordict[author]
            else:
                splited = author.split(' ')
                if len(splited) < 3:
                    print('not find:' + author)
                    un_find_author.append(author)
                elif (splited[0] + ' ' + splited[2]) in authordict:
                    tempdict[author] = authordict[splited[0] + ' ' + splited[2]]
                    print(
                        'find:' + author + '   ' + authordict[splited[0] + ' ' + splited[2]])
                else:
                    un_find_author.append(author)
                    print(
                        'not find:' + author + '      ' + splited[0] + ' ' + splited[2])

        for author in un_find_author:
            tempdict[author] = search_author_id(data['authors'],author)
    fout = codecs.open(meta+'test.yml','w','utf-8')
    out = yaml.dump(tempdict, default_flow_style=False)
    fout.write(out)
    fout.close()     
    
    print(len(tempdict.keys()))
    print(len(data['authors'].keys()))


