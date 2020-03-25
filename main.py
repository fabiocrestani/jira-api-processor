import requests, json
from jira_api_token import *

headers = {'Authorization' : 'Basic ' + jira_api_token}

r = requests.get(
	'https://sandbox-fc.atlassian.net/rest/api/3/issue/TP-1', 
	headers=headers, 
	verify=True)

j = json.loads(r.text)

print(json.dumps(j, indent=1))