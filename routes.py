import os
import time
import models
from typing import Union
from werkzeug.security import generate_password_hash, check_password_hash
from models import student_valid_login,teacher_valid_login,visitor_register,visitor_valid_login,Thecode_valid,search_blog,blog_register
from flask import render_template, request, url_for, redirect, session, send_from_directory, Config
from forms import RegistrationForm
from io import BytesIO
import random
import string
import pymysql
from __init__ import app
from flask.json import jsonify
from flask.helpers import flash


UPLOAD_FOLDER = 'data/coursesource/20180201001/0101002/student-homework/hw1'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER  # 设置文件上传的目标文件夹
basedir: Union[bytes, str] = os.path.abspath(os.path.dirname(__file__))  # 获取当前项目的绝对路径
ALLOWED_EXTENSIONS = set(['txt', 'ppt', 'jpg', 'xls', 'JPG', 'PNG', 'xlsx', 'gif', 'pdf','PDF'])

UPLOAD_SLIDES_FOLDER = 'data/coursesource/20180201001/0101002/PPT'
UPLOAD_HW_FOLDER = 'data/coursesource/20180201001/0101002/homework'
app.config['UPLOAD_SLIDES_FOLDER'] = UPLOAD_SLIDES_FOLDER
app.config['UPLOAD_HW_FOLDER'] = UPLOAD_HW_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/', methods=['POST','GET'])
@app.route('/index', methods=['POST','GET'])
def index():
    if request.method == "GET":
        form=request.form
        form_register = RegistrationForm()    
        number=random.randint(1, 20) 
        if os.path.isfile ("./static/images/thecode/"+str(number)+".jpg"):
            Path = "../static/images/thecode/"+str(number)+".jpg"
        else:
            Path = "../static/images/thecode/"+str(number)+".png"
        session['number']=str(number)
        return render_template("index.html", form=form,form_register=form_register,Path=Path)
    else:
        form=request.form
        username = request.form.get('loginName')
        password = request.form.get('loginPassword')
        code = request.form.get('thecode')
        session['username'] = username
        select=request.form.get('type_select')
        if(select):
            if(Thecode_valid(session['number'],code)):
                if(select=='student'):   #这里要通过索引来转
                    if(username==''):
                        flash(u'学号不能为空！','danger')
                        return redirect(url_for('index'))
                    if(password==''):
                        flash(u'密码不能为空！','danger')
                        return redirect(url_for('index'))
                    if(student_valid_login(username,password)):   #添加错误处理 以及验证码
                        return redirect(url_for('student'))
                    else:
                        flash(u'学号密码不匹配！','danger')
                if(select=='teacher'):  #这里要通过索引来转
                    if(username==''):
                        flash(u'学工号不能为空！','danger')
                        return redirect(url_for('index'))
                    if(password==''):
                        flash(u'密码不能为空！','danger')
                        return redirect(url_for('index'))
                    if(teacher_valid_login(username,password)): 
                        return redirect(url_for('teacher'))
                    else:
                        flash(u'学工号密码不匹配！','danger')
                if (select == 'TA'):  # 这里要通过索引来转
                    if (username == ''):
                        flash(u'学工号不能为空！', 'danger')
                        return redirect(url_for('index'))
                    if (password == ''):
                        flash(u'密码不能为空！', 'danger')
                        return redirect(url_for('index'))
                    if (teacher_valid_login(username, password) and username == '20180201001'):
                        return redirect(url_for('TA'))
                    else:
                        flash(u'学工号密码不匹配！', 'danger')
                if(select=='tourist'):  #这里要通过索引来转
                    if(username==''):
                        flash(u'用户名不能为空！','danger')
                        return redirect(url_for('index'))
                    if(password==''):
                        flash(u'密码不能为空！','danger')
                        return redirect(url_for('index'))
                    if(visitor_valid_login(username,password)): 
                        return redirect(url_for('visitor'))
                    else:
                        flash(u'用户名密码不匹配！','danger')
            else:
                flash(u'验证码错误！','danger')
        else:
            #if valid
            username = request.form.get('signupName')
            password = request.form.get('signupPassword')
            email = request.form.get('signupEmail')
            phone = request.form.get('signupPhone')
            visitor_register(username,password,email,phone)    
            return redirect(url_for('index'))
        return redirect(url_for('index'))

    #写其他页面的函数
    # 
@app.route('/logout',methods=['POST', "GET"])
def logout():
    session.pop('username', None)
    session.pop('type', None)
    return redirect(url_for('index'))


