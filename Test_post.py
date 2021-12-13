from ftplib import FTP
from flask import Flask, request, jsonify
import requests

def Post_Success():

    post_status_to_webapp = requests.post('http://34.125.139.205/document/receive_json')
    return True

Post_Success()
