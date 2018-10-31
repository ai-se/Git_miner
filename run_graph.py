#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 16 11:50:56 2018

@author: suvodeepmajumder
"""

import social_interaction
import code_interaction
import buggy_commit
import pandas as pd
import numpy as np
import csv


project_list = pd.read_csv('project_list.csv')
fp1 = open('run_graph.csv', 'w' , newline='')
myFile1 = csv.writer(fp1)
column_names1 = ['project_name','first','second','third','fourth']
myFile1.writerow(column_names1)
fp1.close()

for i in range(project_list.shape[0]):
    try:
        access_token = project_list.loc[i,'access_token']
        repo_owner = project_list.loc[i,'repo_owner']
        source_type = project_list.loc[i,'source_type']
        git_url = project_list.loc[i,'git_url']
        api_base_url = project_list.loc[i,'api_base_url']
        repo_name = project_list.loc[i,'repo_name'] 
        
        
        sg = social_interaction.create_social_inteaction_graph(repo_name)
        cg = code_interaction.create_code_interaction_graph(git_url,repo_name)
        
        bugs_data = buggy_commit.buggy_commit_maker(repo_name,git_url,repo_name)
        bugs_data.get_buggy_commits()
        buggy_commit_data = bugs_data.get_buggy_committer()
        
        sg_data = sg.get_user_node_degree()
        cg_data = cg.get_user_node_degree()
        
        commit_data = bugs_data.get_commit_count()
        
        sg_data_list = []
        for key, value in sg_data.items():
            temp = [key,value]
            sg_data_list.append(temp)
        cg_data_list = []
        for key, value in cg_data.items():
            temp = [key,value]
            cg_data_list.append(temp)
            
        buggy_commit_data_df = pd.DataFrame(buggy_commit_data, columns = ['committer', 'count'])
        commit_data_df = pd.DataFrame(commit_data, columns = ['committer', 'count'])
        sg_data_df = pd.DataFrame(sg_data_list, columns = ['committer', 'count'])
        cg_data_df = pd.DataFrame(cg_data_list, columns = ['committer', 'count'])
        
        committer_count = []
        for i in range(bugs_data.commit.shape[0]):
            commit_id = bugs_data.commit.loc[i,'commit_number']
            user = bugs_data.repo.get(commit_id).committer
            committer_count.append([user.name, commit_id, 1])
        committer_count_df = pd.DataFrame(committer_count, columns = ['committer', 'commit_id', 'ob'])
        committer_count_df = committer_count_df.drop_duplicates()
        df = committer_count_df.groupby( ['committer']).count()
        commit_count = []
        for key,value in df.iterrows():
            user = key
            count = value.values.tolist()[0]
            commit_count.append([user,count])
        
        print("step1")
        results = [[buggy_commit_data_df,commit_data_df,commit_count,sg_data_df,cg_data_df]]
        result_pd = pd.DataFrame(results,columns = ['buggy_commit_data_df','commit_data_df',
                                                    'commit_count','sg_data_df','cg_data_df'])
        print("step2")
        result_pd.to_pickle('Processed_data/' + repo_name + '_final_results.pkl')
        print("step3")   
        df = []
        for i in range(cg_data_df.shape[0]):
            buggy_commit_count = buggy_commit_data_df[buggy_commit_data_df['committer'] == cg_data_df.loc[i,'committer']]['count']
            if len(buggy_commit_count) == 0:
                continue
            commit_count = commit_data_df[commit_data_df['committer'] == cg_data_df.loc[i,'committer']]['count']
            if len(commit_count) == 0:
                continue
            node_degree = cg_data_df[cg_data_df['committer'] == cg_data_df.loc[i,'committer']]['count']
            df.append([buggy_commit_count.values[0]/commit_count.values[0],node_degree.values[0]])
            
        df = pd.DataFrame(df, columns = ['per','degree'])
        
        
        degree_d = np.array(df['degree'].values.tolist())
        
        first = np.int32(np.percentile(degree_d,99.9))
        second = np.int32(np.percentile(degree_d,99))
        third = np.int32(np.percentile(degree_d,80))
        forth = np.int32(np.percentile(degree_d,50))
        
        first_l = []
        second_l = []
        third_l = []
        forth_l = []
        for i in range(df.shape[0]):
            if df.loc[i,'degree'] < forth:
                forth_l.append(df.loc[i,'per'])
            elif df.loc[i,'degree'] < third:
                third_l.append(df.loc[i,'per'])
            elif df.loc[i,'degree'] < second:
                second_l.append(df.loc[i,'per'])
            else:
                first_l.append(df.loc[i,'per'])
        print(round(np.median(first_l),2),round(np.median(second_l),2),round(np.median(third_l),2),round(np.median(forth_l),2))
        fp1 = open('run_graph.csv', 'a' , newline='')
        myFile1 = csv.writer(fp1)        
        print_list = [repo_name,round(np.median(first_l),2),round(np.median(second_l),2),round(np.median(third_l),2),round(np.median(forth_l),2)]
        myFile1.writerow(print_list)
        fp1.close()

    except Exception as e:
        print("Exception occured for ",git_url)
        print(e)

fp1.close()