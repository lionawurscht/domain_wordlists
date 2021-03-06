from bs4 import BeautifulSoup
import requests
import nltk
import itertools
import hunspell

hobj = hunspell.HunSpell('en_US.dic', 'en_US.aff')

neurowords = set()
# english_vocab = set(w.lower() for w in nltk.corpus.words.words())

def extract_tags(url, tag):
    soup = BeautifulSoup(requests.get(url).text, "html.parser")
    terms=[nltk.word_tokenize(t.text) for t in soup(tag)]
    merged = list(itertools.chain(*terms))
    return set([ (w.lower() if w.istitle() else w) for w in merged if w.isalpha() and len(w) > 2 and not(w.isupper()) and not(hobj.spell(w) or hobj.spell(w.lower())) ])
#    return set([ w for w in merged if w.isalpha() and len(w) > 2 and not(w.isupper()) and not(hobj.spell(w) or hobj.spell(w.lower())) ])

# Erm, copyright? erm?
url = u'https://www.ncbi.nlm.nih.gov/books/NBK10981/'
# We want the <dt></dt> bits
neurowords.update(extract_tags(url, u'dt'))

# ditto re the copyright
url = 'http://michaeldmann.net/glossary.html'
# For this one we want the <strong></strong> bits and the first character
# needs to be lowercased
neurowords.update(extract_tags(url, u'strong'))

# Remove common English words—at least, according to nltk
# (Might be better to compare against hunspell instead but I dunno how)
# neurowords = neurowords - english_vocab

with open('neuroscience-en.txt', 'w') as file_handler:
    for item in sorted(neurowords):
        status = file_handler.write("{}\n".format(item))
