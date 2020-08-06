import spacy

nlp = spacy.load("en_core_web_sm")
import requests

from bs4 import BeautifulSoup

urls = ['https://www.cs.rutgers.edu/academics/undergraduate/course-synopses/course-details/01-198-111-introduction-to-computer-science',
        'https://www.cs.rutgers.edu/academics/undergraduate/course-synopses/course-details/01-198-112-data-structures',
        'https://www.cs.rutgers.edu/academics/undergraduate/course-synopses/course-details/01-198-205-introduction-to-discrete-structures-i',
        'https://www.cs.rutgers.edu/academics/undergraduate/course-synopses/course-details/01-198-206-introduction-to-discrete-structures-ii',
        'https://www.cs.rutgers.edu/academics/undergraduate/course-synopses/course-details/01-198-211-computer-architecture',
        'https://www.cs.rutgers.edu/academics/undergraduate/course-synopses/course-details/01-198-344-design-and-analysis-of-computer-algorithms',
        'https://www.cs.rutgers.edu/academics/undergraduate/course-synopses/course-details/01-198-213-software-methodology',
        'https://www.cs.rutgers.edu/academics/undergraduate/course-synopses/course-details/01-198-214-systems-programming',
        'https://www.cs.rutgers.edu/academics/undergraduate/course-synopses/course-details/01-198-314-principles-of-programming-languages',
        'https://www.cs.rutgers.edu/academics/undergraduate/course-synopses/course-details/01-198-323-numerical-analysis-and-computinghttps://www.cs.rutgers.edu/academics/undergraduate/course-synopses/course-details/01-198-324-numerical-methods',
        'https://www.cs.rutgers.edu/academics/undergraduate/course-synopses/course-details/01-198-334-introduction-to-imaging-and-multimedia',
        'https://www.cs.rutgers.edu/academics/undergraduate/course-synopses/course-details/01-198-336-principles-of-information-and-data-management',
        'https://www.cs.rutgers.edu/academics/undergraduate/course-synopses/course-details/01-198-352-internet-technology',
        'https://www.cs.rutgers.edu/academics/undergraduate/course-synopses/course-details/01-198-411-computer-architecture-ii',
        'https://www.cs.rutgers.edu/academics/undergraduate/course-synopses/course-details/01-198-415-compilers',
        'https://www.cs.rutgers.edu/academics/undergraduate/course-synopses/course-details/01-198-416-operating-systems-design',
        'https://www.cs.rutgers.edu/academics/undergraduate/course-synopses/course-details/01-198-417-distributed-systems-concepts-and-design',
        'https://www.cs.rutgers.edu/academics/undergraduate/course-synopses/course-details/01-198-419-computer-security',
        'https://www.cs.rutgers.edu/academics/undergraduate/course-synopses/course-details/01-198-424-modeling-and-simulation-of-continuous-systems',
        'https://www.cs.rutgers.edu/academics/undergraduate/course-synopses/course-details/01-198-425-computer-methods-in-statistics',
        'https://www.cs.rutgers.edu/academics/undergraduate/course-synopses/course-details/01-198-428-introduction-to-computer-graphics',
        'https://www.cs.rutgers.edu/academics/undergraduate/course-synopses/course-details/01-198-431-software-engineering',
        'https://www.cs.rutgers.edu/academics/undergraduate/course-synopses/course-details/01-198-437-database-systems-implementation',
        'https://www.cs.rutgers.edu/academics/undergraduate/course-synopses/course-details/01-198-440-introduction-to-artificial-intelligence',
        'https://www.cs.rutgers.edu/academics/undergraduate/course-synopses/course-details/01-198-442-topics-in-computer-science',
        'https://www.cs.rutgers.edu/academics/undergraduate/course-synopses/course-details/01-198-443-topics-in-computer-science',
        'https://www.cs.rutgers.edu/academics/undergraduate/course-synopses/course-details/01-198-444-topics-in-computer-science',
        'https://www.cs.rutgers.edu/academics/undergraduate/course-synopses/course-details/01-198-452-formal-languages-and-automata',
        'https://www.cs.rutgers.edu/academics/undergraduate/course-synopses/course-details/01-198-460-introduction-to-computational-robotics',
        'https://www.cs.rutgers.edu/academics/undergraduate/course-synopses/course-details/01-198-493-independent-study-in-computer-science',
        'https://www.cs.rutgers.edu/academics/undergraduate/course-synopses/course-details/01-198-494-independent-study-in-computer-science']



