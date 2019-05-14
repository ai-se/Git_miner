#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  6 12:04:19 2019

@author: suvodeepmajumder
"""

from main.git_understand import git_understand
import os
import re
import shlex
import numpy as np
import pandas as pd
from glob2 import glob, iglob
import subprocess as sp
import understand as und
from pathlib import Path
from pdb import set_trace
from collections import defaultdict
from main.utils.utils import utils
from os.path import dirname as up
import os
import platform

if platform.system() == 'Darwin' or platform.system() == 'Linux':
    data_path = up(os.getcwd()) + '/project_list.csv'
    print(up(os.getcwd()))
else:
    data_path = up(os.getcwd()) + '\\project_list.csv'

project_list = pd.read_csv(data_path)

for i in range(project_list.shape[0]):
    try:
        repo_url = project_list.loc[i,'git_url']
        repo_name = project_list.loc[i,'repo_name'] 
        repo_lang = project_list.loc[i,'lang'] 
        get_matrix = git_understand.MetricsGetter(repo_url,repo_name,repo_lang)
        commits = get_matrix.read_commits()
        matrix = get_matrix.get_all_metrics()
        print(matrix)
    except ValueError:
        print("Error")