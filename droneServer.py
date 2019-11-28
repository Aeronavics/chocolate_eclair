from flask import Flask, request, jsonify
from taskModel import TaskModel
import os
from werkzeug import secure_filename
import shutil
import pickle

app = Flask(__name__) 


@app.route('/task', methods=['POST'])
def createTask():
    email = request.form['email']
    password = request.form['password']
    projectName = request.form.get('projectName')
    options = request.form.get('options')
    task = TaskModel(email, password, projectName, options)
    taskDict[int(task.id)] = task
    saveTasks()
    return jsonify({'id': task.id})

@app.route('/task/<int:task_id>', methods=['POST'])
def uploadImages(task_id):
    task = taskDict.get(task_id)
    images = request.files.getlist('images')
    for file in images:
        file.save(os.path.join(task.images, secure_filename(file.filename)))
    saveTasks()
    return jsonify({'totalImages': len([name for name in os.listdir(task.images) if os.path.isfile(os.path.join(task.images, name))])})

@app.route('/task/<int:task_id>/start', methods=['POST'])
def startTask(task_id):
    task = taskDict.get(task_id)
    tid = task.uploadTask()
    shutil.rmtree(task.images)
    taskDict.pop(task_id)
    saveTasks()
    return jsonify({'WebODMTaskID': tid})

def loadTasks():
    try:
        with open("bin.dat", "rb") as f:
            taskDict = pickle.load(f)
    except:
        taskDict = {}
    return taskDict

def saveTasks():
    with open("bin.dat", "wb") as f:
        pickle.dump(taskDict, f)

taskDict = loadTasks()

if __name__ == "__main__":
    taskDict = loadTasks()
    app.run(port=5000)
