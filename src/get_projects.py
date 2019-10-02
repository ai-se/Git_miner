#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 16 11:50:56 2018

@author: suvodeepmajumder
"""

from interaction import get_commit_lines
from interaction import code_interaction
import main.git_log.buggy_commit as buggy_commit
import pandas as pd
import numpy as np
import csv
from os.path import dirname as up
import os
from pathlib import Path
import platform
from main.git_log import git2data,git_commit_info


def get_heros():
    if platform.system() == 'Darwin' or platform.system() == 'Linux':
        source_projects = up(os.getcwd()) + '/project_list.csv'
    else:
        source_projects = up(os.getcwd()) + '\\project_list.csv'
    project_list = pd.read_csv(source_projects)
    project_list['heros_80'] = [0]*project_list.shape[0]
    project_list['heros_85'] = [0]*project_list.shape[0]
    project_list['heros_90'] = [0]*project_list.shape[0]
    project_list['heros_95'] = [0]*project_list.shape[0]
    project_list['num_dev'] = [0]*project_list.shape[0]
    projects_hero = []
    for i in range(project_list.shape[0]):
        try:
            access_token = project_list.loc[i,'access_token']
            repo_owner = project_list.loc[i,'repo_owner']
            source_type = project_list.loc[i,'source_type']
            git_url = project_list.loc[i,'git_url']
            api_base_url = project_list.loc[i,'api_base_url']
            repo_name = project_list.loc[i,'repo_name'] 
            git_data = git_commit_info.git2data(access_token,repo_owner,source_type,git_url,api_base_url,repo_name)
            git_data.create_data()
            if platform.system() == 'Darwin' or platform.system() == 'Linux':
                data_path = up(os.getcwd()) + '/data/' + repo_name + '/'
            else:
                data_path = up(os.getcwd()) + '\\data\\' + repo_name + '\\'
            
            if not Path(data_path).is_dir():
                os.makedirs(Path(data_path))
            
            cg = get_commit_lines.create_code_interaction_graph(git_url,repo_name)
            project_details = cg.get_user_node_degree()
            project_details.sort_values(by='ob',inplace=True)
            project_details['cum_sum'] = project_details.ob.cumsum()
            total_loc = project_details.ob.sum()
            #print(project_details,total_loc)
            contr_list = [0.8,0.85,0.9,0.95]
            population_list = [0.2,0.15,0.1,0.05]
            for k in range(4):
                for j in range(project_details.shape[0]):
                    if project_details.iloc[j,1] <= project_details.ob.sum()*contr_list[k]:
                        continue
                    else:
                        break
                project_list.iloc[i,11] = project_details.shape[0]

                if project_details.shape[0] < 8:
                    continue
                if 1 == j/project_details.shape[0]:
                    project_list.iloc[i,7+k] = False
                    continue
                if ((1 - j/project_details.shape[0])<population_list[k]):
                    project_list.iloc[i,7+k] = True 
                else:
                    project_list.iloc[i,7+k] = False

            project_list.to_csv(up(os.getcwd()) + '/hero_list.csv')
        except Exception as e:
            print("Error",e)
            continue
    return project_list

get_heros()