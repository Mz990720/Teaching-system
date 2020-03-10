from werkzeug.security import generate_password_hash, check_password_hash
from flaskext.mysql import MySQL
from __init__ import app
import random
from flask.helpers import flash

def Getformat(ID:str):
    conn = start_database()
    cursor = conn.cursor()  
    cursor.execute("SELECT format from Thecode where ID=\'" + ID + "\'")  
    courses = cursor.fetchall()
    print(courses)
    return courses

def Thecode_valid(ID:str,reply:str):
    conn = start_database()
    cursor = conn.cursor()
    cursor.execute("SELECT Realcode from Thecode where ID=\'" + ID + "\'")
    courses = str(cursor.fetchall())
    endStr = "',)"
    endIndex = courses.index(endStr)
    print(courses)
    print(courses[3:endIndex])
    reply = reply.lower()
    print(reply)
    if(courses[3:endIndex]==reply):
        return True
    else:
        return False
   
def start_database():
    db = MySQL()
    db.init_app(app)
    conn = db.connect()
    conn.autocommit(1)
    return conn
    
def search_course_teacher(ID:str):
    conn = start_database()
    cursor = conn.cursor()
    cursor.execute("SELECT CourseName from course where TeacherID=\'" + ID + "\'")
    courses = cursor.fetchall()
    print(courses)
    return courses


def search_course_ID_teacher(ID:str):
    conn = start_database()
    cursor = conn.cursor()
    cursor.execute("SELECT CourseID from course where TeacherID=\'" + ID + "\'")
    course_ID = cursor.fetchall()
    return course_ID

def student_valid_login(usename:str,password:str):
    conn = start_database()
    cursor = conn.cursor()
    cursor.execute("SELECT LoginPassword from student where studentid=\'" + usename +"\'")  
    data = cursor.fetchone()
    print(usename)
    print(data)
    print(password)
    if data is not None and check_password_hash(data[0],password):
        print("yes!")
        return True
    return False


def teacher_valid_login(usename:str,password:str):
    conn = start_database()
    cursor = conn.cursor()
    cursor.execute("SELECT LoginPassword from teacher where TeacherId=\'" + usename +"\'")  
    data = cursor.fetchone()
    if data is not None and check_password_hash(data[0],password):
        return True
    return False

def visitor_valid_login(usename:str,password:str):
    conn = start_database()
    cursor = conn.cursor()
    cursor.execute("SELECT LoginPassword from visitor where userName=\'" + usename +"\'")  
    data = cursor.fetchone()
    if data is not None and check_password_hash(data[0],password):
        return True
    return False


def visitor_register(username:str,password:str,email:str,phone:str):
    conn = start_database()
    cursor = conn.cursor()
    
    password=generate_password_hash(password)

    insert = "insert into Visitor(UserName,LoginPassword,Phone,Email,CourseRecord) " \
             + "values(\'" + str(username) + "\',\'" + str(password) + "\',\'" + str(email) + "\',\'" + str(phone) + "\',\'""\');"
    cursor.execute(insert)

def search_course(ID:str):
    conn = start_database()
    cursor = conn.cursor()
    cursor.execute("SELECT * from course where CourseID=\'" + ID + "\'")
    data = cursor.fetchone()
    return data

def search_student(ID:str):
    conn = start_database()
    cursor = conn.cursor()
    cursor.execute("SELECT * from student where StudentID=\'" + ID + "\'")
    stu_data = cursor.fetchone()

    return stu_data

def search_homework(courseID:str, number:str):
    conn = start_database()
    cursor = conn.cursor()
    cursor.execute("SELECT * from homework where CourseId=\'" +courseID+"\'"" and HomeworkNumber=\'" +number+ "\'")
    data = cursor.fetchone()
    return data

def search_blog(blogName:str, number:str):
    conn = start_database()
    cursor = conn.cursor()
    cursor.execute("SELECT UserName,Content from "+blogName+ " where number=\'" +number + "\'")
    data = cursor.fetchone()
    return data


def blog_register(databaseName: str,userName: str, content:str):
    conn = start_database()
    cursor = conn.cursor()
    cursor.execute("SELECT count(*) from " + databaseName )
    data = cursor.fetchone()
    number=data[0]
    insert = "insert into "+databaseName+"(UserName,Number,Content) " \
             + "values(\'" + str(userName) + "\',\'" + str(number+1) + "\',\'" + str(content)  + "\');"
    print(insert)
    cursor.execute(insert)