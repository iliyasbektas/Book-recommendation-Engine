#!/usr/bin/env python
# coding: utf-8

# In[15]:


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
# from webdriver_manager.chrome import ChromeDriverManager
# from webdriver_manager.firefox import GeckoDriverManager
from bs4 import BeautifulSoup
import pandas as pd
import re
import requests
#import spacy
from tqdm import tqdm
import urllib
from urllib.request import urlopen
from nltk.stem import WordNetLemmatizer 
# lemmatizer = WordNetLemmatizer()
import nltk
nltk.download('stopwords')
nltk.download('punkt')
from nltk.corpus import stopwords
import string
from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize
import os
sw = stopwords.words('english')
punct_correction = string.punctuation + '..' + '...' + "''" + "``"
from collections import Counter
import math
from collections import defaultdict


# In[4]:


def prepare_search(dscr):
    
    dscr = re.sub(r'[^\w\s]', '', dscr) # removing digits
    
    dscr_tokens = nltk.word_tokenize(dscr) # Not considering the repetitive token
    dscr_tokens_lower = []
    for e in dscr_tokens:
        dscr_tokens_lower.extend(re.split("—|-|'",e.lower()))
    
    dscr2 = [n for n in dscr_tokens_lower if not n.lower() in sw]  # stop_words  and punctuation removal 
    dscr3 = [n for n in dscr2 if not n in remove_punctuation]
    
    dscr4 = []
    for e in dscr3:
        
        dscr4.append(PorterStemmer().stem(e)) #Stemming
    
    dscr5 = []
    for e in dscr4:
        if e[0].isnumeric() == False:
            if e not in dscr5:
                dscr5.append(e)
      
    
    return dscr5


# In[18]:


def dict_prep(tkn_dscr):
    ws = []
    for a in tqdm(tkn_dscr):
        for b in a:
            if b not in ws:
                ws.append(b)
    ws=sorted(ws)
    vocab={}
    for i in tqdm(range(len(ws))):
        vocab.update({ws[i]:i})
    voc = vocab

    vocab={}
    for i in tqdm(range(len(ws))):
        vocab.update({ws[i] : [] })
    
    for a, b in tqdm(enumerate(tkn_dscr)):
        for tkn in b:
            vocab[tkn].append(a)
    
    inv_idx = {}
    
    for a,b in tqdm(enumerate(tkn_dscr)):
        for tkn in b:
            inv_idx.update({voc[tkn] : vocab[tkn]})
            
    return inv_idx, voc, vocab


# In[9]:


def query(query_str, df, inv_idx, voc):
    nq = prepare_search(query_str)
    sett = set(inv_idx[voc[nq[0]]])
    
    for w in tqdm(nq):
        sett = sett.intersection(set(inv_idx[voc[w]]))
    
    out = df.iloc[list(sett)]
    return out.sort_index()[['bookTitle','Plot','url']]


# In[11]:


def prepare_search2(dscr):
    
    dscr = re.sub(r'[^\w\s]', '', dscr) # removing digits
    
    dscr_tokens = nltk.word_tokenize(dscr) # Not considering the repetitive token
    dscr_tokens_lower = []
    for e in dscr_tokens:
        dscr_tokens_lower.extend(re.split("—|-|'",e.lower()))
    
    dscr2 = [n for n in dscr_tokens_lower if not n.lower() in sw]  # stop_words  and punctuation removal 
    dscr3 = [n for n in dscr2 if not n in remove_punctuation]
    
    dscr4 = []
    for e in dscr3:
        if e[0].isnumeric() == False:
            dscr4.append(PorterStemmer().stem(e)) #Stemming
    return dscr4


# In[13]:


def tf_score(tokenized_dscr):
    total = 0
    for k, v in tokenized_dscr.items():
        total = total + v #numbers of total tkns in the plot
    tf = {}
    for tkn, rip in tokenized_dscr.items():#the values in this dictionary are the ripetition of that specific tkn
        tf[tkn] = rip / total
    return tf


# In[17]:


def new_inverse_index(inv_idx, voc, empty_list, dic):
    
    new_voc = dict([(value, k) for k, value in voc.items()])
    
    for k in tqdm(inv_idx.keys()):
        l = []
        tkn = new_voc[k]
        for i in inv_idx[k]:  
            l.append((i, empty_list[i][tkn]*dic[tkn]))
        inv_idx[k] = l
    return inv_idx

