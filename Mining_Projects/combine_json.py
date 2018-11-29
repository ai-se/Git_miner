""" @Author Jchakra"""
""" This code is to combine multiple json files into a single json file (after removing duplicates) """
""" The json files need to be in the same directory """

import json,csv,os

combined_list = []

for filename in os.listdir(os.getcwd()):
	if filename.endswith('.json'):
		with open(os.path.join(os.getcwd(), filename)) as json_file:
			data = json.load(json_file)
			print(len(data))
			combined_list = combined_list + data

print(len(combined_list))

## Removing duplicates from combined_list  

seen = set()
new_list = []
for d in combined_list:
    t = tuple(d.items())
    if t not in seen:
        seen.add(t)
        new_list.append(d)

print(len(new_list))


## Creating a csv file to store the combined list

fp1 = open('combined_list.csv', 'w' , newline='')
myFile1 = csv.writer(fp1)
column_names1 = ['id','name','full_name','html_url','owner','issues','commits','PR']
myFile1.writerow(column_names1)
for i in range(len(new_list)):	
	myFile1.writerow(new_list[i].values())

fp1.close()


## Creating a json file to store the combined list

with open("combined_list.json", "w") as repo_file:
    json.dump(new_list, repo_file)