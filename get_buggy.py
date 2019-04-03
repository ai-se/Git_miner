# -*- coding: utf-8 -*-
"""
Created on Thu Aug 30 10:30:28 2018

@author: suvod
"""
from __future__ import division
import git_access,api_access,git2repo,buggy_commit
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
import os
import re
import networkx as nx
import platform

class git2data(object):
    
    def __init__(self,access_token,repo_owner,source_type,git_url,api_base_url,repo_name):
        self.repo_name = repo_name
        if platform.system() == 'Darwin' or platform.system() == 'Linux':
            self.data_path = os.getcwd() + '/data/'
        else:
            self.data_path = os.getcwd() + '\\data\\'
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
        #issue_df = pd.DataFrame(self.git_issues, columns = ['Issue_number','user_logon','author_type','Desc','title','lables'])
        commit_df = pd.DataFrame(self.git_commits, columns=['commit_number', 'message', 'parent','buggy'])
        #events_df = pd.DataFrame(self.git_issue_events, columns=['event_type', 'issue_number', 'commit_number'])
        # issue_commit_temp = []
        # commit_df['issues'] = pd.Series([None]*commit_df.shape[0])
        # issue_df['commits'] = pd.Series([None]*issue_df.shape[0])
        # #print("Phase one done")
        # for i in range(commit_df.shape[0]):
        #     _commit_number = commit_df.loc[i,'commit_number']
        #     _commit_message = commit_df.loc[i,'message']
        #     res = re.search("#[0-9]+$", _commit_message)
        #     if res is not None:
        #         _issue_id = res.group(0)[1:]
        #         issue_commit_temp.append([_commit_number,np.int64(_issue_id)])
        # issue_commit_list_1 = np.array(issue_commit_temp)
        # links = events_df.dropna()
        # links.reset_index(inplace=True)
        # issue_commit_temp = []
        # #print("Phase two done")
        # for i in range(links.shape[0]):
        #     if links.loc[i,'commit_number'] in issue_commit_list_1[:,0]:
        #         continue
        #     else:
        #         issue_commit_temp.append([links.loc[i,'commit_number'],links.loc[i,'issue_number']])
        # issue_commit_list_2 = np.array(issue_commit_temp)
        # issue_commit_list = np.append(issue_commit_list_1,issue_commit_list_2, axis = 0)
        # issue_commit_df = pd.DataFrame(issue_commit_list, columns = ['commit_id','issues']).drop_duplicates()
        # df_unique_issues = issue_commit_df.issues.unique()
        # #print("Phase three done")
        # for i in df_unique_issues:
        #     i = np.int64(i)
        #     commits = issue_commit_df[issue_commit_df['issues'] == i]['commit_id']
        #     x = issue_df['Issue_number'] == i
        #     j = x[x == True].index.values
        #     if len(j) != 1:
        #         continue
        #     issue_df.at[j[0],'commits'] = commits.values
        # df_unique_commits = issue_commit_df.commit_id.unique()
        # #print("Phase four done")
        # for i in df_unique_commits:
        #     issues = issue_commit_df[issue_commit_df['commit_id'] == i]['issues']
        #     x = commit_df['commit_number'] == i
        #     j = x[x == True].index.values
        #     if len(j) != 1:
        #         continue
        #     commit_df.at[j[0],'issues'] = issues.values
        # issue_comments_df = pd.DataFrame(self.git_issue_comments, columns = ['Issue_id','user_logon','commenter_type'])
        committed_files_df = pd.DataFrame(self.git_committed_files, columns = ['commit_id','file_id','file_mode','file_path'])
        # user_df = pd.DataFrame(self.user_map, columns = ['user_name','user_logon'])
        return commit_df,committed_files_df
    
    def create_data(self):
        #self.get_api_data()
        self.get_commit_data()
        self.get_committed_files()
        commit_data,committed_file_data = self.create_link()
        #print("Phase five done")
        #issue_data.to_pickle(self.data_path + self.repo_name + '_issue.pkl')
        #print("Phase six done")
        commit_data.to_pickle(self.data_path + self.repo_name + '_commit.pkl')
        committed_file_data.to_pickle(self.data_path + self.repo_name + '_committed_file.pkl')
        #print("Phase seven done")
        #issue_comment_data.to_pickle(self.data_path + self.repo_name + '_issue_comment.pkl')
        #print("Phase eight done")
        #user_data.to_pickle(self.data_path + self.repo_name + '_user.pkl')
        self.git_repo.repo_remove()
        print(self.repo_name,"Repo Done")