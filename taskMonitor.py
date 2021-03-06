import db
import notifyEmail
import time


def checkStatus():
    taskDict = db.getAllRunningTasks()
    while True:
        time.sleep(2)
        taskDict2 = db.getAllRunningTasks()
        if (taskDict):
            for taskId in taskDict:
                if taskId not in taskDict2:
                    status = db.getTaskStatus(taskId)
                    if (status == 40):
                        projectId = db.getProjectFromTask(taskId)
                        email = db.getEmailFromTask(taskId)
                        if email:
                            notifyEmail.complete(email)
                    elif(status == 30):
                        projectId = db.getProjectFromTask(taskId)
                        email = db.getEmailFromTask(taskId)
                        if email:
                            notifyEmail.failure(email)
        taskDict = taskDict2

checkStatus()
