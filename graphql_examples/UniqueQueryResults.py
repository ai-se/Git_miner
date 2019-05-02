'''
Created on Feb 19, 2019

@author: peipei
'''
from pprint import pprint
import GraphQLQuery
import api
from itertools import chain
def getCmtMsgPerRepo(owner, name, first):
    query=GraphQLQuery.getFirstQueryCmtMsgPerRepo(owner, name, first)
    data=GraphQLQuery.run_query(query)
    
    hasNextPage=data['data']['repository']['ref']['target']['history']['pageInfo']['hasNextPage']
    endCursor=data['data']['repository']['ref']['target']['history']['pageInfo']['endCursor']
    data_msg=[cmt['node']['message'] for cmt in data['data']['repository']['ref']['target']['history']['edges']]
    count=1
    print("count:{} endCursor:{} size of data:{}".format(count,endCursor,len(data_msg)))
#     print(type(endCursor))
#     print(endCursor)
#     print(len(data_msg))   
    issues=[api.getLinkedIssueNum(msg) for msg in data_msg if msg is not None and msg!=""]
    issues=[item for item in issues if item is not None]
    print(issues)
    while hasNextPage:
        query=GraphQLQuery.getNextQueryCmtMsgPerRepo(owner, name, first, endCursor)
        data=GraphQLQuery.run_query(query)
        print(data.keys())
        if 'data' not in data:
            print(query)
            pprint(data)
            break
        hasNextPage=data['data']['repository']['ref']['target']['history']['pageInfo']['hasNextPage']
        endCursor=data['data']['repository']['ref']['target']['history']['pageInfo']['endCursor']
        data_msg=[cmt['node']['message'] for cmt in data['data']['repository']['ref']['target']['history']['edges']]
        
        count+=1
        print("count:{} endCursor:{} size of data:{}".format(count,endCursor,len(data_msg)))
#         print(len(data_msg))   
        temp=[api.getLinkedIssueNum(msg) for msg in data_msg if msg is not None and msg!=""]
        issues.extend([item for item in temp if item is not None])
    print(issues)
#     return data_msg

def getMsgPerPRRepo(owner, name, id_pr, first):
    query=GraphQLQuery.getFirstQueryMsgPerPRRepo(owner, name, id_pr, first)
    data=GraphQLQuery.run_query(query)
    
    hasNextPage=data['data']['repository']['pullRequest']['commits']['pageInfo']['hasNextPage']
    endCursor=data['data']['repository']['pullRequest']['commits']['pageInfo']['endCursor']
    data_msg=[cmt['node']['commit']['message'] for cmt in data['data']['repository']['pullRequest']['commits']['edges']]
    count=1
#     print("count:{} endCursor:{} size of data:{}".format(count,endCursor,len(data_msg)+2))
    
    data_msg.extend([data['data']['repository']['pullRequest']['title'],data['data']['repository']['pullRequest']['bodyText']])
    
    while hasNextPage:
        query=GraphQLQuery.getNextQueryMsgPerPRRepo(owner, name, id_pr, first, endCursor)
        data=GraphQLQuery.run_query(query)
        print(data.keys())
#         if 'data' not in data:
#             print(query)
#             pprint(data)
#             break
        hasNextPage=data['data']['repository']['pullRequest']['commits']['pageInfo']['hasNextPage']
        endCursor=data['data']['repository']['pullRequest']['commits']['pageInfo']['endCursor']
        
        data_msg.extend([cmt['node']['commit']['message'] for cmt in data['data']['repository']['pullRequest']['commits']['edges']])
        
        count+=1
#         print("count:{} endCursor:{} size of data:{}".format(count,endCursor,len(data_msg)))
        
    issues=[api.getLinkedIssueNum(msg) for msg in set(data_msg) if msg is not None and msg!=""]
#     print(issues)
    issues=list(chain(*[item for item in issues if item is not None]))
    print(issues)
    return issues

if __name__ == '__main__':
    getCmtMsgPerRepo("PyGithub","PyGithub",'100')
    pass

