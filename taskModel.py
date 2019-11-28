import itertools
import httpWebODM
import os
import exifEditor

class TaskModel:

    def __init__(self, email, password, projectName=None, options=None):
        self.id = id(self)
        self.email = email
        self.password = password
        self.images = "./uploads/{}/".format(self.id)
        self.projectName = projectName
        self.options = options
        if not os.path.exists("./uploads/"):
            os.mkdir("./uploads/")
        if not os.path.exists(self.images):
            os.mkdir(self.images)


    def uploadTask(self):
        exifEditor.validate(self.images)
        tid = httpWebODM.createTask(self.email, self.password, self.images, self.projectName, self.options)
        return tid


