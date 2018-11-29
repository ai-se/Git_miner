""" @Author Jchakra"""
""" To fetch informations from all the projects we selected"""

from datetime import datetime
import requests,csv

fmt = '%Y-%m-%dT%H:%M:%SZ'

Token = 'XX'
api_url = 'https://api.github.com/'
headers = {'Content-Type': 'application/json','Authorization': 'Bearer {0}'.format(Token)}

fp1 = open('Project_Informations.csv', 'w' , newline='')
myFile1 = csv.writer(fp1)
column_names1 = ['id','name','html_url','owner','releases','languages','Duration(Hours)','Stars','Forks','Watchers','License']
myFile1.writerow(column_names1)

with open('combined_list.csv') as csvfile:
	readCSV = csv.reader(csvfile, delimiter=',')
	for csv_row in readCSV:		
		try:

			""" Fetching no of releases """
			no_of_releases = 0
			page = 1
			repo_url = api_url + 'repos/' + str(csv_row[3]) + '/' + str(csv_row[1]) + '/tags'
			repo_response = requests.get(repo_url, headers=headers).json()			
			if len(repo_response) == 30:
				flag = False
				while flag == False:					
					repo_url_next_page = repo_url + '?page=' + str(page)					
					repo_response_next_page = requests.get(repo_url_next_page, headers=headers).json()					
					if len(repo_response_next_page) == 0:
						flag = True
						break
					else:
						no_of_releases = no_of_releases + len(repo_response_next_page)
						page = page + 1

			else:
				no_of_releases = len(repo_response)

			""" Fetching languages """
			repo_url = api_url + 'repos/' + str(csv_row[3]) + '/' + str(csv_row[1]) + '/languages'
			language_description = requests.get(repo_url, headers=headers).json()

			""" Fetching Duration of Projects """
			repo_url = api_url + 'repos/' + str(csv_row[3]) + '/' + str(csv_row[1])			
			repo_response = requests.get(repo_url, headers=headers).json()
			tstamp1 = datetime.strptime(repo_response['pushed_at'], fmt)
			tstamp2 = datetime.strptime(repo_response['created_at'], fmt)
			td = tstamp1 - tstamp2
			duration_hours = int(round(td.total_seconds() / 3600))
			star_count = repo_response['stargazers_count']
			fork_count = repo_response['forks_count']
			watcher_count = repo_response['watchers_count'] ##This one is different for API and html
			license = repo_response['license']

			myFile1.writerow([str(csv_row[0]),str(csv_row[1]),str(csv_row[2]),str(csv_row[3]),no_of_releases,language_description,duration_hours,star_count,fork_count,watcher_count,license])					
		except:
			print("Exception occurred for -",repo_url)