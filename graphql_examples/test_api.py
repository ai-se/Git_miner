'''
Created on Apr 20, 2019

@author: peipei
'''
import unittest
from github import Github
import api
import UniqueQueryResults


class Test(unittest.TestCase):


    def test_getLinkedIssueNum(self):
        res=api.getLinkedIssueNum('close an issue')
        assert(res is None)
        
        res=api.getLinkedIssueNum("Closes #757\n Closes #860")
        assert(set(res) == set(['757','860']))
        
        res=api.getLinkedIssueNum("Fix #45. Pattern attribute value invalid as regular expression")
        assert(res==['45'])
        pass
    
    def test_isPRLinked2Issue(self):
        github=Github("your_githu_token")
        res=api.isPRLinked2Issue(github,"https://github.com/instedd/guisso/pull/51")
        assert(res==["https://github.com/instedd/guisso/issues/45"])
        res=api.isPRLinked2Issue(github,"https://github.com/PyGithub/PyGithub/pull/1090")
        assert(res==["https://github.com/PyGithub/PyGithub/issues/1089"])
        res=api.isPRLinked2Issue(github,"https://github.com/instedd/guisso/pull/47")
        assert(res==[])
        
        res=api.isPRLinked2Issue2("https://github.com/instedd/guisso/pull/51")
        assert(res==["https://github.com/instedd/guisso/issues/45"])
        res=api.isPRLinked2Issue2("https://github.com/PyGithub/PyGithub/pull/1090")
        assert(res==["https://github.com/PyGithub/PyGithub/issues/1089"])
        res=api.isPRLinked2Issue2("https://github.com/instedd/guisso/pull/47")
        assert(res==[])
        res=api.isPRLinked2Issue2("https://github.com/apache/incubator-shardingsphere/pull/1222")
        assert(res==['https://github.com/apache/incubator-shardingsphere/issues/1045'])
    
    def test_getMsgPerPRRepo(self):
        res=UniqueQueryResults.getMsgPerPRRepo("PyGithub", "PyGithub", 1090, 10)
        assert(res==['1089'])
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_getLinkedIssueNum']
#     unittest.main()
    Test().test_isPRLinked2Issue()