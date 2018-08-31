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

class buggy_commit_maker(object):
    
    
    def __init__(self,project_name,repo_url,repo_name):
        self.project_name = project_name
        self.data_path = os.getcwd() + '\\data\\'
        self.commit = self.read_files('commit')
        self.committed_files = self.read_files('committed_file')
        self.initilize_repo(repo_url,repo_name)
        
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
        
    def get_buggy_commits(self):
        self.commit['isBuggy'] = pd.Series([0]*self.commit.shape[0])
        for i in range(self.commit.shape[0]):
            result = self.isBuggyCommit(self.commit.loc[i,'message'])
            if result:
                self.commit.loc[i,'isBuggy'] = 1
            else:
                self.commit.loc[i,'isBuggy'] = 0
                
    
    def get_buggy_committer(self):
        buggy_commit_df = self.commit[self.commit['isBuggy'] == 1]
        buggy_diffs = self.git_repo.get_diffs(buggy_commit_df['commit_number'].values.tolist())
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
                            bug_creator.append([ref.final_committer.name, ref.orig_commit_id, 1])
                except:
                    continue
        bug_creator_df = pd.DataFrame(bug_creator, columns = ['committer','commit','ob'])
        bug_creator_df = bug_creator_df.drop_duplicates()
        df = bug_creator_df.groupby( ['committer']).count()
        defect_count = []
        for key,value in df.iterrows():
            user = key
            count = value.values.tolist()[0]
            defect_count.append([user,count])
        return defect_count
    
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
        

    