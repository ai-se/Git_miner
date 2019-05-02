'''
Created on Feb 19, 2019

@author: peipei
'''
import pickle
from pprint import pprint
import json
import csv
from datetime import datetime
from itertools import chain
import glob
from github import Github
import re
import UniqueQueryResults

# keywords=["close","closes","closed","fix","fixes","fixed","resolve","resolves","resolved"]
r=re.compile("(?i)(close|close[sd]|fix|fixe[sd]|resolve|resolve[sd]):?\s*#?(\d+)")
ws="/home/peipei/GitHubIssues/"
def getLinkedIssueNum(msg):
    m=r.findall(msg)
    return [issue_id for key,issue_id in m] if len(m)>0 else None

def isPRLinked2Issue(github,pr_url):
    ## with GitHub REST API V3
    # pr_url https://github.com/PyGithub/PyGithub/pull/1090
    # return issue url: if not linked return empty list else return issue url string
#     if pr_url=='https://github.com/RADAR-base/ManagementPortal/pull/364':
#         print('hit')
    elements=pr_url.split("/")
#     print(elements)
    owner,repo_name,is_pr,id=tuple(elements[3:])
    if is_pr!="pull":
        raise ValueError("isLinked2Issue should pass in a PR URL")
    repo=github.get_repo(owner+"/"+repo_name)
    pr=repo.get_pull(int(id))
    
    candidates=[pr.title,pr.body]
    candidates.extend([cmt.commit.message for cmt in pr.get_commits()])
    candidates=[msg for msg in set(candidates) if msg is not None and msg!='']
    
    isLinked=chain(*[x for x in [getLinkedIssueNum(msg) for msg in candidates] if x is not None])
    return ["{}issues/{}".format(pr_url[:pr_url.index(is_pr)],x) for x in set(isLinked)]

def isPRLinked2Issue2(pr_url):
    ## with GitHub GraphQL API V4
    # pr_url https://github.com/PyGithub/PyGithub/pull/1090
    # return issue url: if not linked return empty list else return issue url string   

    elements=pr_url.split("/")
#     print(elements)
    owner,repo_name,is_pr,id=tuple(elements[3:])
    if is_pr!="pull":
        raise ValueError("isLinked2Issue should pass in a PR URL")
    
    isLinked=UniqueQueryResults.getMsgPerPRRepo(owner, repo_name, id, 10)
    return ["{}issues/{}".format(pr_url[:pr_url.index(is_pr)],x) for x in set(isLinked)]

      
if __name__ == '__main__':
    
    pass

