# Jira API
# Adds a comment to a task
# Author: Fabio Crestani

import requests, json
from collections import namedtuple
from jira_api_token import *
import os
import sys
from datetime import datetime

def jiraApiGet(server, service, params):
	headers = {'Authorization' : 'Basic ' + jira_api_token}
	r = requests.get(server + service, headers=headers, params=params, verify=True)
	return [json.loads(r.text), r.status_code]
	
def jiraApiPost(server, service, data):
	headers = {'Authorization' : 'Basic ' + jira_api_token, 'Content-Type' : 'application/json'}
	r = requests.post(server + service, headers=headers,
					 verify=True, data=json.dumps(data))
	return r.status_code
	
def jiraApiAddComment(server, task_id, comment):
	comment_obj = {"body": comment}
	ret = jiraApiPost(server, "/rest/api/2/issue/" + task_id + "/comment", comment_obj)
	return (ret == 201)
	
def usage():
	print("	main.py <Jira Task ID> <Comment to be added> [--force-upload]")

def main():
	server = "https://sandbox-fc.atlassian.net"
	is_file_ready_to_upload = False

	# Parse arguments
	if len(sys.argv) < 3:
		print('Eror: Invalid argument.')
		usage()
		sys.exit()
	task_id = sys.argv[1]
	comment = sys.argv[2]
	if len(sys.argv) == 4:
		if sys.argv[3] == "--force-upload":
			is_file_ready_to_upload = True


	# Open buffer file
	number_of_entries_in_file = 0
	try:
		with open(task_id + '.txt') as json_file:
			json_data = json.load(json_file)
			for c in json_data['comments']:
				number_of_entries_in_file = number_of_entries_in_file + 1
	except:
		print("Error opening file. Will create new file " + task_id + ".txt")
		json_data = json.loads('{"comments": []}')


	# Add comment to buffer file
	now = datetime.now()
	timestamp = now.strftime("%d.%m.%Y %H:%M:%S")
	comment_obj = {'body' : "[" + timestamp + "] " + comment}
	json_data['comments'].append(comment_obj)
	number_of_entries_in_file = number_of_entries_in_file + 1
	print("Comment added to buffer file")
	print(str(number_of_entries_in_file) + " comments pending upload")
	with open(task_id + '.txt', "w") as file:
		json.dump(json_data, file)
	
	
	## Send whole file to server when ready
	if is_file_ready_to_upload == False:
		print("Waiting to upload file")
		return 0
	
	
	# Query tasks
	query = {'jql' : 'project = \'AP\' and id = \'' + task_id + '\''}
	json_result, status_code = jiraApiGet(server, "/rest/api/3/search", query)
	if (status_code != 200):
		print("Error: Task not found")
		return 1
	
	# Prepare comment body
	print("Preparing to upload comments")
	comment_body = ""
	try:
		with open(task_id + '.txt') as json_file:
			json_data = json.load(json_file)
			for c in json_data['comments']:
				number_of_entries_in_file = number_of_entries_in_file + 1
				comment_body = comment_body + "\n" + c['body']
	except:
		print("Error opening file")
		return 1


	# Send POST request with comment body
	print("Adding comment to task (" + str(json_result['total']) + "): ", end="")
	for issue in json_result['issues']:
		print("[" + issue['key'] + "] " + issue['fields']['summary'])
						
	if (jiraApiAddComment(server, task_id, comment_body) == False):
		print("Error adding comments to task")
		return 1
	else:
		print("Comments added")
		os.remove(task_id + '.txt')
		return 0
	
	
if __name__ == "__main__":
	main() # execute only if run as a script

