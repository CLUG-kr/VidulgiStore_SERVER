import requests
import json

firebaseKEY = "AAAA6Uqx-AY:APA91bHVqcEznfJUhgtBAR5WpojLz0EvFmIrgv0CZ7IMODfIjH_4L1jZwDmsnmOMmdm10IZuBmGKYo8UKv4LB8i9DCv18DgN6P-ErLIHBYQndLdIJvVtczbj4JiR8cP6pYZsc2Bk8Mbr"

def send_fcm(seller, item):
	url = 'https://fcm.googleapis.com/fcm/send'
	body = {
		"data": {
			"seller": seller,
			"item": item
		},
		"notification": {
			"title": seller,
			"body": item,
			"content_available": "true"
		},
		"to": "/topics/WantBuy"
	}

	headers = {"Content-Type": "application/json",
			   "Authorization": "key="+firebaseKEY}
	requests.post(url, data=json.dumps(body), headers=headers)