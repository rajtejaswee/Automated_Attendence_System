import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    "databaseURL": "https://attendancesystem-76dce-default-rtdb.firebaseio.com/",
    "storageBucket": "attendancesystem-76dce.appspot.com"
})

folderPath = 'Images'
pathList = os.listdir(folderPath)
print(pathList)

# for path in pathList:
#     fileName = f'{folderPath}/{path}'
#     print(fileName)
#     bucket = storage.bucket()
#     blob = bucket.blob(fileName)
#     blob.upload_from_filename(fileName)

ref = db.reference('Students')

data = {
    "202011007":
        {
            "name": "Al Kahaf Ahmad",
            "batch": "2020",
            "total_attendance": 10,
            "last_attendance": {
                "0": "2022-12-11 00:54:34"
            },
            "attendance_percentage": 0,
            "total_lectures": 20
        },
    "202011013":
        {
            "name": "Ashish Gupta",
            "batch": "2020",
            "total_attendance": 10,
            "last_attendance": {
                "0": "2022-12-11 00:54:34"
            },
            "attendance_percentage":0,
            "total_lectures": 20
        },
    "202011015":
        {
            "name": "Avichal Bansal",
            "batch": "2020",
            "total_attendance": 10,
            "last_attendance": {
                "0": "2022-12-11 00:54:34"
            },
            "attendance_percentage": 0,
            "total_lectures": 20
        },
    "202011060":
        {
            "name": "Raj Tejaswee",
            "batch": "2020",
            "total_attendance": 10,
            "last_attendance": {
                "0": "2022-12-11 00:54:34"
            },
            "attendance_percentage": 0,
            "total_lectures": 20
        },
    "202011077":
        {
            "name": "Vartul Shrivastava",
            "batch": "2020",
            "total_attendance": 10,
            "last_attendance": {
                "0": "2022-12-11 00:54:34"
            },
            "attendance_percentage": 0,
            "total_lectures": 20
        },
    "202011054":
        {
            "name": "Sanskar Patel",
            "batch": "2020",
            "total_attendance": 10,
            "last_attendance": {
                "0": "2022-12-11 00:54:34"
            },
            "attendance_percentage": 0,
            "total_lectures": 20
        }
}

for key,value in data.items():
    ref.child(key).set(value)