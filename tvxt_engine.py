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
import os 

isDebug = False
isDeploy = True    
app = Flask(__name__)

# curl "http://34.87.11.139:8011/tvxt_engine?function=PROCESS_ID_MANDIRI_TYPE_1&upload_filepath=/var/www/html/samples/Mandiri/RK_Mandiri_5622_BMP2.pdf"
# curl "http://34.126.166.29:8011/tvxt_engine?function=PROCESS_ID_BCA_TYPE_1&upload_filepath=/home/tvx/samples/20210602155228-4046f52a-c6ca-4be6-8018-f22f24003bdf.pdf"
# curl "http://10.148.0.9:8011/tvxt_engine?function=LC_TEST&upload_filepath=/var/www/maybank-ocr-ml/samples/LC/1494BCA201224-13308104475-LC.pdf"
#Process ID_KTP
## For Flask usage
@app.route('/tvxt_engine')
def tvxt_engine():
    print("Receive command and start process.")
    command = request.args.get('function')
    filepath = request.args.get('upload_filepath')
    return "YES ENGINE IS RUNNING FILE " + str(filepath)
    # if command == "PROCESS_SAMPLE":
    #     print("Enter PROCESSS_SAMPLE")
    #     cmd = ["python3", "TVExtract_Sample.py"]  ##linux
    #     cmd.append(filepath)
    #     callrunning = subprocess.Popen(cmd)
    # if command == "PROCESS_MY_MAYBANK":
    #     print("Enter PROCESS_MY_MAYBANK")
    #     cmd = ["python3", "TVExtract_MY_MBB.py"]  ##linux
    #     cmd.append(filepath)
    #     callrunning = subprocess.Popen(cmd)
    # if command == "PROCESS_MY_CIMB":
    #     print("Enter PROCESS_MY_CIMB")
    #     cmd = ["python3", "TVExtract_MY_CIMB.py"]  ##linux
    #     cmd.append(filepath)
    #     callrunning = subprocess.Popen(cmd)
    # #if command == "PROCESS_SAMPLE":
    # #    print("Enter PROCESSS_SAMPLE")
    # #    cmd = ["python3", "TVExtract_Sample.py"]  ##linux
    # #    cmd.append(filepath)
    # #    callrunning = subprocess.Popen(cmd)

    # #print (callrunning.communicate())
    # print("Done Enter Process.")
        
    # #print("--- %s seconds ---" % (time.time() - start_time))
    # return jsonify(True)

if __name__ == '__main__':
   app.run(host='0.0.0.0', port=80)