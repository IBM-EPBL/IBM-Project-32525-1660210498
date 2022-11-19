from flask import Flask,render_template,request,redirect,url_for,session
import ibm_db
import re
app = Flask(__name__)

app.secret_key='a'


conn= ibm_db.connect("DATABASE=bludb;HOSTNAME=3883e7e4-18f5-4afe-be8c-fa31c41761d2.bs2io90l08kqb1od8lcg.databases.appdomain.cloud;PORT=31498;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=mqz42299;PWD=InoOxBEJEOI5nejY",'','')

@app.route('/')
def home():
    return render_template('register.html')
    
@app.route('/login',methods=['GET','POST'])
def login():
    global userid
    msg= ''
    if request.method == 'POST' :
        email = request.form['email']
        pswd = request.form['pwd']
        sql = "SELECT * FROM user WHERE email=? AND password=?"
        stmt = ibm_db.prepare(conn,sql)
        ibm_db.bind_param(stmt,1,email)
        ibm_db.bind_param(stmt,2,pswd)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        print(account)
        if account:
            session['loggedin'] = True
            session['id'] =account['EMAIL']
            userid=  account['EMAIL']
            session['email'] =account['EMAIL']
            msg = 'Logged in successfully !'
            return render_template('dashboard.html',msg=msg)
        else:
            msg='Incorrect email/pswd !'
    return render_template('login.html',msg=msg)
    
@app.route('/register', methods =['GET','POST'])
def register():
    msg = ''
    if request.method == 'POST' :
        firstname = request.form['First name']
        lastname = request.form['Last name']
        email = request.form['email']
        pswd = request.form['pwd']
        confirmpassword = request.form['Confirm password']
        gender = request.form['Gender']
        phonenumber = request.form['Phone number']
        address = request.form['Address']
        postalcode = request.form['Postal code']
        sql = "SELECT * FROM user WHERE email=?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt,1,email)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        print(account)
        if account:
            msg = 'Account already exists !'
        else:
            insert_sql = "INSERT INTO user VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"
            prep_stmt = ibm_db.prepare(conn, insert_sql)
            ibm_db.bind_param(prep_stmt, 1, firstname)
            ibm_db.bind_param(prep_stmt, 2, lastname)
            ibm_db.bind_param(prep_stmt, 3, pswd)
            ibm_db.bind_param(prep_stmt, 4, confirmpassword)
            ibm_db.bind_param(prep_stmt, 5, gender)
            ibm_db.bind_param(prep_stmt, 6, phonenumber)
            ibm_db.bind_param(prep_stmt, 7, address)
            ibm_db.bind_param(prep_stmt, 8, postalcode)
            ibm_db.bind_param(prep_stmt, 9, email)
            ibm_db.execute(prep_stmt)
            msg = 'You have successfully registered !'
            return render_template('login.html')
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('register.html', msg = msg)
    

@app.route('/dashboard')
def dash():
    return render_template('dashboard.html')
    
@app.route('/logout')
def logout():
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('email', None)
   return render_template('login.html')  
    
if __name__ == "__main__":
    app.run(debug=True)