import requests
import json
import db
from datetime import datetime
import time
import os

serverIp = "127.0.0.1:8000"
adminUsername = "ServerUser"
adminPassword = "ServerPassw0rd"



def login(username, password):
    res = requests.post('http://' + serverIp +'/api/token-auth/', data={'username': username, 'password': password}).json()
    return res['token']



def createTask(username, password, projectName, taskName, options):
    if not projectName:
        return uploadTask(username, password, taskName, options)
    else:
        projectId = db.getLatestProjectIdFromProjectName(projectName, username)
        if not projectId:
            projectId = createNewProject(username, password, projectName)
        return uploadTask(username, password, taskName, options, projectId)


def uploadImages(username, password, imagePath, taskId, projectId):
    token = login(adminUsername, adminPassword)
    images = []
    images.append(('images', (imagePath, open(imagePath, 'rb'), 'image/jpg')))

    res = requests.post('http://{}/api/projects/{}/tasks/{}/upload/'.format(serverIp,projectId,taskId), headers={'Authorization':'JWT {}'.format(token)}, files = images)
    return



def createNewProject(username, password, projectName=None):
    token = login(username, password)
    if not projectName:
        projectName ="Project created: " + datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
    res = requests.post('http://{}/api/projects/'.format(serverIp),
            headers={'Authorization':'JWT {}'.format(token)},
            data={'name':'{}'.format(projectName)}).json()
    return res['id']




def uploadTask(username, password, taskName, options, projectId=None):
    if not projectId:
        projectId =  db.getLatestProjectFromUsername(username)
    else:
        projectIdList = db.getAllProjectsFromUsername(username)
        if (projectId not in projectIdList):
            projectId = db.getLatestProjectFromUsername(username)
    if not projectId:
        projectId = createNewProject(username,password)

    token = login(adminUsername, adminPassword)
    if not taskName:
        taskName = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
    if not options:
        requestData = {'name': taskName, 'partial': True}
    else:
        requestData = {'name': taskName, 'partial': True, 'options': options}
    res = requests.post('http://{}/api/projects/{}/tasks/'.format(serverIp,projectId), headers={'Authorization':'JWT {}'.format(token)}, data = requestData)
    return res.json().get('id'), res.json().get('project')




def startTask(username, password, taskId, projectId):
    token = login(adminUsername, adminPassword)
    res = requests.post('http://{}/api/projects/{}/tasks/{}/commit/'.format(serverIp,projectId,taskId), headers={'Authorization':'JWT {}'.format(token)})
    return

