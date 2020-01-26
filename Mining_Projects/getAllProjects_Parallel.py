""" @Author Jchakra"""
""" This code is to download project information using GitHub API (Following Amrit's Hero paper criteria of how to find good projects) """
 
from multiprocessing import Process,Lock
import time
import json
import requests
  
## Downloading all the projects


def func1():

  repo_result = []
  print("Inside function 1")
  Token_list = ["b8964bafb3ec2e8d36eb826984091feedbd3d687"]
  #Token_list = [''**'',''**'',''**'',''**'',''**'']

  i = 0  
  api_url = 'https://api.github.com/'

  while i < 10000: # This number will be increased to collect all the projects

    repo_url = api_url + 'repositories?since=' + str(i)  
    exception_count = 0  
    while exception_count < 2:
      try:
        for k in range(0,len(Token_list)):        
          headers = {'Content-Type': 'application/json','Authorization': 'Bearer {0}'.format(Token_list[k])}
          #print(Token_list[k])                 
          repo_response = requests.get(repo_url, headers=headers).json()
          #print(repo_response)                         
          try:            
            if ( len(repo_response['message']) > 0):              
              if( k == len(Token_list) - 1):
                time.sleep(600)
                exception_count = exception_count + 1
            else:
              continue
          except:            
            break
        if ( exception_count == 0):          
          break
        else:
          continue
      except:        
        exception_count = 0


    project_list = []

    try:      
      for j in range(0,len(repo_response)):
        project_id = repo_response[j]['id']
        project_name = repo_response[j]['name']
        project_full_name = repo_response[j]['full_name']
        project_html_url = repo_response[j]['html_url']
        project_owner_name = repo_response[j]['owner']['login']
        project_obj = {"id" : project_id, "name": project_name, "full_name" : project_full_name, "html_url" : project_html_url, "owner" : project_owner_name , "issues" :
        "", "commits" : "", "PR" : ""}
        project_list.append(project_obj)     


    except:
      print ("exception occurred")
    

    try:    
      last_id = repo_response[99]["id"]   
      i = last_id      
      repo_result = repo_result + project_list
          
    except:
      print(" exception inside function 1 ")
      break

    ## Removing projects having less than 8 issues

  p = 0
  while p < len(repo_result):    
    repo_owner = repo_result[p]['owner']
    repo_name = repo_result[p]['name']
    issue_url = api_url + 'repos/' + repo_owner + '/' + repo_name + '/' + 'issues'
    
    exception_count = 0  
    while exception_count < 2:
      try:
        for k in range(0,len(Token_list)):        
          headers = {'Content-Type': 'application/json','Authorization': 'Bearer {0}'.format(Token_list[k])}
          #print(Token_list[k])       
          issue_response = requests.get(issue_url, headers=headers).json()        
          try:
            if ( len(issue_response['message']) > 0):
              if( k == len(Token_list) - 1):
                time.sleep(600)
                exception_count = exception_count + 1
            else:
              continue
          except:
            break
        if ( exception_count == 0):
          break
        else:
          continue
      except:
        exception_count = 0



    if(len(issue_response) > 10):
      repo_result[p]["issues"] = len(issue_response)
      p = p + 1
    else:
      repo_result.pop(p)

    ## Selecting the projects with Pull Request > 0

  m = 0

  while m < len(repo_result):
    repo_owner = repo_result[m]['owner']
    repo_name = repo_result[m]['name']
    PR_url = api_url + 'repos/' + repo_owner + '/' + repo_name + '/' + 'pulls?state=all'


    exception_count = 0  
    while exception_count < 2:
      try:
        for k in range(0,len(Token_list)):        
          headers = {'Content-Type': 'application/json','Authorization': 'Bearer {0}'.format(Token_list[k])}
          #print(Token_list[k])       
          PR_response = requests.get(PR_url, headers=headers).json()        
          try:
            if ( len(PR_response['message']) > 0):
              if( k == len(Token_list) - 1):
                time.sleep(600)
                exception_count = exception_count + 1
            else:
              continue
          except:
            break
        if ( exception_count == 0):
          break
        else:
          continue
      except:
        exception_count = 0


    

    if(len(PR_response) > 0):
      repo_result[m]["PR"] = len(PR_response)      
      m = m + 1
    else:      
      repo_result.pop(m)

  ## Selecting Projects with commits > 20
  n = 0  
  while n < len(repo_result):
    repo_owner = repo_result[n]['owner']
    repo_name = repo_result[n]['name']
    commit_url = api_url + 'repos/' + repo_owner + '/' + repo_name + '/' + 'commits'


    exception_count = 0  
    while exception_count < 2:
      try:
        for k in range(0,len(Token_list)):        
          headers = {'Content-Type': 'application/json','Authorization': 'Bearer {0}'.format(Token_list[k])}
          #print(Token_list[k])       
          commit_response = requests.get(commit_url, headers=headers).json()                  
          try:
            if ( len(commit_response['message']) > 0):
              if( k == len(Token_list) - 1):
                time.sleep(600)
                exception_count = exception_count + 1
            else:
              continue
          except:
            break
        if ( exception_count == 0):
          break
        else:
          continue
      except:
        exception_count = 0



    if(len(commit_response) > 20):
      repo_result[n]["commits"] = len(commit_response)      
      n = n + 1
    else:      
      repo_result.pop(n)


  with open("repo_file1.json", "w") as repo_file:
    json.dump(repo_result, repo_file)
    print("function 1 finished", len(repo_result))


