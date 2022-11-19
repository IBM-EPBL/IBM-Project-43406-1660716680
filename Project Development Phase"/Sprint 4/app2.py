from flask import Flask,render_template,redirect,url_for, request,session
import ibm_db
import credentials
from flask_mail import Mail, Message


app=Flask(__name__)



#Database connection
conn = ibm_db.connect("DATABASE="+credentials.DB2_DATABASE_NAME+";HOSTNAME="+credentials.DB2_HOST_NAME+";PORT="+credentials.DB2_PORT+";SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID="+credentials.DB2_UID+";PWD="+credentials.DB2_PWD+"",'','')


# configuration of mail
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'infonutrassi@gmail.com'
app.config['MAIL_PASSWORD'] = 'mgatvwljsrucdswm'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app) # instantiate the mail class

@app.route('/send',methods=['GET','POST'])
def send():
    if request.method == "POST":
        email = request.form['email']
        msg = request.form['message']
        subject = request.form['subject']
        message= Message(subject,recipients=["infonutrassi@gmail.com"])
        message.sender = email
        message.body = msg
        mail.send(message)
        success="Message sent"
        return render_template("result.html",success=success)


#routing
@app.route('/signin')
def signin():
    return render_template('signin.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

#Nutrition finding result page
@app.route('/upload')
def upload():
    return render_template('upload image.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/index')
def index():
    return render_template('index.html')

#logout
@app.route('/logout')
def logout():
    if 'email' in session:
        session.pop('email',None)
        return redirect('/')
    return redirect('/')

#Signup page
@app.route('/postSignUpData', methods=['GET', 'POST'])
def postSignUpData():
    msg=''
    if request.method == 'POST':
        name = request.form.get("name",False)
        email = request.form.get("email",False)
        password = request.form.get("password",False)
        username = request.form.get("username",False)


        sql = "SELECT * FROM user WHERE email=?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt,1,email)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        if account:
            return render_template('signup.html', msg="You are already a member, please login using your details")
        else:
            insert_sql = "INSERT INTO user VALUES (?,?,?,?)"
            prep_stmt = ibm_db.prepare(conn, insert_sql)
            ibm_db.bind_param(prep_stmt,1, email)
            ibm_db.bind_param(prep_stmt,2, password)
            ibm_db.bind_param(prep_stmt,3, name)
            ibm_db.bind_param(prep_stmt,4, username)
            ibm_db.execute(prep_stmt)
            msg="Registration successfull.."
            return render_template('signin.html',msg=msg)


#Signin Page
@app.route('/postSignInData',methods =['POST','GET'])
def postSignInData():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        sql = "SELECT PASSWORD FROM user WHERE email=?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt,1,email)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        print(account)
        if account and account["PASSWORD"]==password:
            return render_template('index.html',email=email)
        else:
            msg="username or password is incorrect"
            return render_template('signin.html',msg=msg)

#Profile
@app.route('/profile')
def profile():
  sql = "SELECT * FROM user"
  stmt = ibm_db.exec_immediate(conn, sql)
  while ibm_db.fetch_row(stmt) != False:
    email= ibm_db.result(stmt, 0)
    name= ibm_db.result(stmt, 2)
    username= ibm_db.result(stmt, 3)
    return render_template("profile.html", name=name, email=email, username=username)



if __name__=='__main__':
    app.run(host='0.0.0.0',port=8080,debug=True)