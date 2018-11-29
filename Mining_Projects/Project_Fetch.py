""" @Author Jchakra"""
""" To list all the projects we used in the TSE Paper """

import glob,csv
import pandas as pd


"""Data folder contains .pkl files """
combined_list = glob.glob('Data/*.pkl')
print(combined_list)

for i in range(len(combined_list)):
	combined_list[i] = combined_list[i].split('Data\\')[1]
	combined_list[i] = combined_list[i].split('_final_results.pkl')[0]

""" combined_list.csv contains the projects we used in the paper """
fp1 = open('combined_list.csv', 'w' , newline='')
myFile1 = csv.writer(fp1)
column_names1 = ['id','name','html_url','owner']
myFile1.writerow(column_names1)	
	

project_list = pd.read_csv('Projects.csv')

for i in range(len(combined_list)):
	for j in range(project_list.shape[0]):
		if combined_list[i] == project_list.loc[j,'name']:			
			row = [project_list.loc[j,'id'],project_list.loc[j,'name'],project_list.loc[j,'url'],project_list.loc[j,'owner']]
			myFile1.writerow(row)

fp1.close()