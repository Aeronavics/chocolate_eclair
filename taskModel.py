import itertools
import httpWebODM
import os

class TaskModel:
    newid = itertools.count()

    def __init__(self, email, password, projectName=None):
        self.id = next(TaskModel.newid)
        self.email = email
        self.password = password
        self.images = "./uploads/{}/".format(self.id)
        self.projectName = projectName
        if not os.path.exists(self.images):
            os.mkdir(self.images)


    def uploadTask(self):
        tid = httpWebODM.createTask(self.email, self.password, self.images, self.projectName)
        return tid


