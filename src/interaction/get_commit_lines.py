# -*- coding: utf-8 -*-
"""
Created on Tue Sep 11 12:01:40 2018

@author: suvod
"""

from main.git_log import git2repo
import pygit2
import re
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
from datetime import datetime
import re, unicodedata
import nltk.corpus
from nltk.stem import PorterStemmer,SnowballStemmer
from nltk.stem import WordNetLemmatizer
from pygit2 import GIT_SORT_TOPOLOGICAL, GIT_SORT_REVERSE
from main.utils import utils
import threading
from multiprocessing import Queue
from threading import Thread
import math
import os
from multiprocessing import Pool, cpu_count
import platform
from os.path import dirname as up
import sys

class ThreadWithReturnValue(Thread):
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs={}, Verbose=None):
        Thread.__init__(self, group, target, name, args, kwargs)
        self._return = None
    def run(self):
        #print(type(self._target))
        if self._target is not None:
            self._return = self._target(*self._args,
                                                **self._kwargs)
    def join(self, *args):
        Thread.join(self, *args)
        return self._return


class create_code_interaction_graph(object):
    
    def __init__(self,repo_url,repo_name):
        self.repo_url = repo_url
        self.repo_name = repo_name
        self.repo_obj = git2repo.git2repo(self.repo_url,self.repo_name)
        self.repo = self.repo_obj.clone_repo()
        if platform.system() == 'Darwin' or platform.system() == 'Linux':
            self.repo_path = up(os.getcwd()) + '/temp_repo/' + repo_name
            self.file_path = up(os.getcwd()) + '/data/' + repo_name + '_commit.pkl'
        else:
            self.repo_path = up(os.getcwd()) + '\\temp_repo\\' + repo_name
            self.file_path = up(os.getcwd()) + '\\data\\' + repo_name + '_commit.pkl'
        self.commits = self.read_commits()
        self.commit_df = pd.DataFrame(self.commits, columns = ['commit_object'])
        self.diffs = self.get_diffs()
        print('diffs done')
        self.cores = cpu_count()
        
    def read_commits(self):
        df = pd.read_pickle(self.file_path)
        df_commit_id = df.commit_number.values.tolist()
        commits = []
        for commit in df_commit_id:
            obj = self.repo.get(commit)
            if obj == None:
                print(commit)
                continue
            commits.append(obj)
        return commits
        
    def get_diffs(self):
        commmit_id = []
        for i in self.commits:
            commmit_id.append(i.id)
        diffs = self.repo_obj.get_diffs(commmit_id)
        return diffs
    
    def get_bug_creators(self,diffs):
        bug_creator = []
        for value in diffs:
            #print(diffs[value])
            _diff_files = diffs[value]['files']
            self.repo.head.set_target(diffs[value]['object'].parent_ids[0])
            for _value in _diff_files:
                try:
                    file_path = _diff_files[_value]['file_path']
                    #blame = self.repo_obj.get_blame(file_path)
                    bug_creator.append([diffs[value]['object'].committer.name , len(_diff_files[_value]['old_lines'])])
                except Exception as e:
                    print(file_path,e)
                    continue
        bug_creator_df = pd.DataFrame(bug_creator, columns = ['committer1','ob'])
        bug_creator_df = bug_creator_df.groupby(['committer1']).sum()
        return bug_creator_df


    
    
    def get_user_node_degree(self):
        graph_util = utils.utils()
        print("starting graph")
        connection_matrix = self.get_bug_creators(self.diffs)
        connection_matrix.to_csv('temp.csv')
        print("Done everything")
        self.repo_obj.repo_remove()
        return connection_matrix#,connection_matrix
    