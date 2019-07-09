from flask import Flask, url_for, render_template, request, redirect, session
import firebase
from user import User

app = Flask(__name__)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

@app.route('/', methods=['GET', 'POST'])
def splash_page():
    if request.method == 'POST':
        searchItem = request.form['itemSearch']
    return render_template('Splash.html')

@app.route('/main', methods=['GET', 'POST'])
def main_page():
        firebase.registerUser("1234", "1234")
        if session.get("logged_in"):
            return render_template('main.html')
        else :
            return render_template('main.html')

@app.route('/login', methods=['GET', 'POST'])
def login_page():
        if request.method == 'GET':
            return render_template('login.html')
        else:
            name = request.form['input_id']
            passw = request.form['input_pw']
            if firebase.getUser(name,passw):
                session['logged_in'] = True
                return "login"
            else :
                return "not login"
        return "test"

@app.route('/itemDetail', methods=['GET', 'POST'])
def itemDetail_page():
    return render_template('ItemDetail.html')

@app.route('/itemUpload', methods=['GET', 'POST'])
def itemUpload_page():
    return render_template('ItemUpload.html')

if __name__ == '__main__':
    app.run()
