# JiraInterface.py
# Fabio Crestani

import requests, json
from jira_api_token import *
import http.client
import logging

class JiraApi():
	def __init__(self, server):
		self.server = server

	def get(self, service, params):
		headers = {'Authorization' : 'Basic ' + jira_api_token}
		req = self.server + service
		logging.debug("Debug: GET " + req)
		logging.debug("Debug: GET params: " + str(params))
		r = requests.get(req,
			headers=headers, 
			params=params,
			verify=True)
		logging.debug("Debug: GET response code: " + str(http.client.responses[r.status_code]))

		try:
			return [r.json(), r.status_code]
		except Exception as e:
			logging.error(e)
			return [None, r.status_code]
		
		
	def post(self, service, data):
		headers = {'Authorization' : 'Basic ' + jira_api_token,
			'Content-Type' : 'application/json'}
		req = self.server + service
		logging.debug("Debug: POST " + req)
		logging.debug("Debug: POST data: " + str(data))
		r = requests.post(req,
			headers=headers,
			verify=True,
			data=json.dumps(data))
		return r.status_code

class Jira():
	def __init__(self, server, project):
		self.server = server
		self.project = project
		self.api = JiraApi(server)
		
	def addComment(self, task_id, comment):
		comment_obj = {"body": comment}
		ret = self.api.post("/rest/api/2/issue/" + task_id + "/comment", comment_obj)
		return ret == 201

	def getAllTasks(self):
		query = {'jql' : 'project = \'' + self.project + '\''}
		json_result, status_code = self.api.get("/rest/api/3/search", query)
		if status_code != 200:
			logging.debug("Error: Tasks not found")
			logging.debug("Debug: " + str(http.client.responses[status_code]))
		return json_result

	def getTask(self, task_id):
		query = {'jql' : 'project = \'' + self.project + '\' and id = \'' + str(task_id) + '\''}
		json_result, status_code = self.api.get("/rest/api/3/search", query)
		if status_code != 200:
			logging.debug("Error: Task not found")
			logging.debug("Debug: " + str(http.client.responses[status_code]))
		return json_result
	

	def pullTasks(self, tasks):
		remote_tasks = []
		for task in tasks:
			remote_task = self.getTask(task.key)
			remote_tasks.append(remote_task)
		return remote_tasks
	
