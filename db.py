import psycopg2
import docker

def connect():
    client = docker.from_env()
    container = client.containers.get("db")
    try:
        connection = psycopg2.connect(user = "postgres",
            password = "postgres",
            host = "127.0.0.1",
            port = container.ports['5432/tcp'][0]['HostPort'],
            database = "webodm_dev")
        return  connection.cursor()
    except (Exception, psycopg2.Error) as error:
        print ("Error while connecting to PostgreSQL: " + error)
        return


def getProjectFromEmail(email):
    cursor = connect()
    if (cursor):
        try:
            cursor.execute("select t.id from (select distinct app_project.id, app_project.created_at, row_number() over(order by app_project.created_at desc) as rn from app_projectuserobjectpermission join auth_user on app_projectuserobjectpermission.user_id=auth_user.id join app_project on app_project.id=app_projectuserobjectpermission.content_object_id where auth_user.email='" + email + "')t where t.rn =1;")
            record = cursor.fetchone()
            if (not record):
                print("No projects found")
                return
            else:
                return record[0]
        except (Exception, psycopg2.Error) as error:
            print("Error: " + error)

def getUsernameFromEmail(email):
    cursor = connect()
    if (cursor):
        try:
            cursor.execute("select username from auth_user where email='" + email + "';")
            record = cursor.fetchone()
            if (not record):
                print("No user found")
                return
            else:
                return record[0]
        except (Exception, psycopg2.Error) as error:
            print("Error: " + error)
            return


def getTaskStatus(taskID):
    cursor = connect()
    if (cursor):
        try:
            cursor.execute("select status from app_task where id='" + taskID + "';")
            record = cursor.fetchone()
            if (not record):
                print("No task found")
                return
            else:
                return record[0]
        except (Exception, psycopg2.Error) as error:
            print("Error: " + error)
            return

def getProjectFromTask(taskId):
    cursor = connect()
    if (cursor):
        try:
            cursor.execute("select project_id from app_task where id='" + taskId + "'")
            record = cursor.fetchone()
            if (not record):
                print("No task found")
                return
            else:
                return record[0]
        except (Exception, psycopg2.Error) as error:
            print("Error: " + error)
            return

def getAllRunningTasks():
    cursor = connect()
    if (cursor):
        try:
            cursor.execute("select id from app_task where status=20")
            record = cursor.fetchall()
            if (not record):
                return []
            else:
                taskList = []
                for item in record:
                    taskList.append(item[0])
                return taskList
        except (Exception, psycopg2.Error) as error:
            print("Error: " + error)
            return []

def getEmailFromTask(taskId):
    cursor = connect()
    if cursor:
        try:
            cursor.execute("select distinct email from auth_user join app_projectuserobjectpermission on auth_user.id=app_projectuserobjectpermission.user_id join app_task on app_projectuserobjectpermission.content_object_id=app_task.project_id where app_task.id='"+taskId+"'")
            record = cursor.fetchone()
            if not record:
                return
            else:
                return record[0]
        except (Exception,psycopg2.Error) as error:
            print("Error: " + error)
            return
