# -*- coding: utf-8 -*-
"""
Created on Fri Aug 31 13:20:11 2018

@author: suvod
"""

import nltk.corpus
from nltk.stem import PorterStemmer,SnowballStemmer
from nltk.stem import WordNetLemmatizer
import networkx as nx
import numpy as np

class utils(object):
    
    def __init__(self):
        self.name = ''
        
    def stemming(self,x):
        port_stem = PorterStemmer()
        words = []
        for word in x.split(' '):
            words.append(port_stem.stem(word))
        return ' '.join(words)
    
    def create_graph(self,matrix):
        gr = nx.Graph()
        rows,cols = np.where(matrix > 0)
        edges = zip(rows.tolist(), cols.tolist())
        gr = nx.Graph()
        gr.add_edges_from(edges)
        return dict(gr.degree(gr.nodes())),gr