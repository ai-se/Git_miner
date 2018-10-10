# -*- coding: utf-8 -*-
"""
Created on Mon Sep 10 16:54:11 2018

@author: suvod
"""

from __future__ import division
import git_access
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
import networkx as nx
import os
import utils
import platform

class create_social_inteaction_graph(object):
    
    def __init__(self,project_name):
        self.project_name = project_name
        self.read_data()
        
    def read_data(self):
        if platform.system() == 'Darwin':
            self.comments_details_df = pd.read_pickle(os.getcwd() + '/data/' + self.project_name+ '_issue_comment.pkl')
            self.issue_details_df = pd.read_pickle(os.getcwd() + '/data/' + self.project_name+ '_issue.pkl')
            self.user_map = pd.read_pickle(os.getcwd() + '/data/' + self.project_name+ '_user.pkl')
        else:
            self.comments_details_df = pd.read_pickle(os.getcwd() + '\\data\\' + self.project_name+ '_issue_comment.pkl')
            self.issue_details_df = pd.read_pickle(os.getcwd() + '\\data\\' + self.project_name+ '_issue.pkl')
            self.user_map = pd.read_pickle(os.getcwd() + '\\data\\' + self.project_name+ '_user.pkl')
        self.comments_details_df.drop(['commenter_type'], inplace=True, axis = 1)
        self.issue_details_df.drop(['author_type','Desc','title','commits'], inplace=True, axis = 1)
        self.comm_details_df = pd.concat([self.comments_details_df,self.issue_details_df])
        
    def create_adjacency_matrix(self):
        uniq_issues = self.comm_details_df.Issue_id.unique()
        uniq_users = self.comm_details_df.user_logon.unique()
        connection_matrix = np.ndarray(shape=(len(uniq_users),len(uniq_users)))
        connection_matrix = np.zeros((len(uniq_users),len(uniq_users)), dtype=np.int)
        self.user_dict = {}
        rev_user_dict = {}
        user_id = 0
        for i in range(len(uniq_users)):
            self.user_dict[uniq_users[i]] = user_id
            rev_user_dict[user_id] = uniq_users[i]
            user_id += 1
        for i in uniq_issues:
            issue_specific = self.comm_details_df[self.comm_details_df['Issue_id'] == i]
            participents = issue_specific.user_logon.unique()
            for j in range(len(participents)):
                comment_from = participents[j]
                comment_count = issue_specific[issue_specific['user_logon'] == comment_from].shape
                if len(participents) == 1:
                    continue
                comment_to = np.delete(participents,np.where(participents == comment_from))
                for k in comment_to:
                    connection_matrix[self.user_dict[comment_from]][self.user_dict[k]] += len(comment_count)
        return connection_matrix
                    
    
    def get_user_node_degree(self):
        graph_util = utils.utils()
        degree,G = graph_util.create_graph(self.create_adjacency_matrix())
        user_degree = {}
        user_mapping = self.user_map.values.tolist()
        for i in range(len(user_mapping)):
            logon  = user_mapping[i][1]
            user_name = user_mapping[i][0]
            user_id = self.user_dict[logon]
            if user_id not in degree.keys():
                continue
            user_degree[user_name] = degree[user_id]
        return user_degree
        