def func2():

  repo_result = []

  Token_list = ["b8964bafb3ec2e8d36eb826984091feedbd3d687"]
  #Token_list = [''**'',''**'',''**'',''**'',''**'']

  i = 10000  
  api_url = 'https://api.github.com/'

  while i < 20000: # This number will be increased to collect all the projects

    repo_url = api_url + 'repositories?since=' + str(i)  
    exception_count = 0  
    while exception_count < 2:
      try:
        for k in range(0,len(Token_list)):        
          headers = {'Content-Type': 'application/json','Authorization': 'Bearer {0}'.format(Token_list[k])}
          #print(Token_list[k])                 
          repo_response = requests.get(repo_url, headers=headers).json()
          #print(repo_response)                         
          try:            
            if ( len(repo_response['message']) > 0):              
              if( k == len(Token_list) - 1):
                time.sleep(600)
                exception_count = exception_count + 1
            else:
              continue
          except:            
            break
        if ( exception_count == 0):          
          break
        else:
          continue
      except:        
        exception_count = 0


    project_list = []

    try:      
      for j in range(0,len(repo_response)):
        project_id = repo_response[j]['id']
        project_name = repo_response[j]['name']
        project_full_name = repo_response[j]['full_name']
        project_html_url = repo_response[j]['html_url']
        project_owner_name = repo_response[j]['owner']['login']
        project_obj = {"id" : project_id, "name": project_name, "full_name" : project_full_name, "html_url" : project_html_url, "owner" : project_owner_name , "issues" :
        "", "commits" : "", "PR" : ""}
        project_list.append(project_obj)     


    except:
      print ("exception occurred")
    

    try:    
      last_id = repo_response[99]["id"]   
      i = last_id      
      repo_result = repo_result + project_list
          
    except:
      print(" exception inside function 2 ")
      break

    ## Removing projects having less than 8 issues
  
  p = 0
  while p < len(repo_result):    
    repo_owner = repo_result[p]['owner']
    repo_name = repo_result[p]['name']
    issue_url = api_url + 'repos/' + repo_owner + '/' + repo_name + '/' + 'issues'
    
    exception_count = 0  
    while exception_count < 2:
      try:
        for k in range(0,len(Token_list)):        
          headers = {'Content-Type': 'application/json','Authorization': 'Bearer {0}'.format(Token_list[k])}
          #print(Token_list[k])       
          issue_response = requests.get(issue_url, headers=headers).json()        
          try:
            if ( len(issue_response['message']) > 0):
              if( k == len(Token_list) - 1):
                time.sleep(600)
                exception_count = exception_count + 1
            else:
              continue
          except:
            break
        if ( exception_count == 0):
          break
        else:
          continue
      except:
        exception_count = 0



    if(len(issue_response) > 10):
      repo_result[p]["issues"] = len(issue_response)
      p = p + 1
    else:
      repo_result.pop(p)

    ## Selecting the projects with Pull Request > 0

  m = 0

  while m < len(repo_result):
    repo_owner = repo_result[m]['owner']
    repo_name = repo_result[m]['name']
    PR_url = api_url + 'repos/' + repo_owner + '/' + repo_name + '/' + 'pulls?state=all'


    exception_count = 0  
    while exception_count < 2:
      try:
        for k in range(0,len(Token_list)):        
          headers = {'Content-Type': 'application/json','Authorization': 'Bearer {0}'.format(Token_list[k])}
          #print(Token_list[k])       
          PR_response = requests.get(PR_url, headers=headers).json()        
          try:
            if ( len(PR_response['message']) > 0):
              if( k == len(Token_list) - 1):
                time.sleep(600)
                exception_count = exception_count + 1
            else:
              continue
          except:
            break
        if ( exception_count == 0):
          break
        else:
          continue
      except:
        exception_count = 0


    

    if(len(PR_response) > 0):
      repo_result[m]["PR"] = len(PR_response)      
      m = m + 1
    else:      
      repo_result.pop(m)

  ## Selecting Projects with commits > 20
  n = 0  
  while n < len(repo_result):
    repo_owner = repo_result[n]['owner']
    repo_name = repo_result[n]['name']
    commit_url = api_url + 'repos/' + repo_owner + '/' + repo_name + '/' + 'commits'


    exception_count = 0  
    while exception_count < 2:
      try:
        for k in range(0,len(Token_list)):        
          headers = {'Content-Type': 'application/json','Authorization': 'Bearer {0}'.format(Token_list[k])}
          #print(Token_list[k])       
          commit_response = requests.get(commit_url, headers=headers).json()                  
          try:
            if ( len(commit_response['message']) > 0):
              if( k == len(Token_list) - 1):
                time.sleep(600)
                exception_count = exception_count + 1
            else:
              continue
          except:
            break
        if ( exception_count == 0):
          break
        else:
          continue
      except:
        exception_count = 0



    if(len(commit_response) > 20):
      repo_result[n]["commits"] = len(commit_response)      
      n = n + 1
    else:      
      repo_result.pop(n)


  with open("repo_file2.json", "w") as repo_file:
    json.dump(repo_result, repo_file)
    print("function 2 finished", len(repo_result))