i = 0

outside = []


placementCheck = False
corequisiteCheck = False

for url in urls:
    outside.append([' ',[],'Computer Science',i])

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
            if(":" in line):
                doc = nlp(line)
                for token in doc:
                    if('01:' in token.text):
                        outside[i][1].append(token.text)
            doc = nlp(brackets[y+1])
            for token in doc:
                if(token.text=='-' or token.text =='A' or token.text == 'Credit' or token.text =='('):
                    break
                if(token.text == "or" or token.text == ";" or token.text == "in" or token.text == "." or token.text == " " or token.text == '†' or token.text == ':'):
                    continue
                if(token.text == 'placement'):
                    placementCheck = True
                    continue
                if(token.text == 'Corequisite'):
                    corequisiteCheck = True
                    continue
                if(token.text == 'Permission'):
                    outside[i][1].append("Permission from Instructor")
                    break
                if(":" in token.text and corequisiteCheck == True):
                    outside[i][1].append("Corequisite: " + token.text)
                    corequisiteCheck = False
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

#END OF COMP SCI


#START OF Electrical Engineering

urlsEE = ['https://www.ece.rutgers.edu/14332376-virtual-reality',
          'https://www.ece.rutgers.edu/14332424-introduction-information-and-network-security',
          'https://www.ece.rutgers.edu/14332451-introduction-parallel-and-distributed-programming',
          'https://www.ece.rutgers.edu/14332452-software-engineering',
          'https://www.ece.rutgers.edu/14332453-mobile-app-engineering-and-user-experience',
          'https://www.ece.rutgers.edu/14332456-network-centric-programming',
          'https://www.ece.rutgers.edu/14332472-introduction-robotics-and-computer-vision']


placementCheck = False

for url in urlsEE:
    outside.append([' ',[], 'Electrical Engineering',i])

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
        if("You are here" in line):
            if(":" in brackets[y+2]):
                pos_courseCode = brackets[y+2].find(':')-2
                outside[i][0] = brackets[y+2][pos_courseCode : pos_courseCode+11]
            elif(':' in brackets[y+3]):
                pos_courseCode = brackets[y+3].find(':')-2
                outside[i][0] = brackets[y+3][pos_courseCode : pos_courseCode+11]
        if("Pre-Requisite courses:" in line):
            if('14:' in line or '01:' in line):
                doc = nlp(line)
                for token in doc:
                    if('14:' not in token.text and '01:' not in token.text):
                        continue
                    if('14:' in token.text or '01:' in token.text):
                        outside[i][1].append(token.text)
            if('14:' in brackets[y+1] or '01:' in brackets[y+1]):
                doc = nlp(line)
                for token in doc:
                    if('14:' not in token.text and '01:' not in token.text):
                        continue
                    if('14:' in token.text or '01:' in token.text):
                        outside[i][1].append(token.text)
        if("Co-Requisite courses:" in line):
            offsetNum = brackets[y].find('courses:')-2
            if('14:' in brackets[y][offsetNum:] or '01:' in brackets[y][offsetNum:]):
                doc = nlp(brackets[y][offsetNum])
                for token in doc:
                    if('14:' not in token.text and '01:' not in token.text):
                        continue
                    if('14:' in token.text or '01:' in token.text):
                        outside[i][1].append(token.text)
            if('14:' in brackets[y+1]):
                doc = nlp(brackets[y+1])
                for token in doc:
                    outside[i][1].append(token.text)


        #end of line loop
        y+=1

    #end of url loop
    i+=1

#end of Electrical Engineering



#START OF Mathematics

