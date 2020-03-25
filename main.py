import requests, json
from jira_api_token import *

def jiraApiQuery(server, service):
	headers = {'Authorization' : 'Basic ' + jira_api_token}
	r = requests.get(server + service, headers=headers, verify=True)
	return json.loads(r.text)


def main():
	server = "https://sandbox-fc.atlassian.net"

	# Query one given issue
	#result = jiraApiQuery(server, "/rest/api/3/issue/TP-1")
	#print(json.dumps(result, indent=1))
	
	# Query list of all issues
	result = jiraApiQuery(server, "/rest/api/3/issue/picker")
	print(json.dumps(result, indent=1))

if __name__ == "__main__":
	# execute only if run as a script
	main()