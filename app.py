from flask import Flask, url_for, render_template, request, redirect, session
from werkzeug.utils import secure_filename
from sendNoti import send_fcm

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
    if 'itemSearch' in request.form:
        searchItem = request.form['itemSearch']
    else :
        searchItem = "아이패드"
    if len(searchItem) != 0:
        items = firebase.itemSearch(searchItem)
        print(items)
        return render_template("main.html", items = items, searchItem = searchItem)
    else :
        return render_template("main.html", items=[])

@app.route('/showItem', methods=['GET', 'POST'])
def itemShow_page():
    item = request.form['itemName']
    user = request.form['itemAuthor']
    getItem = firebase.getItem(item, user)
    return render_template('itemShow.html', items = getItem)


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

@app.route('/logout', methods=['GET', 'POST'])
def logout_page():
        session['logged_in'] = False
        return redirect(url_for('splash_page'), code=307)

@app.route('/buyItem', methods=['GET', 'POST'])
def buyItem_page():
    item = request.form['itemName']
    user = request.form['itemAuthor']
    getItem = firebase.getItem(item, user)
    return render_template('buyItem.html',items = getItem, deliveryPrice=2500, fees=500)

@app.route('/successPay', methods=['GET', 'POST'])
def successPay_page():
    buyerName = request.form['buyerName']
    buyerNumber = request.form['buyerNumber']
    itemName = request.form['itemName']
    itemAuthor = request.form['itemAuthor']
    getItem = firebase.getItem(itemName, itemAuthor)
    send_fcm(buyerName, itemName, buyerNumber)
    return render_template('paySuccess.html',seller= itemAuthor, buyer = buyerName, buyItem = itemName)

@app.route('/itemUpload', methods=['GET', 'POST'])
def itemUpload_page():
    if session.get("logged_in"):
        if request.method == 'GET':
            return render_template('ItemUpload.html')
        else :
            return render_template('ItemUpload.html')
    else :
        return "로그인 먼저 해주세요."

@app.route('/itemUploadCom', methods=['GET', 'POST'])
def itemUploadCom_page():
    if request.method == 'POST':
        itemName = request.form['itemName']
        itemPrice = request.form['itemPrice']
        itemLocation = request.form['itemLocation']
        itemSeller = request.form['itemSeller']
        itemPhoto = request.files['itemPhoto']
        itemDetail = request.form['itemDetail']

        print(itemName)
        print("test")
        fileName = itemSeller+str(hash(itemName))+'.png'
        itemPhoto.save(secure_filename(fileName))

        firestorage.uploadFile(fileName)
        firebase.uploadItem(itemName, itemPrice, itemLocation, itemSeller, itemDetail, fileName)

        return redirect(url_for('splash_page'), code=307)

if __name__ == '__main__':
    IP = str(socket.gethostbyname(socket.gethostname()))
    app.run(host=IP, port=5010, debug=False)
    app.run()
