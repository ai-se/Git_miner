# -*- coding: utf-8 -*-
"""
Created on Fri Aug 31 13:20:11 2018

@author: suvod
"""

import nltk.corpus
from nltk.stem import PorterStemmer,SnowballStemmer
from nltk.stem import WordNetLemmatizer

class utils(object):
    
    def __init__(self):
        self.name = ''
        
    def stemming(self,x):
        port_stem = PorterStemmer()
        words = []
        for word in x.split(' '):
            words.append(port_stem.stem(word))
        return ' '.join(words)