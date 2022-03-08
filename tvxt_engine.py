# Developer     : Yiqi, Prof Lim
# Version       : v0.0
# Latest update : 202101131700
# Project       : tvExtract Engine

# GENERAL STEPS
# 1. Change the last line to your local IP address
# 2. Comment/Uncomment the file path of your OS

from flask import Flask, request, jsonify
import subprocess
#from subprocess import Popen, CREATE_NEW_CONSOLE   ##windows
from subprocess import Popen                        ##linux
import requests
import os 

isDebug = False
isDeploy = True    
app = Flask(__name__)
web_ip = '34.101.203.130'
URL_PDF_FRONTEND = "http://"+ web_ip +"/uploads/document/" #postgre
URL_PDF_BACKEND = "/var/html/server-ml/samples/"
# curl "http://34.87.11.139:8011/tvxt_engine?function=PROCESS_ID_MANDIRI_TYPE_1&upload_filepath=/var/www/html/samples/Mandiri/RK_Mandiri_5622_BMP2.pdf"
# curl "http://34.126.166.29:8011/tvxt_engine?function=PROCESS_ID_BCA_TYPE_1&upload_filepath=/home/tvx/samples/20210602155228-4046f52a-c6ca-4be6-8018-f22f24003bdf.pdf"
# curl "http://10.148.0.9:8011/tvxt_engine?function=LC_TEST&upload_filepath=/var/www/maybank-ocr-ml/samples/LC/1494BCA201224-13308104475-LC.pdf"
#Process ID_KTP
## For Flask usage

@app.route('/tvxt_engine', methods=['GET', 'POST'])
def tvxt_engine():
    print("Receive command and start process.")
    cmd = ["python3", "Test_post.py"]  ##linux
    callrunning = subprocess.Popen(cmd)


    if request.method=="POST":
        command = request.form.get("function")
        if command == "bca":
            filenames = request.form.get("filename")
            url = URL_PDF_FRONTEND + str(filenames) #get pdf from php side
            filepaths = URL_PDF_BACKEND + str(filenames) #save pdf to python side
            response = requests.get(url)
            with open(filepaths,"wb") as f:
                f.write(response.content)
            return 'receive'
        
       if command == "PROCESS_ID_BCA_TYPE_1":
			filenames = request.form.get("filename")
			url = URL_PDF_FRONTEND + str(filenames) #get pdf from php side
			filepaths = URL_PDF_BACKEND + str(filenames) #save pdf to python side
			response = requests.get(url)
			with open(filepaths,"wb") as f:
				f.write(response.content)
			print("Enter PROCESS_ID_BCA_TYPE_1")
			cmd = ["python3", "ID_BCA_1_FUNCTIONS.py"]  ##linux
			cmd.append(filepaths)
			PrintLog("API Success",filenames)
			callrunning = subprocess.Popen(cmd)
    

    return jsonify(True)

if __name__ == '__main__':
   app.run(host='0.0.0.0', port=80)
