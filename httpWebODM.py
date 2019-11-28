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

def createTask(email, password, imageDir, projectName, taskName, options):
    if not projectName:
        return uploadImages(email, password, imagesDir, taskName, options)
    else:
        projectId = db.getLatestProjectIdFromProjectName(projectName, email)
        if not projectId:
            projectId = createNewProject(email, password, projectName)
        return uploadImages(email, password, imageDir, taskName, options, projectId)

def uploadImages(email, password, imageDir, taskName, options, projectId=None):
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

    images = []
    for root, dirs, files in os.walk(imageDir):
        for f in files:
            images.append(('images', (f, open(imageDir + '/' + f, 'rb'), 'image/jpg')))
    
    if not options:
        requestData = {'name': taskName}
    else:
        requestData = {'name': taskName, 'options': options}

    res = requests.post('http://{}/api/projects/{}/tasks/'.format(serverIp,projectId), headers={'Authorization':'JWT {}'.format(token)}, files = images, data = requestData)
    return res.json().get('id')

def createNewProject(email, password, projectName=None):
    username = db.getUsernameFromEmail(email)
    token = login(username, password)
    if not projectName:
        projectName ="Project created: " + datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
    res = requests.post('http://{}/api/projects/'.format(serverIp),
            headers={'Authorization':'JWT {}'.format(token)},
            data={'name':'{}'.format(projectName)}).json()
    return res['id']
