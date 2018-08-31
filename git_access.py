# -*- coding: utf-8 -*-
"""
Created on Wed Aug 22 10:14:40 2018

@author: suvod
"""

import base64
import requests
import time

requests.packages.urllib3.disable_warnings()


class RestClient(object):
    CONTENT_XML = "text/xml"
    CONTENT_URL_ENCODED = "application/x-www-form-urlencoded"
    DEFAULT_REQUEST_TIMEOUT = 60
    DEFAULT_MAX_RETRY_COUNT = 5
    DEFAULT_RETRY_INTERVAL = 60
    
    def __init__(self):
        self.session = requests.Session()
        
    def add_header(self, key, value):
        self.session.headers[key] = value
    
    def add_token_auth_header(self, token):
        self.add_header('Authorization', "token {}".format(token))
        
    def get(self, uri, headers=None, timeout=DEFAULT_REQUEST_TIMEOUT, **kwargs):
        retry_count = 0
        max_retry_count = 5
        retry_interval = 60
        
        while True:
            try:
                response = self.session.get(uri, headers=headers, timeout=timeout, **kwargs)
                
                if response.status_code == 200:
                    return response
                else:
                    break
            except requests.RequestException as e:
                if retry_count >= max_retry_count:
                    raise e
                time.sleep(retry_interval)
                retry_count += 1
                logger.warning("possibly recoverable error: exception='%s'", str(e))
                logger.warning("Retrying GET request: time %d...", retry_count)
                
                

from requests.exceptions import HTTPError
from requests.exceptions import ConnectionError
from requests.utils import parse_header_links
import json
import time
import urllib
#import urlparser
#import logger

class GitHubClient(RestClient):
    USERS_URI_FORMAT = "{}/users"
    USER_URI_FORMAT = "{}/users/{}"
    REPOS_URI_FORMAT =  "{}/repos/{}"
    REPO_URI_FORMAT = "{}/repos/{}/{}"
    BRANCHES_URI_FORMAT = "{}/branches"
    BRANCH_URI_FORMAT = "{}/branches/{}"
    COMMENTS_URI_FORMAT = "{}/comments"
    COMMITS_URI_FORMAT = "{}/commits"
    COMMIT_URI_FORMAT = "{}/commits/{}"
    CONTRIBUTORS_URI_FORMAT = "{}/contributors"
    EVENTS_URI_FORMAT = "{}/events"
    ISSUES_URI_FORMAT = "{}/issues"
    ISSUE_URI_FORMAT = "{}/issues/{}"
    ISSUES_COMMENTS_URI_FORMAT = "{}/issues/comments"
    ISSUES_EVENTS_URI_FORMAT = "{}/issues/events"
    PULLS_URI_FORMAT = "{}/pulls"
    
    def __init__(self, source=None, wait=True):
        super(GitHubClient, self).__init__()
        self.source = source
        self.access_token = source.get('access_token')
        self.wait = wait
        if self.access_token is not None:
            self.add_token_auth_header(self.access_token)
        
    def _session_get(self, uri, headers=None, timeout=360, **kwargs):
        try:
            response = self.session.get(uri, headers=headers, timeout=timeout, **kwargs)
            return response
        except ConnectionError as e:
            logger.error('Github Connection aborted, Retrying....')
            raise e
    
    def get(self, uri, headers=None, timeout=360, **kwargs):
        response = self._session_get(uri, headers=headers, timeout=timeout, **kwargs)
        status_code = response.status_code
        
        if status_code == 401:
            raise Exception('HTTP ERROR 401: Unauthorized token')
        
        if self._check_api_limit(uri, response):
            return self.get(uri, headers, timeout, **kwargs)
        
        if status_code != 200:
            if status_code == 403:
                try:
                    error = json.loads(response.content)
                except Exception as e:
                    
                    if self._check_api_limit(uri, response):
                        return self.get(uri, headers, timeout, **kwargs)
                    logger.error(e.message)
                    raise ValueError("Response from {} not json parseable: {}".format(uri, response.content))
                message = error['message']
                if "API rate limit exceeded" in message:
                    logger.warning('API rate limit exceeded for uri: {}'.format(uri))
                    if self.wait:
                        rate_limit_reset_time = long(response.headers.get('X-RateLimit-Reset'))
                        self._wait_for_api_rate_limit_reset_time(uri, rate_limit_reset_time)
                        return self.get(uri, headers, timeout, **kwargs)
                    else:
                        logger.debug("Waiting flag is {}, breaking out".format(self.wait))
                elif "Abuse detection mechanism" in message:
                    logger.warning('Abuse detection mechanism triggered for uri: {}'.format(uri))
                    if self.wait:
                        rate_limit_reset_time = long(response.headers.get('Retry-After'))
                        self._wait_for_api_rate_limit_reset_time(uri, rate_limit_reset_time)
                        return self.get(uri, headers, timeout, **kwargs)
                    else:
                        logger.debug("Waiting flag is {}, breaking out".format(self.wait))
            
            response.raise_for_status()
        return response
    
    def _check_api_limit(self, uri, response):
        if 'X-RateLimit_Remaining' in response.headers:
            remaining_limit = long(response.headers['X-RateLimit_Remaining'])
            if remaining_limit < 500:
                if "account was suspended " in response.content:
                    raise Exception("GitHub account was suspended. Please try another tokens")
                
                if self.wait:
                    rate_limit_reset_time = long(response.headers.get('X-RateLimit-Reset'))
                    self._wait_for_api_rate_limit_reset_time(uri, rate_limit_reset_time)
                    return True
        return False
    
    def _wait_for_api_rate_limit_reset_time(self, uri, rate_limit_reset_time):
        now = time.mktime(time.localtime())
        sleep_time = rate_limit_reset_time - now + 1
        rate_limit_reset_strftime = time.strftime("%d %b %Y %H:%M:%S", time.localtime(rate_limit_reset_time))
        logger.warning("API rate limit exceeded for uri: {}. Waiting for %d mins %d seconds. Restarting at %s ...".format(uri), 
                       sleep_time / 60, sleep_time % 60, rate_limit_reset_strftime)
        time.sleep(sleep_time)
        
    def _wait_for_retry_time_reset(self, uri, retry_time):
        logger.warning("Abuse detection machanism triggered for uri: {}. Waiting for %d secs".format(uri), retry_time)
        time.sleep(retry_time)