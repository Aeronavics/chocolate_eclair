import itertools
import httpWebODM
import os
import exifEditor

class TaskModel:

    def __init__(self, email, password, projectName, taskName, options):
        self.id = id(self)
        self.email = email
        self.password = password
        self.images = "./uploads/{}/".format(self.id)
        self.projectName = projectName
        self.taskName = taskName
        self.projectId = None;
        self.taskId = None;
        self.options = options
        if not os.path.exists("./uploads/"):
            os.mkdir("./uploads/")
        if not os.path.exists(self.images):
            os.mkdir(self.images)


    def uploadTask(self):
        exifEditor.validate(self.images)
        self.taskId, self.projectId = httpWebODM.createTask(self.email, self.password, self.projectName, self.taskName, self.options)


    def uploadImages(self):
        exifEditor.validate(self.images)
        for root, dirs, files in os.walk(self.images):
            for f in files:
                httpWebODM.uploadImages(self.email, self.password, self.images + '/' + f, self.taskId, self.projectId)
                os.remove(self.images + '/' + f)


    def startTask(self):
        httpWebODM.startTask(self.email, self.password, self.taskId, self.projectId)
