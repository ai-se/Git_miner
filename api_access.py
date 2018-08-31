# -*- coding: utf-8 -*-
"""
Created on Wed Aug 29 11:36:45 2018

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

class git_api_access(object):
    
    def __init__(self,token,repo_owner,source_type,git_url,api_base_url,repo_name):
        self.access_token = token
        self.repo_owner = repo_owner
        self.source_type = source_type
        self.git_url = git_url
        self.api_base_url = api_base_url
        self.repo_name = repo_name
        self.client = self.get_git_client()
        self.get_git_client()
        
    def get_git_client(self):
        self.client = git_access.GitHubClient({'access_token': self.access_token,
                       'repo_owner': self.repo_owner, 
                       'source_type': self.source_type, 
                       'git_url': self.git_url, 
                       'api_base_url': self.api_base_url, 
                       'repo_name': self.repo_name})
    
    def create_base_url(self, url_type):
        self.url_type = url_type
        self.base_url = self.api_base_url + '/repos/' + self.repo_owner + '/' + self.repo_name + '/' +  self.url_type
        
    def create_advanced_url(self, url_details = ''):
        if url_details != '':
            self.advanced_url = self.base_url + '/' + url_details
        else:
            self.advanced_url = self.base_url
            
    
    def get_comments(self,url_type,url_details = ''):
        self.create_base_url(url_type)
        self.create_advanced_url(url_details)
        x = [0]*100
        page_number = 1
        comments_details = []
        while len(x) >= 100:
            paged_url = self.advanced_url + '?page=' + str(page_number) + '&per_page=100'
            page_number += 1
            res = self.client.get(paged_url)
            x = json.loads(res.content)
            for i in range(len(x)):
                issue_number = x[i]['issue_url'][len(self.base_url)+2:]
                user_logon = x[i]['user']['login']
                author_association = x[i]['author_association']
                comments_details.append([issue_number,user_logon,author_association])
        return comments_details
    
    
    def get_issues(self,url_type,url_details = ''):
        self.create_base_url(url_type)
        self.create_advanced_url(url_details)
        x = [0]*100
        page_number = 1
        issue_details = []
        while len(x) >= 100:
            paged_url = self.advanced_url + '?state=' + 'all' + '&page=' + str(page_number) + '&per_page=100'
            page_number += 1
            res = self.client.get(paged_url)
            x = json.loads(res.content)
            for i in range(len(x)):
                issue_number = x[i]['number']
                user_logon = x[i]['user']['login']
                author_type = x[i]['user']['type']
                desc =  x[i]['body']
                title = x[i]['title']
                issue_details.append([issue_number,user_logon,author_type,desc,title])
        return issue_details
    
    
    def get_events(self,url_type,url_details = ''):
        self.create_base_url(url_type)
        self.create_advanced_url(url_details)
        x = [0]*100
        page_number = 1
        event_details = []
        while len(x) >= 100:
            paged_url = self.advanced_url + '?page=' + str(page_number) + '&per_page=100'
            page_number += 1
            res = self.client.get(paged_url)
            x = json.loads(res.content)
            for i in range(len(x)):
                event_type = x[i]['event']
                issue_number = x[i]['issue']['number']
                commit_number = x[i]['commit_id']
                event_details.append([event_type,issue_number,commit_number])
        return event_details
    