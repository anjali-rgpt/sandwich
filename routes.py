from flask import Flask,request,render_template,redirect,url_for
from flask_mysqldb import MySQL
import re
app=Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'admin'
app.config['MYSQL_DB'] = 'SANDWICHSTORE'
app.config['MYSQL_PORT'] = 3307

mysql = MySQL(app)

regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'

current_user=""
customer_id=0


@app.route('/')
def homepage():
    return render_template('indexpage.html')

@app.route('/registercustomer')
def registercustomer():
    return render_template('customer_registration.html')

@app.route('/register', methods=['POST','GET'])
def registration():
    if request.method=='POST':
        result=request.form
        if result['firstname'] == "" or result['lastname']=="" or result['pass'] == "" or result['phone']=="" or result['email'] == "" or result['street']=="" or result['addline2'] == "" or result['city']=="" or result['region'] == "" or result['zipcode']=="":
            return render_template('invalidcred.html',error="nullspace")
        
        elif not result['firstname'].isalpha() or not result['lastname'].isalpha():
            return render_template('invalidcred.html', error="alpha")

        elif len(result['phone'])>10 or not result['phone'].isdigit():
            return render_template('invalidcred.html', error="phone")

        elif not re.search(regex,result['email']): 
            return render_template('invalidcred.html', error="email")

        else:
            cur=mysql.connection.cursor()
            cur.execute('SELECT MAX(CID) FROM USERID;')
            rec=cur.fetchall()
            print(rec)
            if rec[0][0]==None:
                customer_id=0
            else:
                customer_id=rec[0][0]+1
            print(customer_id,result['firstname'], result['lastname'],result['email'],result['phone'],result['pass'])
            cur.execute('INSERT INTO USERID VALUES (%s,%s,%s,%s,%s,%s);',(int(customer_id),result['firstname'], result['lastname'],result['email'],int(result['phone']),result['pass']))
            print(int(customer_id),result['street'], result['addline2'],result['city'],result['region'],int(result['zipcode']),int(result['phone']))
            cur.execute('INSERT INTO ADDRESS VALUES (%s,%s,%s,%s,%s,%s,%s);',(int(customer_id),result['street'], result['addline2'],result['city'],result['region'],int(result['zipcode']),int(result['phone'])))
            mysql.connection.commit()
            return render_template('customerorder.html')
        
    

if __name__=='__main__':
    app.run(debug=True,port=8081)