# -*- coding: utf-8 -*-
"""
Created on Thu Aug 30 10:30:28 2018

@author: suvod
"""
from __future__ import division
from main.api import git_access,api_access
from main.git_log import git2repo,buggy_commit
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
import os
import re
import networkx as nx
import platform
from os.path import dirname as up

class git2data(object):
    
    def __init__(self,access_token,repo_owner,source_type,git_url,api_base_url,repo_name):
        self.repo_name = repo_name
        if platform.system() == 'Darwin' or platform.system() == 'Linux':
            self.data_path = up(os.getcwd()) + '/data/'
        else:
            self.data_path = up(os.getcwd()) + '\\data\\'
        self.git_client = api_access.git_api_access(access_token,repo_owner,source_type,git_url,api_base_url,repo_name)
        self.git_repo = git2repo.git2repo(git_url,repo_name)
        self.repo = self.git_repo.clone_repo()
            
    def get_commit_data(self):
        #print("Inside get_commit_data in git2data")
        self.git_commits = self.git_repo.get_commits()
        
    def get_committed_files(self):
        #print("Inside get_commit_data in git2data")
        self.git_committed_files = self.git_repo.get_committed_files()
        return self.git_committed_files
    
        
    def create_link(self):
        commit_df = pd.DataFrame(self.git_commits, columns=['commit_number', 'message', 'parent','buggy'])
        committed_files_df = pd.DataFrame(self.git_committed_files, columns = ['commit_id','file_id','file_mode','file_path'])
        return commit_df,committed_files_df
    
    def create_data(self):
        self.get_commit_data()
        self.get_committed_files()
        commit_data,committed_file_data = self.create_link()
        commit_data.to_pickle(self.data_path + self.repo_name + '_commit.pkl')
        committed_file_data.to_pickle(self.data_path + self.repo_name + '_committed_file.pkl')
        self.git_repo.repo_remove()
        print(self.repo_name,"Repo Done")