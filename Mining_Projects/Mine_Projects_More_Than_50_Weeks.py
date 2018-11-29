""" @Author Jchakra"""
""" This code is to select only those projects whose duration > 50 weeks """


from datetime import datetime
from multiprocessing import Process,Lock
import csv,json,requests

fmt = '%Y-%m-%dT%H:%M:%SZ'
API_Token = '**'


def func1():

	api_url = 'https://api.github.com/repos'
	headers = {'Content-Type': 'application/json','Authorization': 'Bearer {0}'.format(API_Token)}	

	with open('1.csv') as csvfile:
		readCSV = csv.reader(csvfile, delimiter=',')
		for csv_row in readCSV:
			try:    
			    repo_url = api_url + '/' + str(csv_row[4]) + '/' + str(csv_row[1])
			    print(repo_url)	    
			    repo_response = requests.get(repo_url, headers=headers).json()	    
			    tstamp1 = datetime.strptime(repo_response['pushed_at'], fmt)
			    tstamp2 = datetime.strptime(repo_response['created_at'], fmt)
			    td = tstamp1 - tstamp2
			    td_mins = int(round(td.total_seconds() / 3600))
			    if td_mins > 8400:
			    	fp1 = open('11.csv', 'a' , newline='')
			    	myFile1 = csv.writer(fp1)
			    	myFile1.writerow(csv_row)
			    	fp1.close()
			except:
				print("Exception occurred for -",repo_url)

def func2():

	api_url = 'https://api.github.com/repos'
	headers = {'Content-Type': 'application/json','Authorization': 'Bearer {0}'.format(API_Token)}

	

	with open('2.csv') as csvfile:
		readCSV = csv.reader(csvfile, delimiter=',')
		for csv_row in readCSV:
			try:    
			    repo_url = api_url + '/' + str(csv_row[4]) + '/' + str(csv_row[1])
			    print(repo_url)	    
			    repo_response = requests.get(repo_url, headers=headers).json()	    
			    tstamp1 = datetime.strptime(repo_response['pushed_at'], fmt)
			    tstamp2 = datetime.strptime(repo_response['created_at'], fmt)
			    td = tstamp1 - tstamp2
			    td_mins = int(round(td.total_seconds() / 3600))
			    if td_mins > 8400:
			    	fp1 = open('22.csv', 'a' , newline='')
			    	myFile1 = csv.writer(fp1)
			    	myFile1.writerow(csv_row)
			    	fp1.close()
			except:
				print("Exception occurred for -",repo_url)

def func3():

	api_url = 'https://api.github.com/repos'
	headers = {'Content-Type': 'application/json','Authorization': 'Bearer {0}'.format(API_Token)}

	

	with open('3.csv') as csvfile:
		readCSV = csv.reader(csvfile, delimiter=',')
		for csv_row in readCSV:
			try:    
			    repo_url = api_url + '/' + str(csv_row[4]) + '/' + str(csv_row[1])
			    print(repo_url)	    
			    repo_response = requests.get(repo_url, headers=headers).json()	    
			    tstamp1 = datetime.strptime(repo_response['pushed_at'], fmt)
			    tstamp2 = datetime.strptime(repo_response['created_at'], fmt)
			    td = tstamp1 - tstamp2
			    td_mins = int(round(td.total_seconds() / 3600))
			    if td_mins > 8400:
			    	fp1 = open('33.csv', 'a' , newline='')
			    	myFile1 = csv.writer(fp1)
			    	myFile1.writerow(csv_row)
			    	fp1.close()
			except:
				print("Exception occurred for -",repo_url)


def func4():

	api_url = 'https://api.github.com/repos'
	headers = {'Content-Type': 'application/json','Authorization': 'Bearer {0}'.format(API_Token)}

	

	with open('4.csv') as csvfile:
		readCSV = csv.reader(csvfile, delimiter=',')
		for csv_row in readCSV:
			try:    
			    repo_url = api_url + '/' + str(csv_row[4]) + '/' + str(csv_row[1])
			    print(repo_url)	    
			    repo_response = requests.get(repo_url, headers=headers).json()	    
			    tstamp1 = datetime.strptime(repo_response['pushed_at'], fmt)
			    tstamp2 = datetime.strptime(repo_response['created_at'], fmt)
			    td = tstamp1 - tstamp2
			    td_mins = int(round(td.total_seconds() / 3600))
			    if td_mins > 8400:
			    	fp1 = open('44.csv', 'a' , newline='')
			    	myFile1 = csv.writer(fp1)
			    	myFile1.writerow(csv_row)
			    	fp1.close()
			except:
				print("Exception occurred for -",repo_url)
	    	


if __name__ == '__main__':
  lock = Lock()  
  p1 = Process(target=func1)
  p2 = Process(target=func2)
  p3 = Process(target=func3)
  p4 = Process(target=func4)  
  p1.start()
  p2.start()
  p3.start()
  p4.start()   
  p1.join()
  p2.join()
  p3.join()
  p4.join()
  




    
