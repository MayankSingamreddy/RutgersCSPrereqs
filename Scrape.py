import spacy

nlp = spacy.load("en_core_web_sm")
import requests

from bs4 import BeautifulSoup

urls = ['https://www.cs.rutgers.edu/academics/undergraduate/course-synopses/course-details/01-198-111-introduction-to-computer-science','https://www.cs.rutgers.edu/academics/undergraduate/course-synopses/course-details/01-198-112-data-structures','https://www.cs.rutgers.edu/academics/undergraduate/course-synopses/course-details/01-198-437-database-systems-implementation']

i = 0

outside = []
placementCheck = False

for url in urls:
    outside.append([' ',[],[],])

    res = requests.get(url)
    html_page = res.content
    soup = BeautifulSoup(html_page, 'html.parser')
    text = soup.find_all(text=True)

    output = ''
    blacklist = [
    	'[document]',
    	'noscript',
    	'header',
    	'html',
    	'meta',
    	'head',
    	'input',
    	'script',
    	# there may be more elements you don't want, such as "style", etc.
    ]

    for t in text:
    	if t.parent.name not in blacklist:
    		output += '{} '.format(t)

    brackets = []
    doc = nlp(output)
    for sent in doc.sents:
        brackets.append(sent.text.rstrip().replace(u'\xa0', u' ').replace(u'\n', u'').replace(u'\t',u' '))

    #print(brackets)

    y = 0
    for line in brackets:
        if("Course Details" in line):
            if(":" in line):
                pos_courseCode = line.find(':')-2
                outside[i][0] = line[pos_courseCode : pos_courseCode+11]
            else:
                pos_courseCode = brackets[y+1].find(':')-2
                outside[i][0] = brackets[y+1][pos_courseCode : pos_courseCode+11]
        if("Prerequisite information:" in line):
            doc = nlp(brackets[y+1])
            for token in doc:
                if(token.text=='-'):
                    break
                if(token.text == "or" or token.text == ";" or token.text == "in" or token.text == "." or token.text == " "):
                    continue
                if(token.text == 'placement'):
                    placementCheck = True
                    continue
                else:
                    if(placementCheck==True):
                        outside[i][1].append("placement in " + token.text)
                        placementCheck = False
                    else:
                        outside[i][1].append(token.text)



        #end of line loop
        y+=1

    #end of url loop
    i+=1


print(outside)
