import requests
import json
import db
from datetime import datetime

serverIp = "127.0.0.1:8000"
adminUsername = "ServerUser"
adminPassword = "ServerPassw0rd"



def login(username, password):
    res = requests.post('http://' + serverIp +'/api/token-auth/', data={'username': username, 'password': password}).json()
    return res['token']

def uploadImages(email, password, images, projectId=None):
    if not projectId:
        projectId =  db.getLatestProjectFromEmail(email)
    else:
        projectIdList = db.getAllProjectsFromEmail(email)
        if (projectId not in projectIdList):
            projectId = db.getLatestProjectFromEmail(email)
    if not projectId:
        projectId = createNewProject(email,password)

    token = login(adminUsername, adminPassword)
    res = requests.post('http://{}/api/projects/{}/tasks/'.format(serverIp,projectId),
            headers={'Authorization':'JWT {}'.format(token)},
            files = images,
            data={'name':datetime.now().strftime("%d/%m/%Y, %H:%M:%S")}).json()

def createNewProject(email, password):
    username = db.getUsernameFromEmail(email)
    token = login(username, password)
    res = requests.post('http://{}/api/projects/'.format(serverIp),
            headers={'Authorization':'JWT {}'.format(token)},
            data={'name':'Project created: {}'.format(datetime.now().strftime("%d/%m/%Y, %H:%M:%S"))}).json()
    return res['id']
