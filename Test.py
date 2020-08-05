import spacy
import csv
from spacy import displacy
nlp = spacy.load('en_core_web_sm')

'''
print("SHALLOW PARSE")
conference_text = ('01:198:323 or  01:640:373; Calc1 .')
conference_doc = nlp(conference_text)
# Extract Noun Phrases
for chunk in conference_doc.noun_chunks:
    print (chunk)


print("ENTITY RECOGNITION")
piano_class_text = ('01:198:323 or  01:640:373; Calc1 .')
piano_class_doc = nlp(piano_class_text)
for ent in piano_class_doc.ents:
    print(ent.text, ent.label_)

with open('CocaCola.csv','r') as csv_file:
    reader =csv.reader(csv_file)
    for row in reader:
        print(row)
'''
print("tokens")
about_text = ('Prerequisites: 01:640:285 and (01:640:477 or 01:960:381).')
about_doc = nlp(about_text)
for token in about_doc:
    if not token.is_stop:
        print (token)

'''
print("DEPENDENCY PARSING")
piano_text = "In 2018, we had 13 of our workers working on our 5 man team of babies. "
piano_doc = nlp(piano_text)
for token in piano_doc:
    print (token.text, token.tag_, token.head.text, token.dep_)

displacy.serve(piano_doc, style='dep')
'''
