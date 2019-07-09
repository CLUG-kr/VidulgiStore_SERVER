from flask import Flask, url_for, render_template, request, redirect, session
from werkzeug.utils import secure_filename

import firebase
from user import User
import firestorage
from item import Item
app = Flask(__name__)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

@app.route('/', methods=['GET', 'POST'])
def splash_page():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        firebase.registerUser("1234", "1234")
        if session.get("logged_in"):
            return render_template("Splash.html",  session_value = True)
        else:
            return render_template('Splash.html', session_value = False)

@app.route('/main', methods=['GET', 'POST'])
def main_page():
    searchItem = request.form['itemSearch']
    items = firebase.itemSearch(searchItem)
    print(items)
    return render_template("main.html")


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
    return render_template('ItemDetail.html')

@app.route('/itemUpload', methods=['GET', 'POST'])
def itemUpload_page():
    if request.method == 'GET':
        return render_template('ItemUpload.html')

@app.route('/itemUploadCom', methods=['GET', 'POST'])
def itemUploadCom_page():
    if request.method == 'POST':
        itemName = request.form['itemName']
        itemPrice = request.form['itemPrice']
        itemLocation = request.form['itemLocation']
        itemSeller = request.form['itemSeller']
        itemPhoto = request.files['itemPhoto'] if request.files.get('itemPhoto') else None
        itemDetail = request.form['itemDetail']
        print("1", itemName, itemPrice, itemLocation, itemSeller, itemDetail, itemPhoto)
        firebase.uploadItem("1", itemName, itemPrice, itemLocation, itemSeller, itemDetail)
        itemPhoto.save(secure_filename(itemPhoto.filename))
        """firestorage.uploadFile(itemPhoto,'upload/'+itemPhoto.filename)"""
        return redirect(url_for('main_page'), code=307)
if __name__ == '__main__':
    app.run()