""" @Author Jchakra"""
""" This code is to check whether a GitHub API token is valid or not """

import json,csv
import requests


project_list = []

Token =  '**' 
api_url = 'https://api.github.com/search/repositories?q=forks:>5000&order=desc'
headers = {'Content-Type': 'application/json','Authorization': 'Bearer {0}'.format(Token)}
repo_response = requests.get(api_url, headers=headers).json()
print(repo_response)

        
  
