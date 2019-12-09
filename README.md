# Chocolate Eclair
This repository contains the intermediate server used for communicating between WebODM and QGroundControl during automated mapping, as well as the email notification handler.

## Intermediate Server
The intermediate server is made of six Python files which are:

- db.py
- droneServer.py
- exifEditor.py
- httWebODM.py
- taskModel.py
- wsgi.py

### db.py
db.py is used to interact with WebODM's Postgris database which is stored in a docker container. This is used to get information that is not easily accessible through WebODM's http api, such as email addresses and which projects users have access to.

### droneServer.py
This is a flask http server which is used to communicate with QGroundControl. The end points available are:

 - ' / ' This is a post request which takes a users WebODM email and password to log in to WebODM.
 - ' /presets ' This is get request to get all of the proccessing presets from WebODM.
 - ' /task ' This is a post request to create a new task. Email and password are required and projectName, taskName and options are optional.
 - ' /task/<int:task_id> ' This is a post request to add one or more images to a specified task. 
 - '/task/<int:task_id>/start' This is a post request which uploads the specified task to WebODM and starts processing it.

Tasks are store in a bin.dat file once they are created and are only removed once they have been uploaded to WebODM. this is as a form of backup if the server goes down the tasks and images will not be lost.

### exifEditor.py
This is used to sanitise the exif data of all images that are to be uploaded to WebODM to ensure that the images will in a usable format.

### httWebODM.py
httWebODM.py sends the http requests to WebODM to create and start tasks and create new projects. 

### taskModel.py
This class stores the data needed to create a task on WebODM. It contains the users email and password, the tasks project and task names, the processing options and the file path for the images of the task.

### wsgi.py
wsgi.py is used so that the flask server will not start in development mode.

## email notification handler
The file taskMonitor.py is used in conjunction with db.py to check on the processing status of all the tasks on WebODM. When a task is no longer running, it's status code is check and based on the status code a relevant email is sent to the email address associated with that task. The emails are sent from notifyEmail.py which uses smtplib to send the emails.
