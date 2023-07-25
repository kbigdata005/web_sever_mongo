from flask import Flask ,render_template , request ,session, redirect ,jsonify
from models import MyMongo
from config import MONGODB_URL
from functools import wraps
from bson.json_util import dumps
from bson.objectid import ObjectId

app = Flask(__name__)
app.secret_key = "a"
mymongo = MyMongo(MONGODB_URL, 'os')

def is_loged_in(func):
    @wraps(func)
    def wrap(*args , **kwargs):
        if 'is_loged' in session:
            return func(*args , **kwargs)
        else:
            return redirect('/login')
    return wrap

def is_admin(f):
    @wraps(f)
    def wrap(*args , **kwargs):
        if session['username'] == "admin":
            return f(*args , **kwargs)
        else:
            return redirect('/login')
    return wrap

@app.route('/', methods=['GET','POST'])
def main():
    return render_template('index.html')

@app.route('/admin', methods=['GET', 'POST'])
@is_loged_in
@is_admin
def admin():
    return render_template('admin.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method =="POST":
        username = request.form['username']
        email = request.form['email']
        phone = request.form['phone']
        password = request.form['password']
        user = mymongo.find_user(email)
        if user:            
            return redirect('/register')
        else:
            if username =="admin":
                return redirect('/register')
            # print(type(password))
            else:      
                result =  mymongo.user_insert(username,email,phone,password)
                return redirect('/login')
        
    elif request.method =="GET":
        return render_template('register.html')


@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    
    elif request.method == 'POST':
        email = request.form['email']
        print(email)
        password = request.form['password']
        result=mymongo.verify_password(password, email)
        user = mymongo.find_user(email)
        # print(f'fwefwfwef{user}')
        if result =="1":
            session['is_loged'] = True
            session['username'] = user['username']
            return render_template('index.html', message=user)
        elif result =="2":
            return render_template("login.html", message="Wrong")
        elif result =='3':
            return render_template("register.html" , message='None')

@app.route('/create', methods=['GET','POST'])
@is_loged_in
def create():  
    if request.method == 'GET':
        return render_template('create.html')
    else:
        title = request.form['title']
        desc = request.form['desc']  
        author = request.form['author']
        # print(author) 
        # return 'a'    
        result = mymongo.insert_data(title,desc,author) 
        return redirect('/list')  
          
@app.route('/list')
def list():
    data = mymongo.find_data()
    # for i in data:
    #     print(i)
    return render_template('list.html' , data = data)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/delete/<ids>')
def delete(ids):
    mymongo.delete_data(ids)
    return redirect('/list')

@app.route('/edit/<ids>' , methods=['GET', "POST"])
def edit_list(ids):
    if request.method == "GET":
        data = mymongo.find_one_data(ids)
        # print(data)
        return render_template('edit.html', data=data)
    elif request.method =="POST":
        title = request.form['title']
        desc = request.form.get('desc')
        mymongo.update_data( ids , title, desc)
        return redirect('/list')

if __name__== "__main__":
    app.run(debug=True, port=9999)