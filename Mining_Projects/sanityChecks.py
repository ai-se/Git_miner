""" @Author Jchakra"""
""" This code is to download project information using GitHub API (Following Amrit's Hero paper criteria of how to find good projects) """

import time
import json
import requests
import pandas as pd
from multiprocessing import Process,Lock
import os

def func1(file_path):
    api_url = 'https://api.github.com/'
    Token_list = ["b8964bafb3ec2e8d36eb826984091feedbd3d687"]
    repo_result = pd.read_csv(file_path)
    #repo_result.reset_index(drop=True, inplace=True)
    repo_result['issues > 8'] = ["YES"] * len(repo_result)
    repo_result['pull_req > 0'] = ["YES"] * len(repo_result)
    repo_result['commits > 20'] = ["YES"] * len(repo_result)
    repo_result['contributors > 8'] = ["YES"] * len(repo_result)
    repo_result['stars'] = [0] * len(repo_result)
    removed_projects = 0

    ## Removing projects having less than 8 issues
    p = 0

    while p < len(repo_result):
        repo_owner = repo_result.iloc[p]['repo_owner']
        repo_name = repo_result.iloc[p]['repo_name']
        issue_url = api_url + 'repos/' + repo_owner + '/' + repo_name + '/' + 'issues'

        exception_count = 0
        while exception_count < 2:
            try:
                for k in range(0, len(Token_list)):
                    headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer {0}'.format(Token_list[k])}
                    # print(Token_list[k])
                    issue_response = requests.get(issue_url, headers=headers).json()
                    try:
                        if (len(issue_response['message']) > 0):
                            if (k == len(Token_list) - 1):
                                time.sleep(600)
                                exception_count = exception_count + 1
                        else:
                            continue
                    except:
                        break
                if (exception_count == 0):
                    break
                else:
                    continue
            except:
                exception_count = 0
        #repo_result[p]["TL_issues"] = len(issue_response)
        if (len(issue_response) > 10):
        #    repo_result[p]["8_plus_issues"] = "YES"
            print("Funct 1 : Project is good")
        else:
            print("Funct 1 : Project is not good")
            #repo_result[p]["8_plus_issues"] = "NO"
            repo_result.at[p,"issues > 8"] = "NO"
            removed_projects+=1
        p+=1

    ## Selecting the projects with Pull Request > 0
    m = 0

    while m < len(repo_result):
        repo_owner = repo_result.iloc[m]['repo_owner']
        repo_name = repo_result.iloc[m]['repo_name']
        PR_url = api_url + 'repos/' + repo_owner + '/' + repo_name + '/' + 'pulls?state=all'

        exception_count = 0
        while exception_count < 2:
            try:
                for k in range(0, len(Token_list)):
                    headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer {0}'.format(Token_list[k])}
                    # print(Token_list[k])
                    PR_response = requests.get(PR_url, headers=headers).json()
                    try:
                        if (len(PR_response['message']) > 0):
                            if (k == len(Token_list) - 1):
                                time.sleep(600)
                                exception_count = exception_count + 1
                        else:
                            continue
                    except:
                        break
                if (exception_count == 0):
                    break
                else:
                    continue
            except:
                exception_count = 0

        if (len(PR_response) > 0):
            print("Funct 1 : Project is good")
        else:
            repo_result.at[m, "pull_req > 0"] = "NO"
            print("Func 1 : Project is not good")
        m+=1
    ## Selecting Projects with commits > 20
    n = 0
    while n < len(repo_result):
        repo_owner = repo_result.iloc[n]['repo_owner']
        repo_name = repo_result.iloc[n]['repo_name']
        commit_url = api_url + 'repos/' + repo_owner + '/' + repo_name + '/' + 'commits'

        exception_count = 0
        while exception_count < 2:
            try:
                for k in range(0, len(Token_list)):
                    headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer {0}'.format(Token_list[k])}
                    # print(Token_list[k])
                    commit_response = requests.get(commit_url, headers=headers).json()
                    try:
                        if (len(commit_response['message']) > 0):
                            if (k == len(Token_list) - 1):
                                time.sleep(600)
                                exception_count = exception_count + 1
                        else:
                            continue
                    except:
                        break
                if (exception_count == 0):
                    break
                else:
                    continue
            except:
                exception_count = 0
        if (len(commit_response) > 20):
            print("Funct 1 : Project is good")
        else:
            print("Funct 1 : Project is not good")
            repo_result.at[n, "commits > 20"] = "NO"
        n+=1

    ## Selecting Projects with contributors > 8
    c = 0
    while c < len(repo_result):
        repo_owner = repo_result.iloc[c]['repo_owner']
        repo_name = repo_result.iloc[c]['repo_name']
        commit_url = api_url + 'repos/' + repo_owner + '/' + repo_name + '/' + 'contributors'

        exception_count = 0
        while exception_count < 2:
            try:
                for k in range(0, len(Token_list)):
                    headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer {0}'.format(Token_list[k])}
                    # print(Token_list[k])
                    commit_response = requests.get(commit_url, headers=headers).json()
                    try:
                        if (len(commit_response['message']) > 0):
                            if (k == len(Token_list) - 1):
                                time.sleep(600)
                                exception_count = exception_count + 1
                        else:
                            continue
                    except:
                        break
                if (exception_count == 0):
                    break
                else:
                    continue
            except:
                exception_count = 0
        if (len(commit_response) > 8):
            print("Funct 1 : Project is good")
        else:
            print("Funct 1 : Project is not good")
            repo_result.at[c, "contributors > 8"] = "NO"
        c+=1
    ## Finding stars of a project
    s = 0
    while s < len(repo_result):
        repo_owner = repo_result.iloc[s]['repo_owner']
        repo_name = repo_result.iloc[s]['repo_name']
        commit_url = api_url + 'repos/' + repo_owner + '/' + repo_name
        headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer {0}'.format(Token_list[0])}
        commit_response = requests.get(commit_url, headers = headers).json()
        if 'stargazers_count' in commit_response:
            stars =  commit_response['stargazers_count']
            repo_result.at[s, "stars"] = stars
        s+=1
    #return  repo_result
    repo_result.to_csv("java_project_sanity_check.csv", mode = 'a+', index = False)

if __name__ == '__main__':
    if os.path.isfile("java_project_sanity_check.csv") :
        os.remove("java_project_sanity_check.csv")
    print("Process created")
    file_path = "project_list//projects_java.csv"
    func1(file_path)

