import firebase_admin
from user import User
from werkzeug.security import generate_password_hash, check_password_hash
from firebase_admin import credentials
from firebase_admin import firestore


cred = credentials.Certificate("vidulgi-firebase-adminsdk-yxed3-b7f4229719.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

def registerUser(id, pw):
    doc_ref = db.collection(u'Users').document(str(id))
    doc_ref.set({
        u'pw': generate_password_hash(pw),
    })

def getUser(id,pw):
    result = db.collection(u'Users').document(id).get().to_dict()
    print(result)
    if result != None:
        user = User(id, result["pw"])

        print(check_password_hash(result["pw"],pw))
        return check_password_hash(result["pw"],pw)
    return False

def itemSearch(searchInput):
    resultList = []

    result = db.collection(u'Items').get()
    for x in result:
        currentData = x.to_dict()
        if currentData.get('name') == searchInput:
            resultList.append(currentData)
    return resultList

def uploadItem(itemId, name, price, location, seller, detail):
    doc_ref = db.collection(u'Items').document()
    doc_ref.set({
        u'author': seller,
        u'location': location,
        u'name': name,
        u'price': price,
        u'subtitle': detail,
    })


def testFirebase():
    doc_ref = db.collection(u'Users').document(u'alovelace')
    doc_ref.set({
        u'first': u'Ada',
        u'last': u'Lovelace',
        u'born': 1815
    })

    doc_ref = db.collection(u'Users').document(str("abc"))
    doc_ref.update({
        u't1': str("1235"),

    })

    doc_ref = db.collection(u'Users').document(str("abc")).get()
    print(doc_ref.to_dict())