urlsMath = ['https://math.rutgers.edu/academics/undergraduate/courses/964-01-640-355-game-theory',
          'https://math.rutgers.edu/academics/undergraduate/courses/986-01-640-454-combinatorics',
          'https://math.rutgers.edu/academics/undergraduate/courses/987-01-640-461-mathematical-logic',
          'https://math.rutgers.edu/academics/undergraduate/courses/985-01-640-453-theory-of-linear-optimization',
          'https://math.rutgers.edu/academics/undergraduate/courses/963-01-640-354-linear-optimization',
          'https://math.rutgers.edu/academics/undergraduate/courses/977-01-640-428-graph-theory']

placementCheck = False
digitCheck = False

for url in urlsMath:
    outside.append(['',[], 'Mathematics',i])

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
        if("Courses" in line):
            if('01:' in brackets[y+1]):
                outside[i][0] = brackets[y+1][:11]
        if("Prerequisite" in line):
            prereqPos = line.find(':')
            doc = nlp(brackets[y][prereqPos:])
            for token in doc:
                if(token.text == '.'):
                    break
                if(any(char.isdigit() for char in token.text) == False):
                    continue
                else:
                    outside[i][1].append(token.text)

        #end of line loop
        y+=1

    #end of url loop
    i+=1

outside.append(['01:640:338',['01:640:250','01:640:251','01:640:477', '01:198:206', '01:960:381'], 'Mathematics',i])
i+=1
outside.append(['01:640:348', ['01:640:250','01:640:300','01:640:356','01:640:477'],'Mathematics',i])
i+=1
#END OF Mathematics



#START OF Philosophy

url = 'https://catalogs.rutgers.edu/generated/nb-ug_0507/pg20657.html'
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


namesPhil = ['Applied Symbolic Logic',
             '01:730:407 Intermediate Logic I (3)',
             '01:730:408 Intermediate Logic II (3)',
             '01:730:329 Minds, Machines, and Persons (3)',
             '01:730:424']

for name in namesPhil:
    outside.append(['',[], 'Philosophy',i])

    if("01:" not in name):
        outside[i][0] = '01:730:315'
    if("01:" in name):
        namePos = name.find("01:")
        outside[i][0] = name[namePos:namePos+11]


    y = 0
    for line in brackets:
        if(name in line):
            ctr = y
            while("Prerequisite" not in brackets[ctr]):
                ctr+=1
            if("01:" in brackets[ctr]):
                doc = nlp(brackets[ctr])
                for token in doc:
                    if(any(char.isdigit() for char in token.text)):
                        outside[i][1].append(token.text)
                    if(token.text == '.'):
                        break
            elif("01:" in brackets[ctr+1]):
                doc = nlp(brackets[ctr+1])
                for token in doc:
                    if(any(char.isdigit() for char in token.text)):
                        outside[i][1].append(token.text)
                    if(token.text == '.'):
                        break
        y+=1

    #end of url loop
    i+=1


#end of Philosophy





#start of Linguistics
outside.append(['01:615:441', ['(B) Course','01:615:305','01:615:315','01:615:325','01:615:350'],'Linguistics',i])
i+=1
#end of Linguistics




#start of statistics

urlsStats = ['https://statistics.rutgers.edu/course-descriptions/511-01-960-384-intermediate-statistical-analysis-3-formerly-960-380',
          'https://statistics.rutgers.edu/course-descriptions/518-01-960-476-introduction-to-sampling-3',
          'https://statistics.rutgers.edu/course-descriptions/516-01-960-463-regression-methods-3',
          'https://statistics.rutgers.edu/course-descriptions/521-01-960-486-computing-and-graphics-in-applied-statistics-3']

placementCheck = False
digitCheck = False

for url in urlsStats:
    outside.append(['',[], 'Statistics', i])

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
        if(y==0):
            outside[i][0] = line[0:11]
        if("Prerequisite" in line):
            prereqPos = line.find(':')
            doc = nlp(brackets[y][prereqPos:])
            for token in doc:
                if(token.text == '.'):
                    break
                if(any(char.isdigit() for char in token.text) == False):
                    continue
                else:
                    outside[i][1].append(token.text)

        #end of line loop
        y+=1
    if not outside[i][1]:
        outside[i][1].append('Level 2')
    #end of url loop
    i+=1


#END OF Statistics








print(outside)
