import spacy

nlp = spacy.load("en_core_web_sm")
import requests

from bs4 import BeautifulSoup

urls = ['https://math.rutgers.edu/academics/undergraduate/courses/987-01-640-461-mathematical-logic']

i = 0


for url in urls:

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
        brackets.append(sent.text.rstrip().replace(u'\xa0', u' ').replace(u'\n', u'').replace(u'\t',u' ').replace(u'  ',u' '))

print(brackets)
