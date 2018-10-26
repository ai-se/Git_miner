#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 16 11:50:15 2018

@author: suvodeepmajumder
"""
from __future__ import division
import git_access,api_access,git2repo
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
import networkx as nx
import re
import git2data
import social_interaction
import threading
from threading import Barrier
from multiprocessing import Queue

project_list = pd.read_csv('project_list.csv')
for i in range(project_list.shape[0]):
	try:
		access_token = project_list.loc[i,'access_token']
		repo_owner = project_list.loc[i,'repo_owner']
		source_type = project_list.loc[i,'source_type']
		git_url = project_list.loc[i,'git_url']
		api_base_url = project_list.loc[i,'api_base_url']
		repo_name = project_list.loc[i,'repo_name']
		git_data = git2data.git2data(access_token,repo_owner,source_type,git_url,api_base_url,repo_name)
		git_data.create_data()
	except Exception as e:
		print("Exception occured for ",project_list.loc[i,'git_url'])
		print(e)