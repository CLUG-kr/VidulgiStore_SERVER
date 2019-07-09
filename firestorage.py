import datetime

from firebase_admin import credentials, firestore, storage


def uploadFile(url, name):
    db = firestore.client()
    bucket = storage.bucket("vidulgi.appspot.com")
    blob = bucket.blob(name)
    outfile= url
    with open(outfile, 'rb') as my_file:
        blob.upload_from_file(my_file)

def downloadImage(img):
    db = firestore.client()
    bucket = storage.bucket("vidulgi.appspot.com")
    blob = bucket.blob(img)
    return blob.generate_signed_url(datetime.timedelta(seconds=10), method='GET')