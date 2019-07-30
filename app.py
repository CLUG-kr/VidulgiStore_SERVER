from flask import Flask, url_for, render_template, request, redirect, session
from werkzeug.utils import secure_filename

import socket
import firebase
import firestorage

app = Flask(__name__)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

@app.route('/', methods=['GET', 'POST'])
def splash_page():
    if request.method == 'GET':
        return render_template('Splash.html')
    else:
        firebase.registerUser("1234", "1234")
        if session.get("logged_in"):
            return render_template("Splash.html",  session_value = True)
        else:
            return render_template('Splash.html', session_value = False)

@app.route('/main', methods=['GET', 'POST'])
def main_page():
    searchItem = request.form['itemSearch']
    if len(searchItem) != 0:
        items = firebase.itemSearch(searchItem)
        print(items)
        return render_template("main.html", items = items)
    else :
        return render_template("main.html", items=[])


@app.route('/login', methods=['GET', 'POST'])
def login_page():
        if request.method == 'GET':
            return render_template('login.html')
        else:
            name = request.form['input_id']
            passw = request.form['input_pw']
            if firebase.getUser(name,passw):
                session['logged_in'] = True
                return redirect(url_for('splash_page'), code=307)
            else :
                return "not login"
        return "test"

@app.route('/itemDetail', methods=['GET', 'POST'])
def itemDetail_page():
    return render_template('itemShow.html', itemPrice = " 100,000원")

@app.route('/itemUpload', methods=['GET', 'POST'])
def itemUpload_page():
    if request.method == 'GET':
        return render_template('ItemUpload.html')
    else :
        return render_template('ItemUpload.html')

@app.route('/itemUploadCom', methods=['GET', 'POST'])
def itemUploadCom_page():
    if request.method == 'POST':
        itemName = request.form['itemName']
        itemPrice = request.form['itemPrice']
        itemLocation = request.form['itemLocation']
        itemSeller = request.form['itemSeller']
        itemPhoto = request.files['itemPhoto']
        itemDetail = request.form['itemDetail']

        itemPhoto.save(secure_filename(itemSeller+itemName+'.png'))
        firestorage.uploadFile(itemSeller+itemName+'.png')
        firebase.uploadItem(itemName, itemPrice, itemLocation, itemSeller, itemDetail, itemSeller+itemName+'.png')

        return redirect(url_for('splash_page'), code=307)

if __name__ == '__main__':
    IP = str(socket.gethostbyname(socket.gethostname()))
    app.run(host=IP, port=5010, debug=False)
    app.run()
