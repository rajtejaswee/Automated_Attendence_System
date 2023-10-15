import cv2
import os
import pickle
import face_recognition
import numpy as np
import cvzone
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage
import numpy as np

from datetime import datetime

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    "databaseURL": "https://attendancesystem-76dce-default-rtdb.firebaseio.com/",
    "storageBucket": "attendancesystem-76dce.appspot.com"
})

bucket = storage.bucket()

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

imgBackground = cv2.imread('Resources/background.png')

# Importing the mode images into a list
folderModePath = 'Resources/Modes'
modePathList = os.listdir(folderModePath)
imgModeList = []
for path in modePathList:
    imgModeList.append(cv2.imread(os.path.join(folderModePath, path)))
# print(len(imgModeList))

# Load the encoding file
print("Loading Encode File ...")
file = open('EncodeFile.p', 'rb')
encodeListKnownWithIds = pickle.load(file)
file.close()
encodeListKnown, studentIds = encodeListKnownWithIds
print(studentIds)
print("Encode File Loaded")

mode = 0
visit = 0
id = -1
imgStudent = []

while True:
    success, img = cap.read()

    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    faceCurFrame = face_recognition.face_locations(imgS)
    encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)

    imgBackground[162:162+480, 55:55+640] = img
    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[mode]

    for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace, tolerance=0.55)
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
        # print("matches", matches)
        # print("faceDis", faceDis)

        matchIndex = np.argmin(faceDis)
        # (w, h), _ = cv2.getTextSize("", cv2.FONT_HERSHEY_COMPLEX, 1, 1)
        # offset = (414 - w) // 2

        if matches[matchIndex]:
            print("Face Detected of Student's ID: ", studentIds[matchIndex])
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
            bbox = 55 + x1, 162 + y1, x2 - x1, y2 - y1
            imgBackground = cvzone.cornerRect(imgBackground, bbox, rt=1)
            id = studentIds[matchIndex]
            if visit == 0:
                cvzone.putTextRect(imgBackground, "Loading", (275, 400))
                cv2.imshow("Face Attendance", imgBackground)
                cv2.waitKey(1)
                visit = 1
                mode = 1

        if visit != 0:

            if visit == 1:
                studentInfo = db.reference(f'Students/{id}').get()
                print(studentInfo)

                blob = bucket.get_blob(f'Images/{id}.png')
                array = np.frombuffer(blob.download_as_string(), np.uint8)
                imgStudent = cv2.imdecode(array, cv2.COLOR_BGRA2BGR)
                # print(type(studentInfo))
                latest_attendance = studentInfo['last_attendance']
                print(latest_attendance)
                print(list(latest_attendance)[-1])
                # print(type(latest_attendance[list(latest_attendance)[-1]]))
                datetimeObject = datetime.strptime(list(latest_attendance)[-1],
                                                   "%Y-%m-%d %H:%M:%S")
                print(datetimeObject)
                secondsElapsed = (datetime.now() - datetimeObject).total_seconds()
                print(secondsElapsed)
                print(datetime.now().strftime("%m/%d/%Y"))
                print(datetime.now().strftime("%H:%M:%S"))
                if secondsElapsed > 86400:
                    ref = db.reference(f'Students/{id}')
                    studentInfo['total_attendance'] += 1
                    ref.child('total_attendance').set(studentInfo['total_attendance'])
                    print(ref.child('last_attendance'))
                    toAdd = len(list(latest_attendance))
                    print(list(latest_attendance))
                    print(toAdd)
                    dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    print(dt)
                    # list(latest_attendance).splice(toAdd, 1, dt)
                    print(list(latest_attendance))
                    obj = {toAdd: datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

                    # latest_attendance['toAdd'] =
                    # print
                    print(type(ref.child('last_attendance')))
                    ref.child('last_attendance').update(obj)
                    print("hip hip")
                    studentInfo['attendance_percentage'] = round((studentInfo['total_attendance'] / studentInfo[
                        'total_lectures']) * 100, 2)
                    ref.child('total_attendance').set(studentInfo['total_attendance'])
                    ref.child('attendance_percentage').set(studentInfo['attendance_percentage'])
                    print("added")
                else:
                    mode = 3
                    visit = 0
                    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[mode]

            if mode != 3:
                if 10<visit<20:
                    mode = 2

                imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[mode]

                if visit <= 10:
                    cv2.putText(imgBackground, str(studentInfo['total_attendance']), (861, 125),
                                cv2.FONT_HERSHEY_COMPLEX, 1, (242, 239, 235), 1)
                    cv2.putText(imgBackground, str(id), (950, 493),
                                cv2.FONT_HERSHEY_COMPLEX, 0.75, (242, 239, 235), 1)
                    cv2.putText(imgBackground, str(studentInfo['batch']), (1025, 625),
                                cv2.FONT_HERSHEY_COMPLEX, 0.6, (66, 58, 56), 1)
                    cv2.putText(imgBackground, str(studentInfo['attendance_percentage']), (1125, 625),
                                cv2.FONT_HERSHEY_COMPLEX, 0.6, (66, 58, 56), 1)

                    (w, h), _ = cv2.getTextSize(studentInfo['name'], cv2.FONT_HERSHEY_COMPLEX, 1, 1)
                    offset = (414 - w) // 2
                    cv2.putText(imgBackground, str(studentInfo['name']), (808 + offset, 445),
                                cv2.FONT_HERSHEY_COMPLEX, 1, (66, 58, 56), 1)

                    imgBackground[175:175 + 216, 909:909 + 216] = imgStudent

                visit += 1

                if visit >= 20:
                    visit = 0
                    mode = 0
                    studentInfo = []
                    imgStudent = []
                    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[mode]
        else:
            visit = 0
            mode = 0


        # else :
        #     cv2.putText(imgBackground, "Unregistered", (808 + offset, 445),
        #                 cv2.FONT_HERSHEY_COMPLEX, 1, (66, 58, 56), 1)
        #     print("Unregistered")
    # cv2.imshow("WebCam", img)
    cv2.imshow("Face Attendance", imgBackground)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break