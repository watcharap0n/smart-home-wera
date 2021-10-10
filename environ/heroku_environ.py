import os

SECRET_LINE = os.environ['SECRET_LINE']
ACCESS_TOKEN = os.environ['ACCESS_TOKEN']

set_firebase = {
    "apiKey": os.environ['apiKey'],
    "authDomain": os.environ['authDomain'],
    "projectId": os.environ['projectId'],
    "databaseURL": os.environ['databaseURL'],
    "storageBucket": os.environ['storageBucket'],
    "messagingSenderId": os.environ['messagingSenderId'],
    "appId": os.environ['appId'],
    "measurementId": os.environ['measurementId']
}