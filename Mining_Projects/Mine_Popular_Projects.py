""" @Author Jchakra"""
""" This code is to find out projects having greater than 5000 forks """

import json,csv
import requests


project_list = []

Token_list = ['**']  
api_url = 'https://api.github.com/search/repositories?q=forks:>5000&order=desc' ## This is the query to find projects with forks > 5000
fp1 = open('Popular_Projects.csv', 'w' , newline='')
myFile1 = csv.writer(fp1)
column_names = ['id','name','owner','html_url']
myFile1.writerow(column_names)
fp1.close()

for i in range(1,10):
  headers = {'Content-Type': 'application/json','Authorization': 'Bearer {0}'.format(Token_list[0])}
  repo_url = api_url + '&page=' + str(i)
  print(repo_url)
  repo_response = requests.get(repo_url, headers=headers).json()
  for j in range(len(repo_response['items'])):
        project_id = repo_response['items'][j]['id']
        project_name = repo_response['items'][j]['name']        
        project_html_url = repo_response['items'][j]['html_url']
        project_owner_name = repo_response['items'][j]['owner']['login']        
        fp1 = open('Top_Projects.csv', 'a' , newline='')
        myFile1 = csv.writer(fp1)
        myFile1.writerow([project_id,project_name,project_owner_name,project_html_url])
        fp1.close()
        
  
