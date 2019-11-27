from flask import Flask, request, jsonify
from taskModel import TaskModel
import os
from werkzeug import secure_filename
import shutil

app = Flask(__name__) 

taskDict = {}

@app.route('/task', methods=['POST'])
def createTask():
    email = request.form['email']
    password = request.form['password']
    projectName = request.form.get('projectName')
    task = TaskModel(email, password, projectName)
    taskDict[int(task.id)] = task
    return jsonify({'id': task.id})

@app.route('/task/<int:task_id>', methods=['POST'])
def uploadImages(task_id):
    task = taskDict.get(task_id)
    images = request.files.getlist('images')
    for file in images:
        file.save(os.path.join(task.images, secure_filename(file.filename)))
    return jsonify({'totalImages': len([name for name in os.listdir(task.images) if os.path.isfile(os.path.join(task.images, name))])})

@app.route('/task/<int:task_id>/start', methods=['POST'])
def startTask(task_id):
    task = taskDict.get(task_id)
    tid = task.uploadTask()
    shutil.rmtree(task.images)
    taskDict.pop(task_id)
    return jsonify({'WebODMTaskID': tid})

if __name__ == '__main__':
    app.run(port=5000)
