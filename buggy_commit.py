# -*- coding: utf-8 -*-
"""
Created on Fri Aug 31 12:49:38 2018

@author: suvod
"""

import git2repo,api_access
import pygit2
import re
import pandas as pd
from datetime import datetime
import re, unicodedata
from pygit2 import GIT_SORT_TOPOLOGICAL, GIT_SORT_REVERSE
import os
from utils import utils
import platform
import threading
from multiprocessing import Queue
from threading import Thread
import numpy as np
import itertools
import pandas as pd
import itertools
import math
from multiprocessing import Pool, cpu_count


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

class buggy_commit_maker(object):
    
    
    def __init__(self,project_name,repo_url,repo_name):
        self.project_name = project_name
        if platform.system() == 'Darwin' or platform.system() == 'Linux':
            self.data_path = os.getcwd() + '/data/'
        else:
            self.data_path = os.getcwd() + '\\data\\'
        self.commit = self.read_files('commit')
        self.committed_files = self.read_files('committed_file')
        self.initilize_repo(repo_url,repo_name)
        self.cores = cpu_count()
        
    def initilize_repo(self,repo_url,repo_name):
        self.git_repo = git2repo.git2repo(repo_url,repo_name)
        self.repo = self.git_repo.clone_repo()
        
       
    def read_files(self,file_data):
        file_path = self.data_path + self.project_name + '_' + file_data + '.pkl'
        return pd.read_pickle(file_path)
    
    
    def isBuggyCommit(self, commit):
        res=re.search(r'\b{bug|defect|fix|patch|#}\b',utils().stemming(commit),re.IGNORECASE)
        if res is not None:
            return True
    
    def buggy_commits(self,commits):
        for i in range(commits.shape[0]):
            result = self.isBuggyCommit(commits.loc[i,'message'])
            if result:
                commits.loc[i,'isBuggy'] = 1
            else:
                commits.loc[i,'isBuggy'] = 0
        return commits

    def get_buggy_commits(self):
        threads = []
        self.commit['isBuggy'] = pd.Series([0]*self.commit.shape[0])
        column_names = self.commit.columns.tolist()
        bug_fixed_commit = pd.DataFrame([], columns = column_names)
        commits_np = np.array_split(self.commit, self.cores)
        for i in range(self.cores):
            commits = pd.DataFrame(commits_np[i], columns = column_names)
            commits.reset_index(inplace = True, drop = True)
            t = ThreadWithReturnValue(target = self.buggy_commits, args = [commits])
            threads.append(t)
        for th in threads:
            th.start()
        for th in threads:
            response = th.join()
            bug_fixed_commit = pd.concat([bug_fixed_commit,response])
            bug_fixed_commit.reset_index(inplace = True, drop = True)
        self.commit = bug_fixed_commit
    
#    def get_buggy_commits(self):
#        self.commit['isBuggy'] = pd.Series([0]*self.commit.shape[0])
#        for i in range(self.commit.shape[0]):
#            result = self.isBuggyCommit(self.commit.loc[i,'message'])
#            if result:
#                self.commit.loc[i,'isBuggy'] = 1
#            else:
#                self.commit.loc[i,'isBuggy'] = 0
   

    def buggy_committer(self,buggy_diffs):
        bug_creator = []
        for value in buggy_diffs:
            _diff_files = buggy_diffs[value]['files']
            self.repo.head.set_target(buggy_diffs[value]['object'].parent_ids[0])
            for _value in _diff_files:
                try:
                    file_path = _diff_files[_value]['file_path']
                    blame = self.git_repo.get_blame(file_path)
                    for _line in _diff_files[_value]['old_lines']:
                        if _line != -1:
                            ref = blame.for_line(_line)
                            #print(_value,ref.final_committer.name)
                            bug_creator.append([ref.final_committer.name, ref.orig_commit_id, 1])
                except:
                    continue
        bug_creator_df = pd.DataFrame(bug_creator, columns = ['committer','commit','ob'])
        bug_creator_df = bug_creator_df.drop_duplicates()
        return bug_creator_df
    
    
    def get_buggy_committer(self):
        threads = []
        df = pd.DataFrame([])
        # To-Do this is to saperate the data into small chunks from get_diff that is the dict
        buggy_commit_df = self.commit[self.commit['isBuggy'] == 1]
        buggy_diffs = self.git_repo.get_diffs(buggy_commit_df['commit_number'].values.tolist())
        keys = list(buggy_diffs.keys())
        len_bd = len(buggy_diffs)
        sub_list_len = len_bd/self.cores
        for i in range(self.cores):
            sub_keys = keys[int(i*sub_list_len):int((i+1)*sub_list_len)]
            subdict = {x: buggy_diffs[x] for x in sub_keys if x in buggy_diffs}
            t = ThreadWithReturnValue(target = self.buggy_committer, args = [subdict])
            threads.append(t)
        for i in range(0,len(threads),self.cores):
            _threads = threads[i:i+self.cores]
            for th in _threads:
                th.start()
            for th in _threads:
                response = th.join()
                df = pd.concat([df,response])
                df.reset_index(inplace = True, drop = True)
        df.drop_duplicates(inplace = True)
        df = df.groupby( ['committer']).count()
        defect_count = []
        for key,value in df.iterrows():
            user = key
            count = value.values.tolist()[0]
            defect_count.append([user,count])
        return defect_count
    
#    def get_buggy_committer(self):
#        buggy_commit_df = self.commit[self.commit['isBuggy'] == 1]
#        buggy_diffs = self.git_repo.get_diffs(buggy_commit_df['commit_number'].values.tolist())
#        bug_creator = []
#        for value in buggy_diffs:
#            _diff_files = buggy_diffs[value]['files']
#            self.repo.head.set_target(buggy_diffs[value]['object'].parent_ids[0])
#            for _value in _diff_files:
#                try:
#                    file_path = _diff_files[_value]['file_path']
#                    blame = self.git_repo.get_blame(file_path)
#                    for _line in _diff_files[_value]['old_lines']:
#                        if _line != -1:
#                            ref = blame.for_line(_line)
#                            print(_value,ref.final_committer.name)
#                            bug_creator.append([ref.final_committer.name, ref.orig_commit_id, 1])
#                except:
#                    continue
#        bug_creator_df = pd.DataFrame(bug_creator, columns = ['committer','commit','ob'])
#        bug_creator_df = bug_creator_df.drop_duplicates()
#        df = bug_creator_df.groupby( ['committer']).count()
#        defect_count = []
#        for key,value in df.iterrows():
#            user = key
#            count = value.values.tolist()[0]
#            defect_count.append([user,count])
#        return defect_count
    
    def get_commit_count(self):
        committer_count = []
        for i in range(self.commit.shape[0]):
            commit_id = self.commit.loc[i,'commit_number']
            user = self.repo.get(commit_id).committer
            committer_count.append([user.name, commit_id, 1])
        committer_count_df = pd.DataFrame(committer_count, columns = ['committer', 'commit_id', 'ob'])
        committer_count_df = committer_count_df.drop_duplicates()
        df = committer_count_df.groupby( ['committer']).count()
        commit_count = []
        for key,value in df.iterrows():
            user = key
            count = value.values.tolist()[0]
            commit_count.append([user,count])
        return commit_count
        

    