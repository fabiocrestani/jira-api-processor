import requests, json
from collections import namedtuple
from jira_api_token import *

def jiraApiQuery(server, service, params):
	headers = {'Authorization' : 'Basic ' + jira_api_token}
	r = requests.get(server + service, headers=headers, params=params,
					 verify=True)
	return json.loads(r.text)

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
	query = {'jql' : 'project = \'AP\' and Sprint = \'Sprint 1\''}
	json_result = jiraApiQuery(server, "/rest/api/3/search", query)
	#print(json.dumps(json_result, indent=1))
	
	print("")
	print("Result of query " + str(query))
	print("Number of issues: " + str(json_result['total']))
	print("")
	for issue in json_result['issues']:
		print("[" + issue['key'] + "] " + issue['fields']['summary'] +
			" -> " + issue['fields']['status']['name'])
	
if __name__ == "__main__":
	# execute only if run as a script
	main()
