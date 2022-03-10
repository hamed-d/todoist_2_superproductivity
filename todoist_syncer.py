from todoist_api_python.api_async import TodoistAPIAsync
from todoist_api_python.api import TodoistAPI
from datetime import datetime
import json
from random import choice
from string import ascii_uppercase
import argparse

def get_tasks_sync(tk):
    api = TodoistAPI(tk)
    try:
        tasks = api.get_tasks()
        return tasks
    except Exception as error:
        print(error)
        
parser = argparse.ArgumentParser()
parser.add_argument('--token', type=str, help='Todoist API token for your account')
parser.add_argument('--path', type=str, help='Path to the directory containing the file named vault.json')
parser.add_argument('--subtasks', type=lambda x: (str(x).lower() in ['true', 't', 'y', 'yes']), help='Whether to add subtasks as tasks or not add them at all')
args = parser.parse_args()

tasks = get_tasks_sync(args.token)
curdate = datetime.today().strftime('%Y-%m-%d')
if not args.subtasks:
    for task in tasks:
        if task.due==None: continue
        if task.due.date == curdate:
            all_tasks.append(task.content)
else:
    cur_tasks = {}
    potential_cur_subtasks = []
    for task in tasks:
        if task.due==None and task.parent_id==None: continue
        elif task.due==None and task.parent_id!=None:
            potential_cur_subtasks.append([task.parent_id, task.content])
            continue
        elif task.due.date==curdate:
            cur_tasks.update({task.id: task.content})
    cur_tasks_2bremoved = []
    cur_tasks_values = list(cur_tasks.values())
    for potential_cur_subtask in potential_cur_subtasks:
        if potential_cur_subtask[0] in cur_tasks.keys():
            if cur_tasks[potential_cur_subtask[0]] not in cur_tasks_2bremoved:
                cur_tasks_2bremoved.append(cur_tasks[potential_cur_subtask[0]])
            cur_tasks_values.append(cur_tasks[potential_cur_subtask[0]]+'-'+potential_cur_subtask[1])
    for cur_task_2bremoved in cur_tasks_2bremoved:
        cur_tasks_values.remove(cur_task_2bremoved)
    all_tasks = cur_tasks_values.copy()
        
with open(args.path+'vault', mode='r') as f:
    sp = json.load(f)
cur_tasks = test = [sp['task']['entities'][task_id]['title'] for task_id in sp['task']['entities'].keys() if sp['task']['entities'][task_id]['isDone']==False]

for task in all_tasks.copy():
    for cur_task in cur_tasks:
        if task==cur_task:
            all_tasks.remove(task)
            
for task in all_tasks:
    newtaskid = ''.join(choice(ascii_uppercase) for i in range(21))
    sp['task']['ids'].append(newtaskid)
    sp['task']['entities'][newtaskid] = {}
    sp['task']['entities'][newtaskid]['id'] = newtaskid
    sp['task']['entities'][newtaskid]['projectId'] = None
    sp['task']['entities'][newtaskid]['subTaskIds'] = []
    sp['task']['entities'][newtaskid]['timeSpentOnDay'] = {}
    sp['task']['entities'][newtaskid]['timeSpent'] = 0
    sp['task']['entities'][newtaskid]['timeEstimate'] = 3600000
    sp['task']['entities'][newtaskid]['isDone'] = False
    sp['task']['entities'][newtaskid]['doneOn'] = None
    sp['task']['entities'][newtaskid]['title'] = task
    sp['task']['entities'][newtaskid]['notes'] = ''
    sp['task']['entities'][newtaskid]['tagIds'] = ['TODAY']
    sp['task']['entities'][newtaskid]['parentId'] = None
    sp['task']['entities'][newtaskid]['reminderId'] = None
    sp['task']['entities'][newtaskid]['created'] = 1646471971126
    sp['task']['entities'][newtaskid]['repeatCfgId'] = None
    sp['task']['entities'][newtaskid]['plannedAt'] = None
    sp['task']['entities'][newtaskid]['_showSubTasksMode'] = 2
    sp['task']['entities'][newtaskid]['attachments'] = []
    sp['task']['entities'][newtaskid]['issueId'] = None
    sp['task']['entities'][newtaskid]['issuePoints'] = None
    sp['task']['entities'][newtaskid]['issueType'] = None
    sp['task']['entities'][newtaskid]['issueAttachmentNr'] = None
    sp['task']['entities'][newtaskid]['attacissueLastUpdatedhments'] = None
    sp['task']['entities'][newtaskid]['issueWasUpdated'] = None
    sp['tag']['entities']['TODAY']['taskIds'].append(newtaskid)

with open(args.path+'synced_vault.json', 'w') as f:
    json.dump(sp, f)