@app.route('/student', methods=['POST', 'GET'])
def student():
    if request.method == "GET":
        print(session['username'])
        stu_ID = session['username']
        stu_data = models.search_student(stu_ID)
        print(stu_data)
        stu_course = stu_data[10]
        session['course_id1'] = stu_course[0:7]
        session['course_id2'] = stu_course[8:15]
        session['course_id3'] = stu_course[16:23]
        #session['course_id'] = stu_data[10]
        #print(session['course_id3'])
        ID_1 = session['course_id1']
        ID_2 = session['course_id2']
        ID_3 = session['course_id3']
        course_data_1 = models.search_course(ID_1)
        course_data_2 = models.search_course(ID_2)
        course_data_3 = models.search_course(ID_3)
        homework_data_1 = models.search_homework(ID_1, "1")
        homework_data_2 = models.search_homework(ID_2, "1")
        homework_data_3 = models.search_homework(ID_3, "1")
    return render_template('student_home.html', course_data_1=course_data_1, course_data_2=course_data_2, course_data_3=course_data_3, homework_data_1=homework_data_1, homework_data_2=homework_data_2, homework_data_3=homework_data_3)

@app.route('/student/information', methods=['POST', 'GET'])
def student_information():
    if request.method == "GET":
        ID_1 = session['course_id1']
        ID_2 = session['course_id2']
        ID_3 = session['course_id3']
        course_data_1 = models.search_course(ID_1)
        course_data_2 = models.search_course(ID_2)
        course_data_3 = models.search_course(ID_3)
        return render_template('student_information.html',course_data_1=course_data_1, course_data_2=course_data_2, course_data_3=course_data_3)

@app.route('/studentcourses', methods=['POST', 'GET'])
def allcourses():
    if request.method == "GET":
        return render_template('allcourses.html')

@app.route('/studenthomework', methods=['POST', 'GET'])
def allhomework():
    if request.method == "GET":
        ID_1 = session['course_id1']
        ID_2 = session['course_id2']
        ID_3 = session['course_id3']
        course_data_1 = models.search_course(ID_1)
        course_data_2 = models.search_course(ID_2)
        course_data_3 = models.search_course(ID_3)
        homework_data_1 = models.search_homework(ID_1, "1")
        homework_data_2 = models.search_homework(ID_2, "1")
        homework_data_3 = models.search_homework(ID_3, "1")
        return render_template('student_allhomework.html',course_data_1=course_data_1, course_data_2=course_data_2, course_data_3=course_data_3,homework_data_1=homework_data_1, homework_data_2=homework_data_2, homework_data_3=homework_data_3)

@app.route('/course/download', methods=['POST', 'GET'])
def course_download():
    return render_template('course_download.html')

@app.route('/blog', methods=['POST', 'GET'])
def blog():
    if request.method == "GET":
        return render_template('student_blog.html')

#留言板功能
@app.route('/blogdetails', methods=['POST', 'GET'])
def blogdetail():
    if request.method == "POST":
        form = request.form
        comment = request.form.get('comment')
        ID = session['username']
        student = models.search_student(ID)
        name = student[2]
        models.blog_register("Board_Public", name, comment)
    blog_name_1 = blog_name_2 = blog_name_3 = None
    blog_content_1 = blog_content_2 = blog_content_3 = None
    courses = models.search_blog("Board_Public", '1')
    if not (courses == None):
        blog_name_1 = courses[0]
        blog_content_1 = courses[1]
        flash("1", "1")
    courses = models.search_blog("Board_Public", '2')
    if not (courses == None):
        blog_name_2 = courses[0]
        blog_content_2 = courses[1]
        flash("1", "2")
    courses = models.search_blog("Board_Public", '3')
    if not (courses == None):
        blog_name_3 = courses[0]
        blog_content_3 = courses[1]
        flash("1", "3")

    if request.method == "GET":
        return render_template('message_board.html', name_1=blog_name_1, name_2=blog_name_2, name_3=blog_name_3
                           ,content_1=blog_content_1,content_2=blog_content_2,content_3=blog_content_3)
    else:
        return render_template('message_board.html', name_1=blog_name_1, name_2=blog_name_2, name_3=blog_name_3
                               , content_1=blog_content_1, content_2=blog_content_2, content_3=blog_content_3)


@app.route('/notice', methods=['POST', 'GET'])
def notice():
    if request.method == "GET":
        return render_template('student_notice.html')


@app.route('/download', methods=['POST', 'GET'])
def download():
    filename = '1.pptx'
    if os.path.isfile(os.path.join('data/coursesource/20180201001/0101002/PPT', filename)):
        return send_from_directory('data/coursesource/20180201001/0101002/PPT', filename, as_attachment=True)


