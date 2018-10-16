# -*- coding: utf-8 -*-
"""
Created on Tue Sep 11 12:01:40 2018

@author: suvod
"""

import git2repo
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
import utils
import threading
from multiprocessing import Queue
from threading import Thread
import math
import os
import platform

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
        if platform.system() == 'Darwin':
            self.repo_path = os.getcwd() + '/temp_repo/' + repo_name
            self.file_path = os.getcwd() + '/data/' + repo_name + '_commit.pkl'
        else:
            self.repo_path = os.getcwd() + '\\temp_repo\\' + repo_name
            self.file_path = os.getcwd() + '\\data\\' + repo_name + '_commit.pkl'
        #self.commits = self.repo_obj.get_commit_objects()
        self.commits = self.read_commits()
        self.commit_df = pd.DataFrame(self.commits, columns = ['commit_object'])
        #self.committed_files = self.repo_obj.get_committed_files()
        self.diffs = self.get_diffs()
        
    def read_commits(self):
        df = pd.read_pickle(self.file_path)
        df_commit_id = df.commit_number.values.tolist()
        commits = []
        for commit in df_commit_id:
            obj = self.repo.get(commit)
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
            _diff_files = diffs[value]['files']
            self.repo.head.set_target(diffs[value]['object'].parent_ids[0])
            for _value in _diff_files:
                try:
                    file_path = _diff_files[_value]['file_path']
                    blame = self.repo_obj.get_blame(file_path)
                    for _line in _diff_files[_value]['old_lines']:
                        if _line != -1:
                            ref = blame.for_line(_line)
                            bug_creator.append([ref.final_committer.name,diffs[value]['object'].committer.name ,ref.orig_commit_id, 1])
                            #       break
                except:
                    continue
        bug_creator_df = pd.DataFrame(bug_creator, columns = ['committer1','committer2','commit','ob'])
        return bug_creator_df

    def create_adjacency_matrix(self):
        threads = []
        bug_creator_df = pd.DataFrame([], columns = ['committer1','committer2','commit','ob'])
        i = 0
        keys = list(self.diffs.keys())
        len_bd = len(self.diffs)
        sub_list_len = len_bd/20
        for i in range(20):
            sub_keys = keys[int(i*sub_list_len):int((i+1)*sub_list_len)]
            subdict = {x: self.diffs[x] for x in sub_keys if x in self.diffs}
            t = ThreadWithReturnValue(target = self.get_bug_creators, args = [subdict])
            threads.append(t)
        print(len(threads))
        for i in range(0,len(threads),20):
            print("Starting Thread group:",i)
            _threads = threads[i:i+20]
            for th in _threads:
                th.start()
            for th in _threads:
                response = th.join()
                bug_creator_df = pd.concat([bug_creator_df,response])
                bug_creator_df.reset_index(inplace = True, drop = True)
        bug_creator_df = bug_creator_df.drop(['commit'], axis = 1)
        df = bug_creator_df.groupby( ['committer1','committer2']).count()
        defect_count = []
        for key,value in df.iterrows():
            user1 = key[0]
            user2 = key[1]
            count = value.values.tolist()[0]
            defect_count.append([user1,user2,count])
        defect_count_df = pd.DataFrame(defect_count, columns = ['committer1','committer2', 'count'])
        uniq_users1 = defect_count_df.committer1.unique()
        uniq_users2 = defect_count_df.committer2.unique()
        uniq_users = np.unique(np.concatenate((uniq_users1,uniq_users2)))
        connection_matrix = np.ndarray(shape=(len(uniq_users),len(uniq_users)))
        connection_matrix = np.zeros((len(uniq_users),len(uniq_users)), dtype=np.int)
        user_dict = {}
        rev_user_dict = {}
        user_id = 0
        for i in range(len(uniq_users)):
            user_dict[uniq_users[i]] = user_id
            rev_user_dict[user_id] = uniq_users[i]
            user_id += 1
        for i in range(defect_count_df.shape[0]):
            changer = user_dict[defect_count_df.loc[i,'committer1']]
            changed = user_dict[defect_count_df.loc[i,'committer2']]
            connection_matrix[changer][changed] += defect_count_df.loc[i,'count']
            
        return connection_matrix,uniq_users,user_dict

    
#    def create_adjacency_matrix(self):
#        bug_creator = []
#        i = 0
#        for value in self.diffs:
#            _diff_files = self.diffs[value]['files']
#            print(i)
#            i += 1
#            self.repo.head.set_target(self.diffs[value]['object'].parent_ids[0])
#            for _value in _diff_files:
#                try:
#                    file_path = _diff_files[_value]['file_path']
#                    blame = self.repo_obj.get_blame(file_path)
#                    for _line in _diff_files[_value]['old_lines']:
#                        if _line != -1:
#                            ref = blame.for_line(_line)
#                            bug_creator.append([ref.final_committer.name,self.diffs[value]['object'].committer.name ,ref.orig_commit_id, 1])
#                            break
#                except:
#                    continue
#        bug_creator_df = pd.DataFrame(bug_creator, columns = ['committer1','committer2','commit','ob'])
#        bug_creator_df = bug_creator_df.drop(['commit'], axis = 1)
#        df = bug_creator_df.groupby( ['committer1','committer2']).count()
#        defect_count = []
#        for key,value in df.iterrows():
#            user1 = key[0]
#            user2 = key[1]
#            count = value.values.tolist()[0]
#            defect_count.append([user1,user2,count])
#        defect_count_df = pd.DataFrame(defect_count, columns = ['committer1','committer2', 'count'])
#        uniq_users1 = defect_count_df.committer1.unique()
#        uniq_users2 = defect_count_df.committer2.unique()
#        uniq_users = np.unique(np.concatenate((uniq_users1,uniq_users2)))
#        connection_matrix = np.ndarray(shape=(len(uniq_users),len(uniq_users)))
#        connection_matrix = np.zeros((len(uniq_users),len(uniq_users)), dtype=np.int)
#        user_dict = {}
#        rev_user_dict = {}
#        user_id = 0
#        for i in range(len(uniq_users)):
#            user_dict[uniq_users[i]] = user_id
#            rev_user_dict[user_id] = uniq_users[i]
#            user_id += 1
#        for i in range(defect_count_df.shape[0]):
#            changer = user_dict[defect_count_df.loc[i,'committer1']]
#            changed = user_dict[defect_count_df.loc[i,'committer2']]
#            connection_matrix[changer][changed] += defect_count_df.loc[i,'count']
#            
#        return connection_matrix,uniq_users,user_dict
    
    
    def get_user_node_degree(self):
        graph_util = utils.utils()
        print("starting graph")
        connection_matrix,uniq_users,user_dict = self.create_adjacency_matrix()
        print("done graph")
        degree,G = graph_util.create_graph(connection_matrix)
        print("getting degree")
        user_degree = {}
        for i in range(len(uniq_users)):
            print(i)
            user_name = uniq_users[i]
            user_id = user_dict[user_name]
            if user_id not in degree.keys():
                continue
            user_degree[user_name] = degree[user_id]
        print("Done everything")
        self.repo_obj.repo_remove()
        return user_degree
    