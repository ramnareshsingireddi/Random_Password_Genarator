from flask import Flask,render_template,request,redirect,url_for, session
from  flask_mysqldb import MySQL
import MySQLdb.cursors
import re
app=Flask(__name__)
app.secret_key = 'your secret key'
app.config['MYSQL_HOST']='local_host'
app.config["MYSQL_USER"]="ram"
app.config['MYSQL_PASSWORD']='password'
app.config['MYSQL_DB']='geekslogin'
mysql=MySQL(app)
@app.route('/')
def home():
    return 'login or register your details'
@app.route('/login',methods=['GET','POST'])
def login():
    msg=''
    if request.method=='POST' and "USER_NAME" in request.form and 'password'in request.form:
        username=request.form["USER_NAME"]
        password=request.form["password"]
        cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.excute('SELECT * FROM accounts WHERE username =%s AND password=%s',(username,password))
        account=cursor.fetchone()
        if account: 
            session['loggedin']=True
            session['id']=account['id']
            session['user_name']=account['user_name']
            msg='you have sucessfully loggedin'
            return render_template('index.html',msg=msg)
        else:
            msg= 'incorrect user_name or password'
    return render_template('login.html',msg=msg)
@app.route('/logout')
def logout():
    session.pop('loggedin',None)
    session.pop('id',None)
    session.pop('user_name',None)
    msg='you have logged out'
    return redirect(url_for('logout'))
@app.route('/register',methods=['GET',"POST"])
def register():
    msg=''
    if request.method=="POST"and "USER_NAME" in request.form and "pasword"in request.form and 'email'in request.form:
        username=request.form['USER_NAME']
        password=request.form['password']
        email=request.form['email']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = % s',(username, ))
        account = cursor.fetchone()
        if account:
            return 'this account is already existed'
        elif not re.match(r'[A-Za-z0-9]+',username):
            msg='enter name or number'
        elif not username or not password or not email:
            msg='fill these bellow forms '
        elif not re.match(r'[^@]+@[^@]+\.[^@]+',email):
            msg='invalid email'
        else:
            cursor.execute('INSERT INTO accounts VALUES (NULL,%s,%s,%s)',(username,password,email,))
            mysql.connection.commit()
            msg='register Sucesesful'
    elif request.method=="POST":
        msg='plese fill these forms'   
    return render_template('register.html',msg=msg) 
if __name__=='__main__':
    app.run(debug=True)
    