@app.route('/student/homework', methods=['POST', 'GET'])
def student_homework():
    if request.method == "GET":
        courseid = session['course_id']
        number = "1"
        data = models.search_homework(courseid, number)
    return render_template('student_homework.html', Str = data)

@app.route('/api/upload', methods=['POST'], strict_slashes=False)
def api_upload():
    file_dir = os.path.join(basedir, app.config['UPLOAD_FOLDER'])  # 拼接成合法文件夹地址
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)  # 文件夹不存在就创建
    f=request.files['myfile']  # 从表单的file字段获取文件，myfile为该表单的name值
    if f and allowed_file(f.filename):  # 判断是否是允许上传的文件类型
        fname=f.filename
        ext = fname.rsplit('.', 1)[1]  # 获取文件后缀
        unix_time = int(time.time())
        new_filename = str(unix_time)+'.'+ext   # 修改文件名
        f.save(os.path.join(file_dir, new_filename))  #保存文件到upload目录
        #ID = session['course_id1']
        #data = models.search_course(ID)
        session['course_id'] = session['course_id1']
        print(session['course_id'])
        ID = session['course_id']
        data = models.search_course(ID)
        homework = models.search_homework(ID, "1")
        return render_template('student_course.html', Str=data, homework=homework)


@app.route('/api/find_course_1', methods=['POST'], strict_slashes=False)
def api_find_course_1():
    session['course_id'] = session['course_id1']
    print(session['course_id'])
    ID = session['course_id']
    data = models.search_course(ID)
    homework = models.search_homework(ID, "1")
    # Str = data['CourseName']
    # print(Str)
    # file = '1.jpg'
    # download(file)
    return render_template('student_course.html', Str=data, homework=homework)

@app.route('/api/find_course_2', methods=['POST'], strict_slashes=False)
def api_find_course_2():
    session['course_id'] = session['course_id2']
    print(session['course_id'])
    ID = session['course_id']
    data = models.search_course(ID)
    homework = models.search_homework(ID, "1")
    # Str = data['CourseName']
    # print(Str)
    # file = '1.jpg'
    # download(file)
    return render_template('student_course.html', Str=data, homework=homework)

@app.route('/api/find_course_3', methods=['POST'], strict_slashes=False)
def api_find_course_3():
    session['course_id'] = session['course_id3']
    print(session['course_id'])
    ID = session['course_id']
    data = models.search_course(ID)
    homework = models.search_homework(ID, "1")
    # Str = data['CourseName']
    # print(Str)
    # file = '1.jpg'
    # download(file)
    return render_template('student_course.html', Str=data, homework=homework)

@app.route('/api/find_homework_1', methods=['POST'], strict_slashes=False)
def api_find_homework_1():
    courseid = session['course_id1']
    number = "1"
    data = models.search_homework(courseid, number)
    return render_template('student_homework.html', Str=data)

@app.route('/api/find_homework_2', methods=['POST'], strict_slashes=False)
def api_find_homework_2():
    courseid = session['course_id2']
    number = "1"
    data = models.search_homework(courseid, number)
    return render_template('student_homework.html', Str=data)

@app.route('/api/find_homework_3', methods=['POST'], strict_slashes=False)
def api_find_homework_3():
    courseid = session['course_id3']
    number = "1"
    data = models.search_homework(courseid, number)
    return render_template('student_homework.html', Str=data)

@app.route('/teacher', methods=['POST', 'GET'])
def teacher():
    if request.method == "GET":
        print(session['username'])
        teacher_ID = session['username']
        courses = models.search_course_teacher(teacher_ID)
        courses_ID = models.search_course_ID_teacher(teacher_ID)
        session['course_id1'] = courses_ID[0][0]
        session['course_id2'] = courses_ID[1][0]
        session['course_id3'] = courses_ID[2][0]
        print(session['course_id3'])
        ID_1 = session['course_id1']
        ID_2 = session['course_id2']
        ID_3 = session['course_id3']
        course_data_1 = courses[0][0]
        course_data_2 = courses[1][0]
        course_data_3 = courses[2][0]
    return render_template('teacher-courses.html', course_name_1=course_data_1, course_name_2=course_data_2, course_name_3=course_data_3)


@app.route('/api/upload_hw', methods=['POST'], strict_slashes=False)
def api_upload_hw():
    ID = session['course_id']
    data = models.search_course(ID)
    homework = models.search_homework(ID, "1")
    # homework[5] = 'Red-Black Trees'
    file_dir = os.path.join(basedir, app.config['UPLOAD_HW_FOLDER'])  # 拼接成合法文件夹地址
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)  # 文件夹不存在就创建
    f = request.files['myfile']  # 从表单的file字段获取文件，myfile为该表单的name值
    if f and allowed_file(f.filename):  # 判断是否是允许上传的文件类型
        f.save(os.path.join(file_dir, f.filename))   # 保存文件到upload目录
        return render_template('course-single.html', Str=data, homework=homework)


