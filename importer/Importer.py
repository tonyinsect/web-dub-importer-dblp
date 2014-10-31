# import sys
# sys.path.append('dblp-python/')
# import dblp
import dblppython.dblp
import codecs
import yaml
# import hashlib
import re
# import lxml
import time
import os


def run(directory):

    fin = open(directory + '/url.yml')
    urls = yaml.load(fin)
    fin.close()

    if not os.path.exists(directory+"/nn"):
    	os.makedirs(directory+"/nn")
    # fout.write('---\n')
    fdict = {}
    count = 0

    for url_id, url in urls.items():
        author = dblppython.dblp.Author(url['url'].strip('\n'))
        name = author.name.split(' ')
        adict = {}
        print("\n")
        print(author.name)
        # for pub in author.publications:
        for i in range(len(author.publications)):
            pub = author.publications[i]
            try:
                if pub.authors:
                    tempdict = {}
                    print(str(i)+" "+pub.title)
                    # hashcode = hashlib.sha224(str(pub)).hexdigest()
                    first = pub.authors[0].split(' ')
                    pdict = {}
                    # pdict['hash'] = hashcode
                    pdict['title'] = pub.title.replace('\'', '')
                    pdict['authors'] = []
                    if len(pub.authors) == 1:
                        pdict['authors'].append(pub.authors[0])
                    else:
                        for pubAuthor in pub.authors:
                            pdict['authors'].append(str(pubAuthor))
                    if pub.booktitle:
                        pdict['booktitle'] = str(pub.booktitle)
                    if pub.chapter:
                        pdict['chapter'] = str(pub.chapter)
                    # if pub.citations:
                    #     pdict['citations'] = str(pub.citations)
                    if pub.crossref:
                        pdict['crossref'] = str(pub.crossref)
                    if pub.editors:
                        pdict['editors'] = str(pub.editors)
                    if pub.ee:
                        pdict['ee'] = str(pub.ee)
                    if pub.isbn:
                        pdict['isbn'] = str(pub.isbn)
                    if pub.journal:
                        pdict['journal'] = str(pub.journal)
                    if pub.mdate:
                        pdict['mdate'] = str(pub.mdate)
                    if pub.month:
                        pdict['month'] = str(pub.month)
                    if pub.number:
                        pdict['number'] = str(pub.number)
                    if pub.pages:
                        pdict['pages'] = str(pub.pages)
                    if pub.publisher:
                        pdict['publisher'] = str(pub.publisher)
                    if pub.school:
                        pdict['school'] = str(pub.school)
                    # if pub.series:
                    #     pdict['series'] = str(pub.series)
                    # if pub.sub_type:
                    #     pdict['sub_type'] = str(pub.sub_type)
                    if pub.type:
                        pdict['type'] = str(pub.type)
                    if pub.url:
                        pdict['url'] = str(pub.url)
                    if pub.volume:
                        pdict['volume'] = str(pub.volume)
                    if pub.year:
                        pdict['year'] = str(pub.year)

                    tempdict['id_publication_' + pub.url] = pdict
                    filename = str(pub.url)
                    # filename = str(count)
                    # for j in range(5-len(filename)):
                    #     filename = '0'+filename

                    fout = codecs.open(
                        directory + '/nn/pub' + filename.replace('/', '_') + '.yml', 'w', 'utf-8')
                    out = yaml.dump(
                        tempdict, default_flow_style=False, default_style='"')
                    fout.write(out)
                    fout.close()
                    count = count + 1
                    # adict['id_publication_' + pub.url] = pdict
                    time.sleep(0.5)
                    # adict['id_publication_'+re.sub(r'[^a-zA-Z]','_',pub.title.lower())]
                    # = pdict
            except Exception as e:
                print('\nwrong: ' + str(i) + " " + pub.title + " ")
                print(e)
                pass

        # use the full name of the people as the id
        fdict[
            'id_' + name[len(name) - 1].lower() + '_' + name[0].lower()] = adict

    # fout = codecs.open(directory + '/publications.yml', 'w', 'utf-8')
    # out = yaml.dump(fdict, default_flow_style=False, default_style='"')
    # fout.write(out)
    # fout.close()
