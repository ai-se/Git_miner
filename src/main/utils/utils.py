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
    
    def printProgressBar(self,iteration, total, prefix='Progress:', suffix='Complete',
                     decimals=2, length=50, fill='█'):
        """
        Call in a loop to create terminal progress bar
    
        Parameters
        ----------
        iteration: int 
            Current iteration
        total: int
            Total iterations
        prefix: str
            Prefix string 
        suffix: str
            Suffix string
        decimals: int
            Positive number of decimals in percent complete
        length: int 
            Character length of bar
        fill: str
            Bar fill character (Str)
        """
        percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / total))
        filledLength = int(length * iteration / total)
        bar = fill * filledLength + '-' * (length - filledLength)
        print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end='\r')
        # Print New Line on Complete
        if iteration == total:
            print()