@app.route('/api/upload_slides', methods=['POST'], strict_slashes=False)
def api_upload_slides():
    ID = session['course_id']
    data = models.search_course(ID)
    homework = models.search_homework(ID, "1")
    # homework[5] = 'Red-Black Trees'
    file_dir = os.path.join(basedir, app.config['UPLOAD_SLIDES_FOLDER'])  # 拼接成合法文件夹地址
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)  # 文件夹不存在就创建
    f = request.files['myfile']  # 从表单的file字段获取文件，myfile为该表单的name值
    if f and allowed_file(f.filename):  # 判断是否是允许上传的文件类型
        f.save(os.path.join(file_dir, f.filename))   # 保存文件到upload目录
        return render_template('course-single.html', Str=data, homework=homework)


@app.route('/visitor',methods=['POST', "GET"])
def visitor():
    return render_template('visitor_home.html')

@app.route('/allcourses',methods=['POST', "GET"])
def visitor_courses():
    return render_template('visitor_courses.html')

@app.route('/visitor/collection',methods=['POST', "GET"])
def visitor_collection():
    return render_template('visitor_collection.html')

@app.route('/api/tfind_course_1', methods=['POST'], strict_slashes=False)
def api_tfind_course_1():
    session['course_id'] = session['course_id1']
    ID = session['course_id']
    data = models.search_course(ID)
    homework = models.search_homework(ID, "1")
    return render_template('course-single.html', Str=data, homework=homework)


@app.route('/api/tfind_course_2', methods=['POST'], strict_slashes=False)
def api_tfind_course_2():
    session['course_id'] = session['course_id2']
    ID = session['course_id']
    data = models.search_course(ID)
    homework = models.search_homework(ID, "1")
    return render_template('course-single.html', Str=data, homework=homework)


@app.route('/api/tfind_course_3', methods=['POST'], strict_slashes=False)
def api_tfind_course_3():
    session['course_id'] = session['course_id3']
    ID = session['course_id']
    data = models.search_course(ID)
    homework = models.search_homework(ID, "1")
    return render_template('course-single.html', Str=data, homework=homework)

@app.route('/homework/detail', methods=['POST', 'GET'])
def homework_detail():
    return render_template('homework-detail.html')


@app.route('/teacher/information', methods=['POST', 'GET'])
def teacher_information():
    if request.method == "GET":
        ID_1 = session['course_id1']
        ID_2 = session['course_id2']
        ID_3 = session['course_id3']
        course_data_1 = models.search_course(ID_1)
        course_data_2 = models.search_course(ID_2)
        course_data_3 = models.search_course(ID_3)
        return render_template('teacher-information.html',course_data_1=course_data_1, course_data_2=course_data_2, course_data_3=course_data_3)


@app.route('/teacher/download', methods=['POST', 'GET'])
def teacher_download():
    filename = '1.zip'
    if os.path.isfile(os.path.join('data', filename)):
        return send_from_directory('data', filename, as_attachment=True)

@app.route('/teacher/create_hw', methods=['POST', 'GET'])
def create_hw():
    return render_template("create-homework.html")


@app.route('/teacher/add_radio', methods=['POST', 'GET'])
def add_radio():
    return render_template("add-radio.html")

@app.route('/teacher/ppt_up', methods=['POST', 'GET'])
def ppt_up():
    return render_template("ppt-up.html")

@app.route('/student/test_answer', methods=['POST', 'GET'])
def test_answer():
    return render_template("test-answer.html")

@app.route('/student/testr', methods=['POST', 'GET'])
def test():
    return render_template("test-no.html")


@app.route('/index/message_board', methods=['GET'])
def blog_index():
    return render_template('message_board_index.html')


@app.route('/teacher_assistance', methods=['POST', 'GET'])
def TA():
    if request.method == "GET":
        print(session['username'])
        TA_ID = session['username']
        courses = models.search_course_teacher(TA_ID)
        courses_ID = models.search_course_ID_teacher(TA_ID)
        session['course_id1'] = courses_ID[0][0]
        course_data_1 = courses[0][0]
    return render_template('teacher-assistance.html', course_name_1=course_data_1)

@app.route('/findpassword', methods=['POST', 'GET'])
def findpswd():
    return render_template('findpwd.html')

if __name__ == '__main__':
    app.run()
    