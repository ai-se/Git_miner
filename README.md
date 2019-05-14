# Git_miner
Git Miner is a python based application to mine GitHub repository.

## Details about framework
The application uses GitHub API v3 along with pygit2 library for mining purpose. The application has a api based miner, which is used to mine GitHub information related to issues, pull requests, issue comments and other project metadata. It also has a git log based miner that uses pygit2 python library to get commit, committed file related information.

The api miner will use the personal token to access the GitHub API and then download the data, similarly the git_log miner will download the repo(all branches by default), and get commit, committed file related data(for now). Then the framework will make inferences to connect commits to committed files to issues. This will create 5 pickel files - 
1) commit 
2) committed file
3) issue
4) issue comments
5) user

each file is connected to another by commit number or issue number(except user). This will give user a complete view of connected issue, commit and committed file. Which will help in making the research easier.

The framework allows user to add their own code for specific mining tasks by utilizing the api and git_log codes in src/main folder. 

## Running experiments

For running the existing code, the user would need to add a csv file in the Git_miner folder and name it "project_list". 
The file should have following fields - 
1) repo_name
2) repo_owner
3) git_url(git://github.com/xxx/xxx.git) change xxx to repo_owner and name 
4) api_base_url(http://api.github.com)
5) source_type(github_repo)
6) access_token

