'''
Created on Feb 19, 2019

@author: peipei
'''
import requests
import json
from time import sleep
import sys
from datetime import datetime
headers = {"Authorization": "token your_github_token"}

# The GraphQL query (with a few aditional bits included) itself defined as a multi-line string.       
query1 = """
{
  viewer {
    login
  }
  rateLimit {
    limit
    cost
    remaining
    resetAt
  }
}
"""

def run_query(query): # A simple function to use requests.post to make the API call. Note the json= section.
    request = requests.post('https://api.github.com/graphql', json={'query': query}, headers=headers)
#     print("request return code - {}".format(request.status_code))
    if request.status_code == 200:
        return request.json()
#     else:
#         tries=3
#         while request.status_code != 200 and tries>0:
#             print("sleep {} min".format(4-tries))
#             sleep((4-tries)*60)
# 
#             request = requests.post('https://api.github.com/graphql', json={'query': query}, headers=headers)
#             tries-=1
#             print("Retry {} th".format(3-tries))
#         if request.status_code == 200:
#             return request.json()
    else: 
        print("request return code - {}".format(request.status_code))
        raise Exception("Query failed to run by returning code of {}. {}".format(request.status_code, query))
    
def checkTokenLimit():
    result = run_query(query1) # Execute the query
    remaining_rate_limit = result["data"]["rateLimit"]["remaining"] # Drill down the dictionary
    print("Remaining rate limit - {}".format(remaining_rate_limit))
    
    resetTime = result["data"]["rateLimit"]["resetAt"]
    print("GitHub API must be reset to time - {}".format(resetTime))
    
    resetTime=datetime.strptime(resetTime,'%Y-%m-%dT%H:%M:%SZ')
    nowTimeUTC=datetime.utcnow()
    print("UTC time now - {}".format(nowTimeUTC))
    if nowTimeUTC.date()==resetTime.date() and nowTimeUTC.time()<resetTime.time():
        print("will reset in future")
        return remaining_rate_limit
    else:
        raise Exception("resetAt error")
def getFirstQueryCmtMsgPerRepo(owner,name,first):
    query_first='''
    {{
      repository(owner:"{owner}", name:"{name}") {{
        description
        ref(qualifiedName: "master") {{
          name
          target{{
            ... on Commit{{
              id
              history(first: {first}) {{
                pageInfo {{
                  hasNextPage
                  endCursor
                }}
                edges {{
                  node {{
                    message
                    oid
                  }}
                }}
              }}
            }}
          }}
        }}
      }}
    }}
    '''
    variables={"owner": owner,"first":first,"name":name}
    return query_first.format(**variables)

def getNextQueryCmtMsgPerRepo(owner,name,first,endCursor):
    query_next='''
    {{
      repository(owner:"{owner}", name:"{name}") {{
        description
        ref(qualifiedName: "master") {{
          name
          target{{
            ... on Commit{{
              id
              history(first:{first}, after: "{endCursor}") {{
                pageInfo {{
                  hasNextPage
                  endCursor
                }}
                edges {{
                  node {{
                    message
                    oid
                  }}
                }}
              }}
            }}
          }}
        }}
      }}
    }}
    '''
    variables={"owner": owner,"first":first,"name":name,"endCursor":endCursor}
    return query_next.format(**variables)     

def getFirstQueryMsgPerPRRepo(owner,name,id_pr,first):
    query_first='''
{{
  repository(owner: "{owner}", name: "{name}") {{
    pullRequest(number: {prID}) {{
      title
      bodyText
      commits(first: {first}) {{
        totalCount
          pageInfo{{
            hasNextPage
            endCursor
          }}
        edges {{
          node {{
            commit {{
              oid
              message
            }}
          }}
        }}
      }}
    }}
  }}
}}
'''
    variables={"owner": owner,"first":first,"name":name,"prID":id_pr}
    return query_first.format(**variables)

def getNextQueryMsgPerPRRepo(owner,name,id_pr,first,endCursor):
    query_next='''
{{
  repository(owner: "{owner}", name: "{name}") {{
    pullRequest(number: {prID}) {{
      title
      bodyText
      commits(first: {first} after: "{endCursor}") {{
        totalCount
          pageInfo{{
            hasNextPage
            endCursor
          }}
        edges {{
          node {{
            commit {{
              oid
              message
            }}
          }}
        }}
      }}
    }}
  }}
}}
'''
    variables={"owner": owner,"first":first,"name":name,"prID":id_pr,"endCursor":endCursor}
    return query_next.format(**variables)      

if __name__ == '__main__':
    checkTokenLimit()

    pass
