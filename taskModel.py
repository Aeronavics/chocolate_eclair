import paramiko
from scp import SCPClient
import itertools
import httpWebODM
import os
import exifEditor
import shutil


class TaskModel:

    def __init__(self, email, password, projectName, taskName, options):
        self.id = id(self)
        self.email = email
        self.password = password
        self.images = "/home/james/Documents/chocolate_eclair/uploads/{}".format(self.id)
        self.projectName = projectName
        self.taskName = taskName
        self.projectId = None;
        self.taskId = None;
        self.options = options
        self.log = "/home/james/Documents/chocolate_eclair/logs/{}".format(self.id)
        self.logName = ""
        if not os.path.exists("./uploads/"):
            os.mkdir("./uploads/")
        if not os.path.exists(self.images):
            os.mkdir(self.images)
        if not os.path.exists("./logs/"):
            os.mkdir("./logs/")
        if not os.path.exists(self.log):
            os.mkdir(self.log)


    def uploadTask(self):
        self.taskId, self.projectId = httpWebODM.createTask(self.email, self.password, self.projectName, self.taskName, self.options)


    def startTask(self):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect("altium1.aeronavics.com", username="anton", password="")

        scp=SCPClient(ssh.get_transport())

        scp.put("/home/james/Documents/chocolate_eclair/uploads/{}".format(self.id), recursive=True, remote_path="C:/Users/Public/")
        scp.put("/home/james/Documents/chocolate_eclair/logs/{}/{}".format(self.id,self.logName), remote_path="C:/Users/Public/{}_log".format(self.id))

        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command('"C:\\Program Files (x86)\\Septentrio\\GeoTagZ\\bin\\GeoTagZ.exe" -f C:\\Users\\Public\\{}_log -p C:\\Users\\Public\\{} -o C:\\Users\\Public\\{}_processed'.format(self.id,self.id,self.id))

        print(ssh_stderr.readlines())
        print(ssh_stdout.readlines())

        scp.get("C:/Users/Public/{}_processed".format(self.id), recursive=True, local_path="/home/james/Documents/chocolate_eclair/uploads/")

        scp.close()

        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("rmdir /Q/S C:\\Users\\Public\\{} C:\\Users\\Public\\{}_processed".format(self.id, self.id))

        print(ssh_stderr.readlines())
        print(ssh_stdout.readlines())

        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("del /f C:\\Users\\Public\\{}_log".format(self.id))

        print(ssh_stderr.readlines())
        print(ssh_stdout.readlines())

        ssh.close()




        exifEditor.validate(self.images+"_processed/")
        for root, dirs, files in os.walk(self.images+"_processed/"):
            for f in files:
                httpWebODM.uploadImages(self.email, self.password, self.images + '_processed/' + f, self.taskId, self.projectId)
        shutil.rmtree(self.images+"_processed")
        shutil.rmtree(self.images)
        shutil.rmtree(self.log)
        httpWebODM.startTask(self.email, self.password, self.taskId, self.projectId)
