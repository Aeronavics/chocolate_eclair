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



def loginWithEmail(email, password):
    username = db.getUsernameFromEmail(email)
    return login(username, password)



def createTask(email, password, projectName, taskName, options):
    if not projectName:
        return uploadTask(email, password, taskName, options)
    else:
        projectId = db.getLatestProjectIdFromProjectName(projectName, email)
        if not projectId:
            projectId = createNewProject(email, password, projectName)
        return uploadTask(email, password, taskName, options, projectId)


def uploadImages(email, password, imagePath, taskId, projectId):
    token = login(adminUsername, adminPassword)
    images = []
    images.append(('images', (imagePath, open(imagePath, 'rb'), 'image/jpg')))

    res = requests.post('http://{}/api/projects/{}/tasks/{}/upload/'.format(serverIp,projectId,taskId), headers={'Authorization':'JWT {}'.format(token)}, files = images)
    return



def createNewProject(email, password, projectName=None):
    token = loginWithEmail(email, password)
    if not projectName:
        projectName ="Project created: " + datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
    res = requests.post('http://{}/api/projects/'.format(serverIp),
            headers={'Authorization':'JWT {}'.format(token)},
            data={'name':'{}'.format(projectName)}).json()
    return res['id']




def uploadTask(email, password, taskName, options, projectId=None):
    if not projectId:
        projectId =  db.getLatestProjectFromEmail(email)
    else:
        projectIdList = db.getAllProjectsFromEmail(email)
        if (projectId not in projectIdList):
            projectId = db.getLatestProjectFromEmail(email)
    if not projectId:
        projectId = createNewProject(email,password)

    token = login(adminUsername, adminPassword)
    if not taskName:
        taskName = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
    if not options:
        requestData = {'name': taskName, 'partial': True}
    else:
        requestData = {'name': taskName, 'partial': True, 'options': options}
    res = requests.post('http://{}/api/projects/{}/tasks/'.format(serverIp,projectId), headers={'Authorization':'JWT {}'.format(token)}, data = requestData)
    return res.json().get('id'), res.json().get('project')




def startTask(email, password, taskId, projectId):
    token = login(adminUsername, adminPassword)
    res = requests.post('http://{}/api/projects/{}/tasks/{}/commit/'.format(serverIp,projectId,taskId), headers={'Authorization':'JWT {}'.format(token)})
    return

