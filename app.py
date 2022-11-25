from jarvissGui2 import Ui_MainWindow
from PyQt5 import QtCore , QtWidgets , QtGui
from PyQt5.QtGui import QMovie
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.uic import loadUiType
import numpy as np
import cv2
import os
import imutils
import subprocess
from gtts import gTTS 
import pyttsx3
import pyttsx3
import speech_recognition as sr 
import webbrowser as Web 
import pywhatkit
import winsound 
import requests
from geopy.distance import great_circle 
from geopy.geocoders import Nominatim
import geocoder
from art import *
import datetime
import sys
import time
import yagmail
from playsound import playsound
import requests
import json
def say(text):
    engine = pyttsx3.init('sapi5')
    voice = engine.getProperty('voices')
    engine.setProperty('voice', voice[1].id)
    engine.setProperty('rate',150)
    print("  ")
    print(f"panic : {text}")
    engine.say(text=text)
    engine.runAndWait()
    print("  ")
class MainThread(QThread):
    
    def __init__(self):
        super(MainThread,self).__init__()

    def run(self):
            self.Taskexe()
    def listen(self):
            r = sr.Recognizer()
            with sr.Microphone() as source:
                print("Listening...")
                r.pause_threshold = 1
                audio = r.listen(source,0,5)
            try:
                print("Recognizing..") 
                query = r.recognize_google(audio,language="en-in")
                print(f"You Said : {query}")
            except:
                return
            query = str(query)
            return query.lower()
    def Taskexe(self):
        say("how i can help you ?")
        def beep(duration=500) :
            frequency = 2500  # Set Frequency To 2500 Hertz
            winsound.Beep(frequency, duration)
        def location():
            ip_add = requests.get('https://api.ipify.org').text

            url = 'https://get.geojs.io/v1/ip/geo/' + ip_add + '.json'

            geo_q = requests.get(url)

            geo_d = geo_q.json()

            state = geo_d['city']

            country = geo_d['country']

            say(f"you are in {state , country} .")
        def googlemaps(Place):
            URL="https://www.google.com/maps/place/"+str(Place)
            geolocator = Nominatim(user_agent="myGeocoder")
            location = geolocator.geocode(Place, addressdetails=True)
            target_latlon=location.latitude , location.longitude
            location = location.raw['address']
            target = {'city': location.get('city',' '),
                        'state':location.get('state',''),
                        'country': location.get('country','')}
            current_loca = geocoder.ip('me')
            current_latlon = current_loca.latlng
            distance = str(great_circle(current_latlon,target_latlon))
            distance=str(distance.split(' ',1)[0])
            distance=int(float(distance))
            Web.open(url=URL)
            say(target)
            say(f"sir,{Place} is {distance} km  away from your location")
        def realtime():
            import time
            LABELS = open("coco.names").read().strip().split("\n")
            print("[INFO] loading YOLO from disk...")
            net = cv2.dnn.readNetFromDarknet("yolov3.cfg", "..\jarvis\yolov3.weights")

            ln = net.getLayerNames()
            ln = [ln[i - 1] for i in net.getUnconnectedOutLayers()]

            
            cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

            frame_count = 0
            start = time.time()
            first = True
            frames = []

            while True:
                frame_count += 1
                
                ret, frame = cap.read()
                frame = cv2.flip(frame,1)
                frames.append(frame)

                if frame_count == 300:
                    break
                if ret:
                    
                    key = cv2.waitKey(1)
                    
                    if frame_count % 60 == 0:
                        end = time.time()
                        
                        (H, W) = frame.shape[:2]
                        blob = cv2.dnn.blobFromImage(frame, 1 / 255.0, (416, 416),
                            swapRB=True, crop=False)
                        net.setInput(blob)
                        layerOutputs = net.forward(ln)
                        boxes = []
                        confidences = []
                        classIDs = []
                        centers = []

                        for output in layerOutputs:
                            for detection in output:
                                scores = detection[5:]
                                classID = np.argmax(scores)
                                confidence = scores[classID]
                                if confidence > 0.5:
                                    box = detection[0:4] * np.array([W, H, W, H])
                                    (centerX, centerY, width, height) = box.astype("int")
                                    x = int(centerX - (width / 2))
                                    y = int(centerY - (height / 2))
                                    w = int(width)
                                    h = int(height)
                                    boxes.append([x, y, int(width), int(height)])
                                    confidences.append(float(confidence))
                                    classIDs.append(classID)
                            
                                    centers.append((centerX, centerY))
                                    
                                    frame = cv2.rectangle(frame, (x,y), (x+w,y+h), (0,250,0), 1)
                                    cv2.imshow("Live Detection", frame)

                        idxs = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.3)

                        texts = []
                        if len(idxs) > 0:
                            for i in idxs.flatten():
                                centerX, centerY = centers[i][0], centers[i][1]
                                
                                if centerX <= W/3:
                                    W_pos = "left "
                                elif centerX <= (W/3 * 2):
                                    W_pos = "center "
                                else:
                                    W_pos = "right "
                                
                                if centerY <= H/3:
                                    H_pos = "top "
                                elif centerY <= (H/3 * 2):
                                    H_pos = "mid "
                                else:
                                    H_pos = "bottom "
                        
                                texts.append(H_pos + W_pos + LABELS[classIDs[i]])
                            
                        
                        print(texts)
                        say(texts)
            cap.release()
            cv2.destroyAllWindows()
        def fireproctection():
            def mail():
                import time
                import smtplib
                from email.message import EmailMessage
                Address = "27-17-43/1, Sector 12, Navi Mumbai"
                msg = EmailMessage()
                msg["Subject"] = "Fire Outbreak Detected"
                msg["From"] = "goosezenv@gmail.com"
                msg["To"] = "anushreddydasari@gmail.com"
                msg.set_content(f"I'm FireDetectionSys,\nData:\nAddress - {Address}\nTime - {time.ctime()}")
                with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
                    smtp.login("goosezenv@gmail.com", "test1234test")
                    smtp.send_message(msg)
                    smtp.close()

                def alarm():

                    from playsound import playsound
                    print("Fire Detected")
                    playsound("Alert.mp3")


                def shutdown():

                    import time
                    import sys
                    time.sleep(1)
                    sys.exit()

            if __name__ == '__main__':
                firedetector = cv2.CascadeClassifier('FDSys.xml')
                capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)
                capture.set(3,640)
                capture.set(4,480)
                while (True):
                    ret, frame = capture.read()
                    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    fire = firedetector.detectMultiScale(frame, 1.2, 5)
                    for (x,y,w,h) in fire:
                        cv2.destroyAllWindows()
                        alarm()
                        mail()
                        shutdown()

                    cv2.imshow('window', frame)
                    if cv2.waitKey(1) == ord('q'):
                        break 
        def police():
            say("Sending message home")
            say("searching for Nearby police station")
            r = requests.get('https://get.geojs.io/')
            ip_request=requests.get('https://get.geojs.io/v1/ip.json')
            ipAdd = ip_request.json()
            import json 
            from urllib.request import urlopen
            url = 'https://ipinfo.io/json'
            response=urlopen(url)
            data=json.load(response)
            url ='https://get.geojs.io/v1/ip/geo/'+data['ip']+'.json'
            geo_request=requests.get(url)
            geo_data = geo_request.json()
            response_API = requests.get(' https://discover.search.hereapi.com/v1/discover?at='+geo_data['longitude']+','+geo_data['latitude']+'&limit=6&lang=en&q=police+greaternoida&apiKey=tTF-MpGBcrXpP31qui2XhymGTA5YCG4aDg0q9_A_IjY')
            data = response_API.text
            datay = json.loads(data)
            x=(datay['items'])
            y=(x[5]['title'])
            say('nearest station is {}'.format(y))
            say("more station near you")
            for i in range(len(x)):
                print(x[i]['position'])
                say("if you want routes say way")
                reciever=self.listen()
                if "way" in reciever:
                            x=(datay['items'])
                            r=(x[i]['position'])
                            t=(r['lat'])
                            o=(r['lng'])
                            response_APIi = requests.get('https://router.hereapi.com/v8/routes?transportMode=car&origin='+geo_data['latitude']+','+geo_data['longitude']+'&destination='+str(t)+','+str(o)+'&return=summary&apiKey=tTF-MpGBcrXpP31qui2XhymGTA5YCG4aDg0q9_A_IjY')
                            print(response_APIi.status_code)
                            data = response_APIi.text
                            dataz = json.loads(data)
                            say("describing route")
                            say(dataz['routes'])
                else:
                        say("okay")
        def hospital():
                    say("Sending message home")
                    say("searching for Nearby hospital")
                    r = requests.get('https://get.geojs.io/')
                    ip_request=requests.get('https://get.geojs.io/v1/ip.json')
                    ipAdd = ip_request.json()
                    import json 
                    from urllib.request import urlopen
                    url = 'https://ipinfo.io/json'
                    response=urlopen(url)
                    data=json.load(response)
                    url ='https://get.geojs.io/v1/ip/geo/'+data['ip']+'.json'
                    geo_request=requests.get(url)
                    geo_data = geo_request.json()
                    response_API = requests.get(' https://discover.search.hereapi.com/v1/discover?at='+geo_data['longitude']+','+geo_data['latitude']+'&limit=6&lang=en&q=hospital+greaternoida&apiKey=tTF-MpGBcrXpP31qui2XhymGTA5YCG4aDg0q9_A_IjY')
                    data = response_API.text
                    datay = json.loads(data)
                    x=(datay['items'])
                    y=(x[3]['title'])
                    say('nearest hospital is {}'.format(y))
                    say("more hospital near you")
                    for i in range(len(x)):
                        print(x[i]['access'])
                        say(x[i]['title'])
                    say("if you want routes say way")
                    reciever=self.listen()
                    if "way" in reciever:
                            x=(datay['items'])
                            r=(x[i]['position'])
                            t=(r['lat'])
                            o=(r['lng'])
                            response_APIi = requests.get('https://router.hereapi.com/v8/routes?transportMode=car&origin='+geo_data['latitude']+','+geo_data['longitude']+'&destination='+str(t)+','+str(o)+'&return=summary&apiKey=tTF-MpGBcrXpP31qui2XhymGTA5YCG4aDg0q9_A_IjY')
                            print(response_APIi.status_code)
                            data = response_APIi.text
                            dataz = json.loads(data)
                            say("describing route")
                            say(dataz['routes'])
                    else:
                        say("okay")
                    
            
        def mail():
                    r = requests.get('https://get.geojs.io/')
                    ip_request=requests.get('https://get.geojs.io/v1/ip.json')
                    ipAdd = ip_request.json()
                    import json 
                    from urllib.request import urlopen
                    url = 'https://ipinfo.io/json'
                    response=urlopen(url)
                    data=json.load(response)
                    url ='https://get.geojs.io/v1/ip/geo/'+data['ip']+'.json'
                    geo_request=requests.get(url)
                    geo_data = geo_request.json()
                    response_API = requests.get('https://discover.search.hereapi.com/v1/discover?at='+geo_data['longitude']+','+geo_data['latitude']+'&limit=2&lang=en &q=Obi+uttarpradesh&apiKey=tTF-MpGBcrXpP31qui2XhymGTA5YCG4aDg0q9_A_IjY')
                    data = response_API.text
                    datay = json.loads(data)
                    
                    import time
                    import smtplib
                    from email.message import EmailMessage
                    Address = datay
                    msg = EmailMessage()
                    msg["Subject"] = "Emergency alert"
                    msg["From"] = "namantaneja13@gmail.com"
                    msg["To"] = "namojain.2003@@gmail.com"
                    msg.set_content(f"emergency,\nData:\nAddress - {Address}\nTime - {time.ctime()}")
                    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
                        smtp.login("namantaneja13@gmail.com", "bornfighter13031129")
                        smtp.send_message(msg)
                        smtp.close()

                    
        while True:
            try:
                self.query = self.listen()    
                if "emergency" in self.query:
                    beep() 
                    beep()
                    beep()
                    say("Message has been  send to your family members")
                    mail()
                    location()
                    break
                elif "location" in self.query:
                    location()
                    say("done")
                elif "time" in self.query:
                    time_Ac =datetime.datetime.now()
                    now=time_Ac.strftime("%H:%M:%S")
                    say(now)
                elif "where is" in self.query:
                    beep()
                    self.query=self.query.replace("where is"," ")
                    googlemaps(self.query)
                elif "google search" in self.query:
                    beep()
                    say("this is what i found")
                    self.query=self.query.replace("google search"," ")
                    self.query=self.query.replace("flypy"," ")
                    pywhatkit.search(self.query)
                    say("done")
                elif "detection" in self.query:
                    beep()
                    say("fly py starts real time detection ")
                    realtime()
                    say("done")
                elif "help" in self.query:
                    say("what kind of emergency")
                    reciever=self.listen()
                    if "fire" in reciever:
                        beep()
                        fireproctection()
                        beep()
                    elif "police" in reciever:
                        beep()
                        police()
                        
                    elif "hospital" in reciever:
                        beep()
                        hospital()
                        

                        beep()
                        
                    else:
                        say("your safe ")             
                else:
                    say("Not a valid command")
            except TypeError:
                say("Going to sleep")
                break
startFunction = MainThread()

class Gui_Start(QMainWindow):
    def __init__(self):
        super().__init__()
        self.jarvis_ui = Ui_MainWindow()
        self.jarvis_ui.setupUi(self)

        self.jarvis_ui.pushButton_3.clicked.connect(self.startFunc)
        self.jarvis_ui.pushButton_4.clicked.connect(self.close)
    def startFunc(self):

        self.jarvis_ui.movies_2 = QtGui.QMovie("Brown and Beige Pattern Hand Help Illustrated Random Act Of Kindness Flyer (Presentation (169)) (1).gif")
        self.jarvis_ui.label.setMovie(self.jarvis_ui.movies_2)
        self.jarvis_ui.movies_2.start()
        
        self.jarvis_ui.movies_3 = QtGui.QMovie("Brown and Beige Pattern Hand Help Illustrated Random Act Of Kindness Flyer (Presentation (169)) (1).gif")
        self.jarvis_ui.label_2.setMovie(self.jarvis_ui.movies_3)
        self.jarvis_ui.movies_3.start()
        startFunction.start()
   
Gui_App = QApplication(sys.argv)
Gui_Jarvis = Gui_Start()
Gui_Jarvis.show()
exit(Gui_App.exec_())

















