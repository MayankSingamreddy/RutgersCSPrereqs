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

'''
placementCheck = False
corequisiteCheck = False

for url in urls:
    outside.append([' ',[],'Computer Science'])

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






urlsEE = ['https://www.ece.rutgers.edu/14332376-virtual-reality',
          'https://www.ece.rutgers.edu/14332424-introduction-information-and-network-security',
          'https://www.ece.rutgers.edu/14332451-introduction-parallel-and-distributed-programming',
          'https://www.ece.rutgers.edu/14332452-software-engineering',
          'https://www.ece.rutgers.edu/14332453-mobile-app-engineering-and-user-experience',
          'https://www.ece.rutgers.edu/14332456-network-centric-programming',
          'https://www.ece.rutgers.edu/14332472-introduction-robotics-and-computer-vision']


placementCheck = False

for url in urlsEE:
    outside.append([' ',[], 'Electrical Engineering'])

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






'''

'''REMEMBER TO ADD THE INDENT BACK TO EVERYTHING AFTER UNCOMMENTING'''

mathClasses = ['01:640:338 Discrete and Probabilistic Models in Biology',
               '01:640:348 Cryptography',
               '01:640:354 Linear Optimization (3)',
               '01:640:428 Graph Theory (3)',
               '01:640:453',
               '01:640:454',
               '01:640:461']

placementCheck = False

for className in mathClasses:
    outside.append([className[:11],[], 'Mathematics'])

    url = 'https://catalogs.rutgers.edu/generated/nb-ug_current/pg442.html'
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
        if(className in line):
            ctr = y +1
            while("Prerequisite" not in brackets[ctr]):
                ctr+=1

            doc = nlp(brackets[ctr+1])
            for token in doc:
                if token.text == '.':
                    break
                if( token.text == ':' or token.text == "(" or token.text == ')' or token.text == 'either' or token.text == 'permission' or token.text == 'of' or token.text == 'department'):
                    continue
                else:
                    outside[i][1].append(token.text)
            if("Corequisite:" in brackets[ctr+2]):
                if("01:" in brackets[ctr+2]):
                    doc = nlp(brackets[ctr+2])
                    for token in doc:
                        if(token.text == '.'):
                            break
                        if("01:" in token.text):
                            outside[i][1].append(token.text)
                elif("01:" in brackets[ctr+3]):
                    doc = nlp(brackets[ctr+3])
                    for token in doc:
                        if(token.text == '.'):
                            break
                        if("01:" in token.text):
                            outside[i][1].append(token.text)

        #end of line loop
        y+=1

    #end of url loop
    i+=1





print(outside)