def func3():

  repo_result = []

  Token_list = ["b8964bafb3ec2e8d36eb826984091feedbd3d687"]
  #Token_list = [''**'',''**'',''**'',''**'',''**'']

  i = 20000  
  api_url = 'https://api.github.com/'

  while i < 30000: # This number will be increased to collect all the projects

    repo_url = api_url + 'repositories?since=' + str(i)  
    exception_count = 0  
    while exception_count < 2:
      try:
        for k in range(0,len(Token_list)):        
          headers = {'Content-Type': 'application/json','Authorization': 'Bearer {0}'.format(Token_list[k])}
          #print(Token_list[k])                 
          repo_response = requests.get(repo_url, headers=headers).json()
          #print(repo_response)                         
          try:            
            if ( len(repo_response['message']) > 0):              
              if( k == len(Token_list) - 1):
                time.sleep(600)
                exception_count = exception_count + 1
            else:
              continue
          except:            
            break
        if ( exception_count == 0):          
          break
        else:
          continue
      except:        
        exception_count = 0


    project_list = []

    try:      
      for j in range(0,len(repo_response)):
        project_id = repo_response[j]['id']
        project_name = repo_response[j]['name']
        project_full_name = repo_response[j]['full_name']
        project_html_url = repo_response[j]['html_url']
        project_owner_name = repo_response[j]['owner']['login']
        project_obj = {"id" : project_id, "name": project_name, "full_name" : project_full_name, "html_url" : project_html_url, "owner" : project_owner_name , "issues" :
        "", "commits" : "", "PR" : ""}
        project_list.append(project_obj)     


    except:
      print ("exception occurred")
    

    try:    
      last_id = repo_response[99]["id"]   
      i = last_id      
      repo_result = repo_result + project_list
          
    except:
      print(" exception inside function 3 ")
      break

    ## Removing projects having less than 8 issues
  
  p = 0
  while p < len(repo_result):    
    repo_owner = repo_result[p]['owner']
    repo_name = repo_result[p]['name']
    issue_url = api_url + 'repos/' + repo_owner + '/' + repo_name + '/' + 'issues'
    
    exception_count = 0  
    while exception_count < 2:
      try:
        for k in range(0,len(Token_list)):        
          headers = {'Content-Type': 'application/json','Authorization': 'Bearer {0}'.format(Token_list[k])}
          #print(Token_list[k])       
          issue_response = requests.get(issue_url, headers=headers).json()        
          try:
            if ( len(issue_response['message']) > 0):
              if( k == len(Token_list) - 1):
                time.sleep(600)
                exception_count = exception_count + 1
            else:
              continue
          except:
            break
        if ( exception_count == 0):
          break
        else:
          continue
      except:
        exception_count = 0



    if(len(issue_response) > 10):
      repo_result[p]["issues"] = len(issue_response)
      p = p + 1
    else:
      repo_result.pop(p)

    ## Selecting the projects with Pull Request > 0

  m = 0

  while m < len(repo_result):
    repo_owner = repo_result[m]['owner']
    repo_name = repo_result[m]['name']
    PR_url = api_url + 'repos/' + repo_owner + '/' + repo_name + '/' + 'pulls?state=all'


    exception_count = 0  
    while exception_count < 2:
      try:
        for k in range(0,len(Token_list)):        
          headers = {'Content-Type': 'application/json','Authorization': 'Bearer {0}'.format(Token_list[k])}
          #print(Token_list[k])       
          PR_response = requests.get(PR_url, headers=headers).json()        
          try:
            if ( len(PR_response['message']) > 0):
              if( k == len(Token_list) - 1):
                time.sleep(600)
                exception_count = exception_count + 1
            else:
              continue
          except:
            break
        if ( exception_count == 0):
          break
        else:
          continue
      except:
        exception_count = 0


    

    if(len(PR_response) > 0):
      repo_result[m]["PR"] = len(PR_response)      
      m = m + 1
    else:      
      repo_result.pop(m)

  ## Selecting Projects with commits > 20
  n = 0  
  while n < len(repo_result):
    repo_owner = repo_result[n]['owner']
    repo_name = repo_result[n]['name']
    commit_url = api_url + 'repos/' + repo_owner + '/' + repo_name + '/' + 'commits'


    exception_count = 0  
    while exception_count < 2:
      try:
        for k in range(0,len(Token_list)):        
          headers = {'Content-Type': 'application/json','Authorization': 'Bearer {0}'.format(Token_list[k])}
          #print(Token_list[k])       
          commit_response = requests.get(commit_url, headers=headers).json()                  
          try:
            if ( len(commit_response['message']) > 0):
              if( k == len(Token_list) - 1):
                time.sleep(600)
                exception_count = exception_count + 1
            else:
              continue
          except:
            break
        if ( exception_count == 0):
          break
        else:
          continue
      except:
        exception_count = 0



    if(len(commit_response) > 20):
      repo_result[n]["commits"] = len(commit_response)      
      n = n + 1
    else:      
      repo_result.pop(n)


  with open("repo_file3.json", "w") as repo_file:
    json.dump(repo_result, repo_file)
    print("function 3 finished", len(repo_result))

