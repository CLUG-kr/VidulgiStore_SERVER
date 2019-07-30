import datetime

from firebase_admin import credentials, firestore, storage


def uploadFile(name):
    db = firestore.client()
    bucket = storage.bucket("vidulgi.appspot.com")
    blob = bucket.blob(name)
    blob.upload_from_filename(name)

def downloadImage(img):
    db = firestore.client()
    bucket = storage.bucket("vidulgi.appspot.com")
    blob = bucket.blob(img)
    return blob.generate_signed_url(datetime.timedelta(seconds=20), method='GET')