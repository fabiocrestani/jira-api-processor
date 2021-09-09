# Jira API
# Adds a comment to a task
# Author: Fabio Crestani

import logging
from jira_api_token import *
from JiraInterface import Jira

from pprint import pprint

class User():
	def __init__(self, name, email, link):
		self.name = name
		self.email = email
		self.link = link

class Priority():
	def __init__(self, id, name):
		self.id = id
		self.name = name

class Status():
	def __init__(self, id, name, description):
		self.id = id
		self.name = name
		self.description = description

class Task():
	def __init__(self, key, link, creator, assignee, created, priority,
			progress, updated, summary, description, duedate, status):
		self.key = key
		self.link = link
		self.creator = creator
		self.assignee = assignee
		self.created = created	
		self.priority = priority
		self.progress = progress
		self.updated = updated
		self.summary = summary
		self.description = description
		self.duedate = duedate
		self.status = status

def main():
	logging.basicConfig(level=logging.DEBUG)
	logging.info('Starting')

	server = "https://crestani.atlassian.net"
	project = "fc"
	jira = Jira(server, project)

	local_tasks = [
		Task("FC-1", "", User("", "", ""), User("", "", ""),
			Priority("", ""), "", "", "", "", "", "",
			Status("", "", "")),
		Task("FC-2", "", User("", "", ""), User("", "", ""),
			Priority("", ""), "", "", "", "", "", "",
			Status("", "", ""))
	]

	# "pull" tasks: Update local_tasks with remote data
	for task in local_tasks:
		print(task.__dict__)
	
	remote_tasks = jira.pullTasks(local_tasks)

	for task in remote_tasks:
		issues = task.get("issues")
		issue0 = issues[0]
		key = issue0.get("key")
		link = issue0.get("self")
		fields = issue0.get("fields")
		creator = fields.get("creator")
		creator_name = creator.get("displayName")
		creator_email = creator.get("emailAddress")
		creator_link = creator.get("self")
		assignee = fields.get("assignee")
		assignee_name = ""
		assignee_email = ""
		assignee_link = ""
		try:
			assignee_name = assignee.get("displayName")
			assignee_email = assignee.get("emailAddress")
			assignee_link = assignee.get("self")
		except:
			pass

		created = fields.get("created")
		priority = fields.get("priority")
		priority_id = priority.get("id")
		priority_name = priority.get("name")
		progress = fields.get("progress")
		updated = fields.get("updated")
		summary = fields.get("summary")
		duedate = fields.get("duedate")
		description = fields.get("description")

		status = fields.get("status")
		status_id = status.get("id")
		status_name = status.get("name")
		status_description = status.get("description")
		
		t = Task(key,
			link,
			User(creator_name, creator_email, creator_link),
			User(assignee_name, assignee_email, assignee_link),
			created,
			Priority(priority_id, priority_name),
			progress,
			updated,
			summary,
			description,
			duedate,
			Status(status_id, status_name, status_description))

		print("")
		print("***** TASK *****")
		pprint(t.__dict__)
		print("")
		



	
	
if __name__ == "__main__":
	main() # execute only if run as a script