def func4():

  repo_result = []

  Token_list = ["b8964bafb3ec2e8d36eb826984091feedbd3d687"]
  #Token_list = [''**'',''**'',''**'',''**'',''**'']

  i = 30000  
  api_url = 'https://api.github.com/'

  while i < 40000: # This number will be increased to collect all the projects

    repo_url = api_url + 'repositories?since=' + str(i)  
    exception_count = 0  
    while exception_count < 2:
      try:
        for k in range(0,len(Token_list)):        
          headers = {'Content-Type': 'application/json','Authorization': 'Bearer {0}'.format(Token_list[k])}
          #print(Token_list[k])                 
          repo_response = requests.get(repo_url, headers=headers).json()
          #print(repo_response)                         
          try:            
            if ( len(repo_response['message']) > 0):              
              if( k == len(Token_list) - 1):
                time.sleep(600)
                exception_count = exception_count + 1
            else:
              continue
          except:            
            break
        if ( exception_count == 0):          
          break
        else:
          continue
      except:        
        exception_count = 0


    project_list = []

    try:      
      for j in range(0,len(repo_response)):
        project_id = repo_response[j]['id']
        project_name = repo_response[j]['name']
        project_full_name = repo_response[j]['full_name']
        project_html_url = repo_response[j]['html_url']
        project_owner_name = repo_response[j]['owner']['login']
        project_obj = {"id" : project_id, "name": project_name, "full_name" : project_full_name, "html_url" : project_html_url, "owner" : project_owner_name , "issues" :
        "", "commits" : "", "PR" : ""}
        project_list.append(project_obj)     


    except:
      print ("exception occurred")
    

    try:    
      last_id = repo_response[99]["id"]   
      i = last_id      
      repo_result = repo_result + project_list
          
    except:
      print(" exception inside function 4 ")
      break

    ## Removing projects having less than 8 issues
  
  p = 0
  while p < len(repo_result):    
    repo_owner = repo_result[p]['owner']
    repo_name = repo_result[p]['name']
    issue_url = api_url + 'repos/' + repo_owner + '/' + repo_name + '/' + 'issues'
    
    exception_count = 0  
    while exception_count < 2:
      try:
        for k in range(0,len(Token_list)):        
          headers = {'Content-Type': 'application/json','Authorization': 'Bearer {0}'.format(Token_list[k])}
          #print(Token_list[k])       
          issue_response = requests.get(issue_url, headers=headers).json()        
          try:
            if ( len(issue_response['message']) > 0):
              if( k == len(Token_list) - 1):
                time.sleep(600)
                exception_count = exception_count + 1
            else:
              continue
          except:
            break
        if ( exception_count == 0):
          break
        else:
          continue
      except:
        exception_count = 0



    if(len(issue_response) > 10):
      repo_result[p]["issues"] = len(issue_response)
      p = p + 1
    else:
      repo_result.pop(p)

    ## Selecting the projects with Pull Request > 0

  m = 0

  while m < len(repo_result):
    repo_owner = repo_result[m]['owner']
    repo_name = repo_result[m]['name']
    PR_url = api_url + 'repos/' + repo_owner + '/' + repo_name + '/' + 'pulls?state=all'


    exception_count = 0  
    while exception_count < 2:
      try:
        for k in range(0,len(Token_list)):        
          headers = {'Content-Type': 'application/json','Authorization': 'Bearer {0}'.format(Token_list[k])}
          #print(Token_list[k])       
          PR_response = requests.get(PR_url, headers=headers).json()        
          try:
            if ( len(PR_response['message']) > 0):
              if( k == len(Token_list) - 1):
                time.sleep(600)
                exception_count = exception_count + 1
            else:
              continue
          except:
            break
        if ( exception_count == 0):
          break
        else:
          continue
      except:
        exception_count = 0


    

    if(len(PR_response) > 0):
      repo_result[m]["PR"] = len(PR_response)      
      m = m + 1
    else:      
      repo_result.pop(m)

  ## Selecting Projects with commits > 20
  n = 0  
  while n < len(repo_result):
    repo_owner = repo_result[n]['owner']
    repo_name = repo_result[n]['name']
    commit_url = api_url + 'repos/' + repo_owner + '/' + repo_name + '/' + 'commits'


    exception_count = 0  
    while exception_count < 2:
      try:
        for k in range(0,len(Token_list)):        
          headers = {'Content-Type': 'application/json','Authorization': 'Bearer {0}'.format(Token_list[k])}
          #print(Token_list[k])       
          commit_response = requests.get(commit_url, headers=headers).json()                  
          try:
            if ( len(commit_response['message']) > 0):
              if( k == len(Token_list) - 1):
                time.sleep(600)
                exception_count = exception_count + 1
            else:
              continue
          except:
            break
        if ( exception_count == 0):
          break
        else:
          continue
      except:
        exception_count = 0



    if(len(commit_response) > 20):
      repo_result[n]["commits"] = len(commit_response)      
      n = n + 1
    else:      
      repo_result.pop(n)


  with open("repo_file4.json", "w") as repo_file:
    json.dump(repo_result, repo_file)
    print("function 4 finished", len(repo_result)) 


 
    
if __name__ == '__main__':
  lock = Lock()    
  p1 = Process(target=func1)
  p2 = Process(target=func2)
  p3 = Process(target=func3)
  p4 = Process(target=func4)
  print("Process created")
  p1.start()
  p2.start()
  p3.start()
  p4.start() 
  p1.join()
  p2.join()
  p3.join()
  p4.join() 
  
  