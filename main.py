# Jira API
# Adds a comment to a task
# Author: Fabio Crestani

import requests, json
from collections import namedtuple
from jira_api_token import *
import os
import sys

def jiraApiGet(server, service, params):
	headers = {'Authorization' : 'Basic ' + jira_api_token}
	r = requests.get(server + service, headers=headers, params=params,
					 verify=True)
	return json.loads(r.text)
	
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
	print("	main.py <Jira Task ID> <Comment to be added>")

def main():
	server = "https://sandbox-fc.atlassian.net"

	# Query one given issue
	#result = jiraApiQuery(server, "/rest/api/3/issue/TP-1")
	#print(json.dumps(result, indent=1))
	
	# Query list of all issues in Project AP
	#query = {'jql' : 'project = AP'}
	#result = jiraApiQuery(server, "/rest/api/3/search", query)
	#print(json.dumps(result, indent=1))
	
	# Query list of all issues in Sprint 1
	#query = {'jql' : 'project = \'AP\' and Sprint = \'Sprint 1\''}
	#json_result = jiraApiQuery(server, "/rest/api/3/search", query)
	#print(json.dumps(json_result, indent=1))
	
	#print("")
	#print("Result of query " + str(query))
	#print("Number of issues: " + str(json_result['total']))
	#print("")
	#for issue in json_result['issues']:
	#	print("[" + issue['key'] + "] " + issue['fields']['summary'] +
	#		" -> " + issue['fields']['status']['name'])
	
	# Add a comment to a task
	if len(sys.argv) < 3:
		print('Eror: Invalid argument.')
		usage()
		sys.exit()

	task_id = sys.argv[1]
	comment = sys.argv[2]
	
	# Query tasks
	query = {'jql' : 'project = \'AP\' and id = \'' + task_id + '\''}
	json_result = jiraApiGet(server, "/rest/api/3/search", query)
	
	print("")
	print("Adding comment to task (" + str(json_result['total']) + "): ", end="")
	for issue in json_result['issues']:
		print("[" + issue['key'] + "] " + issue['fields']['summary'])
						
	if (jiraApiAddComment(server, task_id, comment) == False):
		print("Error adding comment to task")
	else:
		print("Comment added")
	
	
if __name__ == "__main__":
	main() # execute only if run as a script

