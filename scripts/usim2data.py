import sys
import csv
from collections import defaultdict
import os
from html.parser import HTMLParser

class MyHTMLParser(HTMLParser):

    def __init__(self):
        HTMLParser.__init__(self)
        self.lemma2id2data = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: None)))
        self.lemma = None
        self.id_ = None
        self.tag = None
        self.endtag = None
        self.sentence = None
        self.preceding = None
        self.following = None
        self.target_id = None
    
    def handle_starttag(self, tag, attrs):
        print("Encountered a start tag:", tag, attrs)
        if tag == 'lexelt':
            self.lemma = attrs[0][1]
        if tag == 'instance':
            self.id_ = attrs[0][1]
        if tag == 'context':
            self.sentence = ''
        self.tag = tag

    def handle_endtag(self, endtag):
        print("Encountered an end tag :", endtag)
        if endtag == 'instance':
            lemma = self.lemma
            id_ = self.id_
            preceding = self.preceding if self.preceding!=None else ' '
            following = self.following if self.following!=None else ' '
            self.lemma2id2data[lemma][id_]['sentence'] = self.sentence.replace('\n','').replace('\t','').replace('    ','')
            self.lemma2id2data[lemma][id_]['preceding'] = preceding.replace('\n','').replace('\t','').replace('    ','')
            self.lemma2id2data[lemma][id_]['following'] = following.replace('\n','').replace('\t','').replace('    ','')
            self.lemma2id2data[lemma][id_]['target_id'] = self.target_id        
        self.endtag = endtag

    def handle_data(self, data):
        print("Encountered some data  :", data, self.tag, self.endtag)
        if (self.tag == 'context' and (self.endtag == 'instance' or self.endtag == 'lexelt' or self.endtag == None)) or (self.tag == 'head' and self.endtag == 'head'):
            self.sentence += data
        if self.tag == 'head' and self.endtag == 'context':
            self.following = data
        if self.tag == 'head' and (self.endtag == 'instance' or self.endtag == 'lexelt' or self.endtag == None):
            self.sentence += data
            self.sentence = self.sentence.replace('\n','').replace('\t','').replace('    ','')
            sentence_split = self.sentence.split()
            self.target_id = len(sentence_split)-1
        if self.tag == 'wcontext' and (self.endtag == 'instance' or self.endtag == 'lexelt' or self.endtag == None):
            self.preceding = data


            
[_, data, annotations, datadir] = sys.argv

            
# parse an HTML file by name
with open(data, encoding='iso-8859-1') as xmlfile:
    data = xmlfile.read()
    parser = MyHTMLParser()
    parser.feed(data)
    lemma2id2data = parser.lemma2id2data

date = 2006    
lemma2id2context = defaultdict(lambda: defaultdict(lambda: None))
for lemma, id2data in lemma2id2data.items():
    lemma, pos = lemma.split('.')
    for id_, data in id2data.items():
        identifier = lemma+'-'+id_
        grouping = '1'
        preceding = data['preceding'].strip(' ')
        sentence = data['sentence']
        following = data['following'].strip(' ')
        leading_spaces = len(sentence) - len(sentence.lstrip(' '))
        index = int(data['target_id']) - leading_spaces
        sentence = sentence.strip(' ')
        context = preceding + ' ' + sentence + ' ' + following
        index = len(preceding.split()) + index
        index_sentence = str(len(preceding.split()))+':'+str(len(preceding.split())+len(sentence.split()))
        context = {'lemma':lemma, 'pos':pos, 'date':date, 'grouping':grouping, 'identifier':identifier, 'description':' ', 'context':' ', 'indexes_target_token':' ', 'indexes_target_sentence':' ', 'context_tokenized':context, 'indexes_target_token_tokenized':index, 'indexes_target_sentence_tokenized':index_sentence}  
        lemma2id2context[lemma][lemma+'-'+id_] = context

    
with open(annotations, encoding='utf-8') as csvfile: 
    reader = csv.DictReader(csvfile, delimiter=',',quoting=csv.QUOTE_NONE,strict=True)
    table = [row for row in reader]

lemma2data = defaultdict(lambda: [])
for row in table:    
    lemma, pos = row['lemma'].split('.')
    id1 = row['lexsub_id1']
    id2 = row['lexsub_id2']
    comment = ' '
    judgment = row['judgment']
    annotator = row['user_id']
    if annotator == 'avg':
        continue
    data = {'identifier1':lemma+'-'+id1,'identifier2':lemma+'-'+id2,'annotator':annotator,'judgment':float(judgment),'comment':comment,'lemma':lemma}    
    lemma2data[lemma].append(data)
    
for lemma in lemma2data:
    output_folder = datadir+'/' +lemma+'/'    
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)    

    # Export data
    with open(output_folder +'judgments.csv', 'w') as f:  
        w = csv.DictWriter(f, lemma2data[lemma][0].keys(), delimiter='\t', quoting = csv.QUOTE_NONE, quotechar='')
        w.writeheader()
        w.writerows(lemma2data[lemma])

    contexts = list(lemma2id2context[lemma].values())
    
    # Export data
    with open(output_folder +'uses.csv', 'w') as f:  
        w = csv.DictWriter(f, contexts[0].keys(), delimiter='\t', quoting = csv.QUOTE_NONE, quotechar='')
        w.writeheader()
        w.writerows(contexts)
