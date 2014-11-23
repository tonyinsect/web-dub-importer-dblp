import yaml
import os
import codecs

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

def search_author(author,map_dict):
    for data in list(map_dict.values()):
        if author in data['dblp']['data']['authors']:
            return data['dblp']['data']['authors'][author]
    return None

def build_new_author(author):
    split = author.split(' ')
    author_dict = {}
    author_id = "id_author_"
    if len(split) == 2:
        author_id = author_id + split[1].lower() + "_" +split[0].lower()
        author_dict[author_id] = {'name':[split[1],split[0]]}
    elif len(split) > 2:
        author_id = author_id + split[len(split)-1].lower() + "_" +split[0].lower()
        last = split[len(split)-1]
        del(split[len(split)-1])
        split.insert(0,last)
        author_dict[author_id] = {'name':split}
    return author_dict

def normalize(directory):
    nn = directory + '/nn/'
    rtm = directory + '/rtm/'

    if not os.path.exists(directory+"/rtm"):
        os.makedirs(directory+"/rtm")

    filelist = os.listdir(nn)

    map_dict = build_dict(directory)


    for filename in filelist:
        if filename == '.DS_Store':
            continue
        fin = codecs.open(nn + filename, 'r', 'utf-8')
        yml = yaml.load(fin)
        fin.close()

        pub = {}
        try:
            pub = yml[list(yml.keys())[0]]
        except Exception as e:
            print("ERROR: "+str(e)+" "+filename)

        paper_dict = {}
        new_dict = {}

        # authors
        if len(pub['authors']) > 10:
            continue
        paper_dict['authors'] = []
        new_dict['authors'] = []
        new_authors = []
        for author in pub['authors']:
            author_id = search_author(author,map_dict)
            if author_id == None:
                new_authors.append(author)
                paper_dict['authors'].append(None)
            else:
                paper_dict['authors'].append(author_id)


        # manage new authors
        for author in new_authors:
            new_dict['authors'].append(build_new_author(author))

        # put new ids in paper_dict
        j = 0
        for i in range(len(paper_dict['authors'])):
            if paper_dict['authors'][i] == None:
                paper_dict['authors'][i] = list(new_dict['authors'][j].keys())[0]
                j = j+1



        # build rest of paper_dict
        paper_dict['title'] = pub['title']
        # tempdict['conference'] = cdict_r[crossref[1]+' '+crossref[2]]
        # paper_dict['pages'] = pub['pages']
        paper_dict['conference'] = ""
        paper_dict['officialurl'] = ''
        paper_dict['localthumb'] = ''
        paper_dict['localpdf'] = ''
        paper_dict['localvideo'] = ''

        fout = codecs.open(rtm + filename, 'w', 'utf-8')
        out = yaml.dump({"new":new_dict,"paper":paper_dict,"well_edit":False}, default_flow_style=False)
        fout.write(out)
        fout.close()