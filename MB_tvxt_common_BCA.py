# Developer     : Dr Tew, Prof Lim, Wilsen, Adrian, Mita
# Version       : v1.0
# Latest update : 202103182200
# Project       : Common Import and Defined Funtions

import math
from flask import Flask, request, jsonify
from os import listdir
from os.path import isfile, join
import pikepdf
from pdf2image import pdfinfo_from_path,convert_from_path
import numpy as np
import csv
import cv2
import ftfy
import imutils
import matplotlib.pyplot as plt
import os
import pandas as pd
import pytesseract
import re
import string
import time, datetime
import sys
import json
from ftplib import FTP
import platform
from PyPDF2 import PdfFileReader, PdfFileWriter
import sys, subprocess
# from TVExtract_PostProcessing import *
import requests
from PIL import Image

os.environ['OMP_THREAD_LIMIT'] = '1'
start_time  = time.time()
isDebug     = False  # For showing all detailed output in ipynb
isDeploy    = True  # For running at server, with MINIMAL processes
isOutputXls = True   # For generating xlsx
isOutputJsn = True   # For generating json
host = '10.184.0.6'
user = 'tvx'
password = 'php@ml123'
app = Flask(__name__)

#Global IP
global api_ip
global URL_Success
global URL_Error
global URL_WebApp
global URL_Receive
global URL_Json

api_ip = '34.101.203.130'
URL_Success = 'http://' + api_ip + ':80/index.php/panggilAku'
URL_Error = 'http://' + api_ip + ':80/index.php/panggilAku/index_error'
URL_Receive = 'http://' + api_ip + ':80/index.php/panggilAku/receive'
URL_WebApp = '/var/html/output/static/'
URL_Json = '/var/html/output/json/'

PROCESS_NAME        = "DEFAULT_BANKSTATEMENT"

#SAMPLE_DIRECTORY    = r"[YOUR SAMPLE DATA DIRECTORY]"

#By default (server) program runs in
#TVEXTRACT_FOLDER    = r"/var/www/html/tvextract-web/application/libraries/python/"
#Uncheck below if run in local directory
#TVEXTRACT_FOLDER   = r"[YOUR LOCAL DIRECTORY]"
TVEXTRACT_FOLDER    = r"/var/html/main/"

### ALL PROCESS / OUTPUT FILE NAME IS FOLLOWING RAW / INPUT FILE NAME ###
# For all raw / input files
RAW_FOLDER_PATH     = TVEXTRACT_FOLDER + "raw/"
# For processed image before pass to tesseract
PROCESS_FOLDER_PATH = TVEXTRACT_FOLDER + "process/"
# For logging on every exception
LOG_FOLDER_PATH     = TVEXTRACT_FOLDER + "log/"
# For AI detection
XML_FOLDER_PATH     = TVEXTRACT_FOLDER + "xml/"
TIME_FOLDER_PATH    = TVEXTRACT_FOLDER + "time/"
FACE_XML_PATH       = XML_FOLDER_PATH  + "haarcascade_frontalface_alt.xml"

# By default (server) to retrieve process output file at
# OUTPUT_FOLDER_PATH  = "/var/www/html/tvextract-web/output/"
#Uncheck below if run in local directory
#OUTPUT_FOLDER_PATH   = r"[YOUR LOCAL OUTPUT DIRECTORY]"
OUTPUT_FOLDER_PATH      = "/home/tvx/"
OUTPUT_XLS_FOLDER_PATH  = OUTPUT_FOLDER_PATH + "xls/"
OUTPUT_JSN_FOLDER_PATH  = OUTPUT_FOLDER_PATH + "json/"

FILE_NAME_IN_PROCESS= ""

### Tesseract path ###
## Web server ##
#pytesseract.pytesseract.tesseract_cmd = r"/opt/tesseract/tesseract"
# Windows path to tesseract
pytesseract.pytesseract.tesseract_cmd = r"/opt/tesseract/./tesseract"
#dictionary = enchant.Dict("en_US")
PDF2IMG_POPPLER_PATH=r"/etc/poppler-0.73.0/poppler"

SAMPLE_DIRECTORY = ""
PDF2IMG_POPPLER_PATH = ""
LOCAL_DIRECTORY = ""

# SAMPLE_DIRECTORY = ""
# PROCESS_NAME = ""
# TVEXTRACT_FOLDER = ""
# RAW_FOLDER_PATH = ""
# PROCESS_FOLDER_PATH = ""
# LOG_FOLDER_PATH = ""
# XML_FOLDER_PATH = ""
# FACE_XML_PATH = ""
# OUTPUT_FOLDER_PATH = ""
# OUTPUT_XLS_FOLDER_PATH = ""
# OUTPUT_JSN_FOLDER_PATH = ""
# PDF2IMG_POPPLER_PATH = ""
# LOCAL_DIRECTORY = ""

## Pre-defined Function ##

def setPATHS(iSAMPLE_DIRECTORY, iPROCESS_NAME, iTVEXTRACT_FOLDER, iRAW_FOLDER_PATH,
             iPROCESS_FOLDER_PATH, iLOG_FOLDER_PATH, iXML_FOLDER_PATH, iFACE_XML_PATH,
             iOUTPUT_FOLDER_PATH, iOUTPUT_XLS_FOLDER_PATH, iOUTPUT_JSN_FOLDER_PATH,
             iPDF2IMG_POPPLER_PATH):

    global SAMPLE_DIRECTORY
    global PROCESS_NAME
    global TVEXTRACT_FOLDER
    global RAW_FOLDER_PATH
    global PROCESS_FOLDER_PATH
    global LOG_FOLDER_PATH
    global XML_FOLDER_PATH
    global FACE_XML_PATH
    global OUTPUT_FOLDER_PATH
    global OUTPUT_XLS_FOLDER_PATH
    global OUTPUT_JSN_FOLDER_PATH
    global PDF2IMG_POPPLER_PATH

    SAMPLE_DIRECTORY = iSAMPLE_DIRECTORY
    PROCESS_NAME = iPROCESS_NAME
    TVEXTRACT_FOLDER = iTVEXTRACT_FOLDER
    RAW_FOLDER_PATH = iRAW_FOLDER_PATH
    PROCESS_FOLDER_PATH = iPROCESS_FOLDER_PATH
    LOG_FOLDER_PATH = iLOG_FOLDER_PATH
    XML_FOLDER_PATH = iXML_FOLDER_PATH
    FACE_XML_PATH = iFACE_XML_PATH
    OUTPUT_FOLDER_PATH = iOUTPUT_FOLDER_PATH
    OUTPUT_XLS_FOLDER_PATH = iOUTPUT_XLS_FOLDER_PATH
    OUTPUT_JSN_FOLDER_PATH = iOUTPUT_JSN_FOLDER_PATH
    PDF2IMG_POPPLER_PATH = iPDF2IMG_POPPLER_PATH
    print("===========setPATHS==============")
    print("SAMPLE_DIRECTORY=",SAMPLE_DIRECTORY)
    print("PROCESS_NAME=",PROCESS_NAME)
    print("TVEXTRACT_FOLDER=",TVEXTRACT_FOLDER)
    print("RAW_FOLDER_PATH=",RAW_FOLDER_PATH)
    print("PROCESS_FOLDER_PATH=",PROCESS_FOLDER_PATH)
    print("LOG_FOLDER_PATH=",LOG_FOLDER_PATH)
    print("XML_FOLDER_PATH=",XML_FOLDER_PATH)
    print("FACE_XML_PATH=",FACE_XML_PATH)
    print("OUTPUT_FOLDER_PATH=",OUTPUT_FOLDER_PATH)
    print("OUTPUT_XLS_FOLDER_PATH=",OUTPUT_XLS_FOLDER_PATH)
    print("OUTPUT_JSN_FOLDER_PATH=",OUTPUT_JSN_FOLDER_PATH)
    print("poppler_path=",PDF2IMG_POPPLER_PATH)
    #print("==========setPATHS==============")

def setFILE_NAME_IN_PROCESS(iFILE_NAME_IN_PROCESS):
    global FILE_NAME_IN_PROCESS
    global PROCESS_NAME
    PROCESS_NAME = iFILE_NAME_IN_PROCESS[:-4]
    FILE_NAME_IN_PROCESS = TIME_FOLDER_PATH + iFILE_NAME_IN_PROCESS[:-4]+'.txt'
    try:
        f = open(FILE_NAME_IN_PROCESS, "x")
        f.close()
    except:
        os.remove(FILE_NAME_IN_PROCESS)
        f = open(FILE_NAME_IN_PROCESS, "x")
        f.close()
    print("===========setPATHS==============")
    print("FILE_NAME_IN_PROCESS=", FILE_NAME_IN_PROCESS)

def DirectoryCreator(dirs):
    try:
        print("DirectoryCreator creating...",dirs)
        os.mkdir(dirs)
        print("Directory '% s' created successfully." % dirs)
    except:
        print("Directory ", dirs, " already created!")

def PrintLog(text):
    text = str(text)
    print(text)
    now = datetime.datetime.now()
    log_file_name = PROCESS_NAME+"_"+now.strftime("%Y%m%d%H")
    LOG_FILE_PATH = LOG_FOLDER_PATH + log_file_name + ".log"
    try:
        if LOG_FILE_PATH != "":
            f=open(LOG_FILE_PATH, "a+")
            f.write(now.strftime("%Y%m%d %H:%M:%S")+"\t"+text+ "\n")
            f.close()
    except:
        #f=open(LOG_FILE_PATH, "a+")
        #f.write(now.strftime("%Y%m%d %H:%M:%S")+"\t"+"Error when writing Log file:" + LOG_FILE_PATH + "\n")
        print("Error when writing Log file:" + LOG_FILE_PATH)
        f.close()


def ReadFile(LocalFileIndex):
    filepath = ""
    print("LocalFileIndex=",LocalFileIndex,SAMPLE_DIRECTORY)
    if LocalFileIndex == -1:
        filepath = sys.argv[1]#.get('upload_filepath')
        #print("filepath : ", filepath)
        upload_filename = filepath[filepath.rfind("/")+1:]
    else:
        onlyfiles = [f for f in listdir(SAMPLE_DIRECTORY) if isfile(join(SAMPLE_DIRECTORY, f))]
        filepath = join(SAMPLE_DIRECTORY,onlyfiles[LocalFileIndex])
    file_name = os.path.basename(filepath)
    setFILE_NAME_IN_PROCESS(file_name)
    timestamp_collector(time.time() - start_time, "ReadFile")
    return filepath

def IsNativePDF(extractedText, regEx):
    PrintLog("IsNativePDF checking...")
    isNative = False
    if extractedText == ['']*len(extractedText) or extractedText==[]:
        return isNative
    else:
        for text in extractedText:
            if text == ExtractValue_SpecificPattern(text,regEx, 0,'', False, False):
                isNative=True
            else:
                isNative=False
                break
            
    timestamp_collector(time.time() - start_time, "IsNativePDF")
    return isNative

def ReadNativePDF(path):
    PrintLog("Reading pdf file...")

    outputPath = PROCESS_FOLDER_PATH
    base = os.path.basename(path)
    file_name = os.path.splitext(base)[0]
    fileReader = PdfFileReader(path)

    if fileReader.isEncrypted:
        pdf = pikepdf.open(path)
        path=outputPath + file_name +'_decrypted'+'.pdf'
        pdf.save(path)
        base = os.path.basename(path)
        file_name = os.path.splitext(base)[0]
        fileReader = PdfFileReader(path)

    numPages = fileReader.getNumPages()
    list_page=[]
    if numPages == 1:
        list_page.append(path)
    else:
        for page in range(numPages):
            pdf_writer = PdfFileWriter()
            pdf_writer.addPage(fileReader.getPage(page))
            OutputFilePath = outputPath+'{}_page_{}.pdf'.format(file_name, page)
            with open(OutputFilePath, 'wb') as out:
                list_page.append(OutputFilePath)
                pdf_writer.write(out)
    list_filepath=[]
    list_text=[]
    if numPages == 0:
        list_page.append(path)
        OutputFilePath = outputPath+'{}.txt'.format(file_name)
    else:
        for page in range(numPages):
            temp=[]
            OutputFilePath = outputPath+'{}_page_{}.txt'.format(file_name, page)
            # cmd example: "C:\Users\Documents\gs9.54.0\bin\gswin64c.exe -dBATCH -dNOPAUSE -sDEVICE=txtwrite 
            #               -sOutputFile=C:\Users\Documents\OCR_MB\file_name_page_XX.txt path"
            args=['gs', '-dBATCH', '-dNOPAUSE', '-sDEVICE=txtwrite', '-sOutputFile=%s' %OutputFilePath, list_page[page] ]
            try:    
                subprocess.check_output(args, universal_newlines=True)
                with open(OutputFilePath) as f:
                    lines = f.readlines()
                for m in lines:
                    temp.append(' '.join(m.split()))
                list_text.append('\n'.join(temp))
                list_filepath.append(OutputFilePath)
            except:
                PrintLog("ReadNativePDF : Error on page "+ str(page))
    timestamp_collector(time.time() - start_time, "ReadNativePDF")
    return list_filepath,list_text



# def ConvertFileToImageByChris(filepath):
#     host = '10.148.0.3'
#     user1 = 'tvx'
#     password1 = 'php@ml123'
#     file_name = os.path.basename(filepath)
#     process_filepath = PROCESS_FOLDER_PATH + file_name
#     img,list_path = [],[]
#     if filepath.lower().endswith(('.png', '.jpg', '.jpeg','.JPG')):
#         PrintLog("Reading image file: "+ filepath)
#         image = cv2.imread(filepath)#[...,::-1]
#         img.append(image)
#         if isDeploy:
#            cv2.imwrite(process_filepath, img[0])
#            with FTP(host) as ftp:
#             ftp.login(user=user1, passwd=password1)
#             PrintLog(str(ftp.getwelcome()))
#             ftp.cwd(URL_WebApp)

#             with open(process_filepath, 'rb') as im:
#                 ftp.storbinary('STOR ' + file_name, im)
#             ftp.quit()
#         list_path.append(process_filepath)

#     elif filepath.lower().endswith(('.pdf')):
#         PrintLog("Reading PDF file: "+ filepath)
#         # info = pdfinfo_from_path(filepath, userpw=None, poppler_path=None)
#         # maxPages = info["Pages"]
#         # for page in range(1, maxPages+1, 255) :
#         #     pages = convert_from_path(filepath, dpi=600, first_page=page, last_page = min(page+10-1,maxPages))
#         pages = convert_from_path(filepath, dpi=250)
#         file_name_no_ext = os.path.splitext(file_name)[0]
#         i = 0
#         list_path=[]
#         for page in pages:
#             output_filepath = PROCESS_FOLDER_PATH + file_name_no_ext + '.jpg'
#             page.save(output_filepath, 'JPEG')
#             image = cv2.imread(output_filepath)
#             img.append(image)
#             if isDeploy:
#                 output_filepath = PROCESS_FOLDER_PATH + file_name_no_ext + "_" + str(i) + '.jpg'
#                 output_filepath2 = PROCESS_FOLDER_PATH + file_name_no_ext + "_" + str(i) + '.jpg'
#                 send_webapp = URL_WebApp + file_name_no_ext + "_" + str(i) + '.jpg'
#                 page.save(output_filepath, 'JPEG')
#                 page.save(output_filepath2, 'JPEG')
#                 with FTP(host) as ftp :
#                     ftp.login(user=user1, passwd=password1)
#                     PrintLog(str(ftp.getwelcome()))
#                     ftp.cwd(URL_WebApp)

#                     with open(PROCESS_FOLDER_PATH + file_name_no_ext + "_" + str(i) + '.jpg', 'rb') as im:
#                         ftp.storbinary('STOR ' + file_name_no_ext + "_" + str(i) + '.jpg', im)
#                     ftp.quit()
#                 i = i + 1
#             list_path.append(send_webapp)
#     elif filepath.lower().endswith(('.tif','.tiff',)):
#         PrintLog("Reading image file: "+ filepath)
#         img_read = Image.open(filepath) #mandiri.tif[0]dst
#         file_name_no_ext = os.path.splitext(file_name)[0]
#         if isDeploy:
#             for i in range(0,250):
#                 try:
#                     img_read.seek(i)
#                     img_read.save(PROCESS_FOLDER_PATH + file_name_no_ext + "_" + str(i) +'.jpg')
#                     img.append(cv2.imread(PROCESS_FOLDER_PATH + file_name_no_ext + "_" + str(i) +'.jpg'))
#                     send_webapp = URL_WebApp + file_name_no_ext + "_" + str(i) + '.jpg'
#                     try:
#                         with FTP(host) as ftp :
#                             ftp.login(user=user1, passwd=password1)
#                             PrintLog(str(ftp.getwelcome()))
#                             ftp.cwd(URL_WebApp)
#                             with open(PROCESS_FOLDER_PATH + file_name_no_ext + "_" + str(i) + '.jpg', 'rb') as im:
#                                 ftp.storbinary('STOR ' + file_name_no_ext + "_" + str(i) + '.jpg', im)
#                             ftp.quit()
#                         list_path.append(send_webapp)

#                     except:
#                         message = "Error when stor an image"
#                         PrintLog(message)
#                     i = i + 1
#                 except :
#                     message = "tiff cannot be read"
#                     PrintLog(message)
#                     break

#     else:
#         errorMessage = "file cannot be read"
#         PrintLog(errorMessage)
#     timestamp_collector(time.time() - start_time, "ConvertFileToImageByChris")
#     return img, list_path


def RotateImage_FaceDetection(image):
    img = image
    faceCascade = cv2.CascadeClassifier(FACE_XML_PATH)
    faces = faceCascade.detectMultiScale(
                img,
                scaleFactor=1.5,
                minNeighbors=5,
                minSize=(50, 50),
                flags=cv2.CASCADE_SCALE_IMAGE
            )
    if isDebug:
        PrintLog(str(len(faces)) + " face detected")
    if len(faces) < 1:
        for angle in range(90,271,90):
            rotate_img= imutils.rotate(image, angle)
            faces = faceCascade.detectMultiScale(rotate_img, scaleFactor=1.5, minNeighbors=5, minSize=(50, 50),
                                                 flags=cv2.CASCADE_SCALE_IMAGE)
            if len(faces) > 0:
                img = rotate_img
                face_detected = True
                break
    return img, faces

def RotateImage_TextConfidenceLevel(img):
    temp_conf_level=[]
    temp_img=[]
    img=cv2.resize(img,(1000,700))
    temp_conf_level.append(CalcConf_RotateImage(img))
    temp_img.append(img)
    for i in range(90,271,90):
        rotate_img= imutils.rotate(img, i)
        img_rgb = cv2.cvtColor(rotate_img,cv2.COLOR_BGR2RGB)
        fig1, (ax1) = plt.subplots(1, 1, figsize=(25, 8))
        ax1.imshow(img_rgb.astype('uint8'),cmap=plt.cm.gray)
        ax1.set_title(i)
        ax1.set_axis_off()
        plt.show()
        confidence_level=CalcConf_RotateImage(rotate_img)
        temp_conf_level.append(confidence_level)
        temp_img.append(rotate_img)
    #print(temp_conf_level)
    #print(temp_conf_level.index(max(temp_conf_level)))
    #k=temp_img[temp_conf_level.index(max(temp_conf_level))]
    return temp_conf_level, temp_img

def CalcConf_RotateImage(img):
    img_data = pytesseract.image_to_data(img,lang="ind",output_type="data.frame")
    img_data = img_data.dropna()
    #print(img_data)
    if(img_data.empty==False):
        n_boxes = len(img_data['text'])
        pd_index = []
        for i in range(n_boxes):
            pd_index.append(i)
        o = pd.Series(pd_index)
        img_data = img_data.set_index([o])
        if((len(img_data)==1 and img_data['text'][0]==' ') or (len(img_data)==2 and img_data['text'][0]==' ')):
            return 0
        else:
            total = img_data.sum(axis=0)
            count = img_data.count(axis=0)
            avgConf = total.conf / count.conf
            return avgConf
    else:
        return 0

def RetrieveImage_FaceRatio(image, faces):
    raw_width = 1600
    raw_height = 1000
    image_face = image.copy()
    if(len(faces)>0):
        x, y, w, h = faces[len(faces)-1]
        cv2.rectangle(image_face, (x, y), (x+w, y+h), (0, 255, 0), 20)
        # card_width = 8 face_width
        # card_height = 4 face_height
        # face_x = 5 face_width from left
        # face_y = 2 face_height from top
        start_x = 0 if x-(5*w) < 0 else x-(5*w)
        start_y = 0 if y-(2*h) < 0 else y-(2*h)
        end_x = image.shape[1] if x+(2*w) > image.shape[1] else x+(2*w)
        end_y = image.shape[0] if y+(3*h) > image.shape[0] else y+(3*h)
        if isDebug==False:
            PrintLog("from "+ str(image.shape[1])+ str(image.shape[0])+ " crop to "+ str(start_x)+ str(end_x)+ str(start_y)+ str(end_y))

        region_0 = image[start_y:end_y, start_x:end_x]
        image_resize = cv2.resize(region_0, (raw_width, raw_height))
    else:
        image_resize=image

    if isDebug:
        image_face_rgb = cv2.cvtColor(image_face,cv2.COLOR_BGR2RGB)
        image_resize_rgb = cv2.cvtColor(image_resize,cv2.COLOR_BGR2RGB)
        fig1, (ax1, ax2) = plt.subplots(1, 2, figsize=(25, 8))
        ax1.imshow(image_face_rgb.astype('uint8'),cmap=plt.cm.gray)
        ax1.set_title("Detected Face")
        ax1.set_axis_off()
        ax2.imshow(image_resize_rgb.astype('uint8'),cmap=plt.cm.gray)
        ax2.set_title("Resized image")
        ax2.set_axis_off()
        plt.show()
    return image_resize, image_face


def RetrieveImage_QRCodeRatio(image, image_qrcode, x, y, w, h):
    raw_width = 1000
    raw_height = 700
    cv2.rectangle(image_qrcode, (x, y), (x+w, y+h), (0, 255, 0), 20)
    # card_width = 6.5 face_width
    # card_height = 3.5 face_height
    # face_x = 5.5 face_width from left # 6.5 - 5.5 = 1.0
    # face_y = 1 face_height from top # 3.5 - 1 = 2.5
    start_x = 0 if int(x-(5.5*w)) < 0 else int(x-(5.5*w))
    start_y = 0 if int(y-(1.5*h)) < 0 else int(y-(1.5*h))
    end_x = image.shape[1] if int(x+(1.0*w)) > image.shape[1] else int(x+(1.0*w))
    end_y = image.shape[0] if int(y+(2.5*h)) > image.shape[0] else int(y+(2.5*h))
    if isDebug:
        PrintLog("from "+ str(image.shape[1])+ str(image.shape[0])+" crop to "+ str(start_x)+ str(end_x)+ str(start_y)+ str(end_y))
    region_0 = image[start_y:end_y, start_x:end_x]
    image_resize = cv2.resize(region_0, (raw_width, raw_height))
    if isDebug:
        image_qrcode_rgb = cv2.cvtColor(image_qrcode,cv2.COLOR_BGR2RGB)
        image_resize_rgb = cv2.cvtColor(image_resize,cv2.COLOR_BGR2RGB)
        fig1, (ax1, ax2) = plt.subplots(1, 2, figsize=(25, 8))
        ax1.imshow(image_qrcode_rgb.astype('uint8'),cmap=plt.cm.gray)
        ax1.set_title("Detected QR Code")
        ax1.set_axis_off()
        ax2.imshow(image_resize_rgb.astype('uint8'),cmap=plt.cm.gray)
        ax2.set_title("Resized image")
        ax2.set_axis_off()
        plt.show()
    return image_resize

def RemoveQRCode(image):
    processedImage = image.copy()
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (9,9), 0)
    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    # Morph close
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))
    close = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=2)

    # Find contours and filter for QR code
    cnts = cv2.findContours(close, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    if isDebug:
        PrintLog("Detected QR boxes number : "+ str(len(cnts)))
    largestArea = 0
    selectedRect = 0
    for c in cnts:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.04 * peri, True)
        x,y,w,h = cv2.boundingRect(approx)
        area = cv2.contourArea(c)
        ar = w / float(h)
        if len(approx) == 4 and area > 5000 and (ar > .85 and ar < 1.3):
            if area > largestArea:
                selectedRect = [x,y,w,h]
                largestArea = area
    if len(cnts) > 0 and largestArea != 0:
        if isDebug:
            PrintLog("Approx : 4, SelectedArea : "+ str(largestArea))
        [x,y,w,h] = selectedRect
        cv2.rectangle(processedImage, (x, y), (x + w, y + h), (255,255,255), -1)
        processedImage = RetrieveImage_QRCodeRatio(processedImage, image, x, y, w, h)
    return processedImage

def FilterImage_Threshold(image, value, displayDebugImage):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    th, image = cv2.threshold(gray, value[0], 255, value[1])

    if isDebug and displayDebugImage:
        fig1, (ax1) = plt.subplots(1, 1, figsize=(25, 8))
        ax1.imshow(image.astype('uint8'),cmap=plt.cm.gray)
        ax1.set_title(value)
        ax1.set_axis_off()
        plt.show()
    timestamp_collector(time.time() - start_time, "FilterImage_Threshold")
    return image

def SegmentImage_FaceRatio(image_gray, image_rgb):
    faceCascade = cv2.CascadeClassifier(FACE_XML_PATH)
    faces = faceCascade.detectMultiScale(
                image_rgb,
                scaleFactor=1.5,
                minNeighbors=5,
                minSize=(50, 50),
                flags=cv2.CASCADE_SCALE_IMAGE
            )
    if isDebug:
        PrintLog(str(len(faces))+ " face is detected")
    if(len(faces)>0):
        x, y, w, h = faces[len(faces)-1]
        #cv2.rectangle(img_resize_rgb, (x, y), (x+w, y+h), (0, 255, 0), 20)
        region_1 = image_gray[0:image_gray.shape[0], 0:x-50]
        region_2 = image_gray[y+h+50:y+h+300, x-100:image_gray.shape[1]-50]
        region_3 = image_rgb[y-80:y+h+80, x-50:x+w+50]
    else:
        region_1 = image_rgb
        region_2 = image_rgb
        region_3 = image_rgb
    if isDebug:
        fig1, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(25, 8))
        ax1.imshow(region_1.astype('uint8'),cmap=plt.cm.gray)
        ax1.set_title("Region 1 image")
        ax1.set_axis_off()
        ax2.imshow(region_2.astype('uint8'),cmap=plt.cm.gray)
        ax2.set_title("Region 2 image")
        ax2.set_axis_off()
        region_3_rgb = cv2.cvtColor(region_3, cv2.COLOR_BGR2RGB)
        ax3.imshow(region_3_rgb.astype('uint8'),cmap=plt.cm.gray)
        ax3.set_title("Region 3 image")
        ax3.set_axis_off()
        plt.show()
    return region_1, region_2, region_3

def ProcessTesseract(image,z):
    if z==1:
        image_to_string_result = pytesseract.image_to_string(image, lang="ind+eng",config="--psm 4 --oem 3 -c tessedit_char_whitelist=0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ/-.,:' '")
    elif z==2:
        image_to_string_result = pytesseract.image_to_string(image, lang="eng+ind",config="--psm 6 --oem 3 -c tessedit_char_whitelist=0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ/-.,:' '")
    else:
        image_to_string_result = pytesseract.image_to_string(image, lang="eng+ind",config="--psm 3 --oem 3 -c tessedit_char_whitelist=0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ/-.,:' '")
    if isDebug:
        PrintLog("image to string raw output:")
        PrintLog(image_to_string_result)
    result = Tesseract_CleanText_1(image_to_string_result)
    result = Tesseract_CleanText_2(result)
    image_to_string_result = result.upper()
    timestamp_collector(time.time() - start_time, "ProcessTesseract")
    return image_to_string_result

def ProcessTesseract_MaximumConfidenceLevel1(img, arrayThreshold,z):
    if isDebug:
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        fig1, (ax1) = plt.subplots(1, 1, figsize=(25, 8))
        ax1.imshow(img_rgb.astype('uint8'),cmap=plt.cm.gray)
        ax1.set_title("Raw image")
        ax1.set_axis_off()
        plt.show()
    PrintLog("Checking maximum confidence level 1 on OCR procress...")
    temp_conf =[]
    temp_img  =[]
    img_data_list  =[]
    for i in arrayThreshold:
        threshold = FilterImage_Threshold(img, i, False)
        if z==1:
            #BCA
            #BNI TYPE 2
            img_data = pytesseract.image_to_data(threshold, lang="ind+eng",config="--psm 4 --oem 3 -c tessedit_char_whitelist=0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ/-.,:' '", output_type='data.frame')#BCA
        elif z==2:
            #BNI TYPE 1
            img_data = pytesseract.image_to_data(threshold, lang="eng+ind",config="--psm 6 --oem 3 -c tessedit_char_whitelist=0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ/-.,:' '", output_type='data.frame')
        else:
            #BNI TYPE 2
            img_data = pytesseract.image_to_data(threshold, lang="eng+ind",config="--psm 3 --oem 3 -c tessedit_char_whitelist=0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ/-.,:' '", output_type='data.frame')
        img_data = img_data.dropna()
        total = img_data.sum(axis=0)
        count = img_data.count(axis=0)
        avgConf = total.conf / count.conf
        temp_conf.append(avgConf)
        temp_img.append(threshold)
        img_data_list.append(img_data)
    u = temp_conf.index(max(temp_conf))
    image = temp_img[u]
    image_data = img_data_list[u]
    if isDebug:
        PrintLog("image to data raw output:")
        PrintLog(image_data)
    row = math.ceil(len(arrayThreshold)/3)
    if row==0:
        row+=1
    if isDebug==True:
        fig1, ax = plt.subplots(row, 3, figsize=(25, 20))
        count=0
        for i in range(row):
            for j in range(3):
                if(count<len(temp_img)):
                    tempStr = str(arrayThreshold[count]) + " " + str(np.round(temp_conf[count], 3)) + "%"
                    if(row==1):
                        ax[j].imshow(cv2.cvtColor(temp_img[count],cv2.COLOR_BGR2RGB).astype('uint8'),cmap=plt.cm.gray)
                        ax[j].set_title(tempStr)
                        ax[j].set_axis_off()
                    else:
                        ax[i,j].imshow(cv2.cvtColor(temp_img[count],cv2.COLOR_BGR2RGB).astype('uint8'),cmap=plt.cm.gray)
                        ax[i,j].set_title(tempStr)
                        ax[i,j].set_axis_off()
                    count+=1
                else:
                    if(row==1):
                        ax[j].set_visible(False)
                    else:
                        ax[i,j].set_visible(False)
        plt.subplots_adjust(hspace = 0.1, wspace = 0.1)
        plt.show()
        PrintLog(str(arrayThreshold[u])+ " " + str(temp_conf[u])+ " % is selected")
    timestamp_collector(time.time() - start_time, "ProcessTesseract_MaximumConfidenceLevel1")
    return image, image_data, arrayThreshold[u], temp_conf[u]

def ProcessTesseract_MaximumConfidenceLevel2(img, parameter, lvl1Image, lvl1Conf):
    PrintLog("Checking maximum confidence level 2 on OCR procress...")
    x=2
    temp=[ [parameter[0],parameter[1]],

        [parameter[0]-(3*x),parameter[1]],
            [parameter[0]-(2*x),parameter[1]],
            [parameter[0]-x,parameter[1]],
            [parameter[0]+x,parameter[1]],
            [parameter[0]+(2*x),parameter[1]],
            [parameter[0]+(3*x),parameter[1]]]
    temp_conf=[]
    temp_img=[]
    temp_conf.append(lvl1Conf)
    temp_img.append(lvl1Image)
    for i in range(1,len(temp)):
        threshold = FilterImage_Threshold(img, temp[i], False)
        img_data = pytesseract.image_to_data(threshold,lang="eng+ind",config="--psm 4 --oem 3 -c tessedit_char_whitelist=0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ/-.,:' '", output_type='data.frame')
        img_data = img_data.dropna()
        total = img_data.sum(axis=0)
        count = img_data.count(axis=0)
        avgConf = total.conf / count.conf
        #print("Confidence Level with parameter ",i," : "+str(("%.2f" % avgConf) + " %"))
        temp_conf.append(avgConf)
        temp_img.append(threshold)
    u=temp_conf.index(max(temp_conf))
    image=temp_img[u]
    if isDebug:
        fig1, ax = plt.subplots(3, 3, figsize=(20, 15))
        count=1
        for i in range(3):
            for j in range(3):
                if(i!=1):
                    if(count<len(temp_conf)):
                        ax[i,j].imshow(cv2.cvtColor(temp_img[count],cv2.COLOR_BGR2RGB).astype('uint8'),cmap=plt.cm.gray)
                        tempStr = str(temp[count]) + " " + str(np.round(temp_conf[count], 3)) + "%"
                        ax[i,j].set_title(tempStr)
                        ax[i,j].set_axis_off()
                        count+=1
                    else:
                        break
                else:
                    continue
        ax[1,1].imshow(cv2.cvtColor(temp_img[0],cv2.COLOR_BGR2RGB).astype('uint8'),cmap=plt.cm.gray)
        tempStr = str(temp[0]) + " " + str(np.round(temp_conf[0], 3)) + "%"
        ax[1,1].set_title(tempStr)
        ax[1,1].set_axis_off()
        plt.subplots_adjust(hspace = 0.01, wspace = 0.01)
        fig1.delaxes(ax[1,0])
        fig1.delaxes(ax[1,2])
        plt.show()
        PrintLog(str(temp[u])+" "+ str(temp_conf[u])+ " % is selected")
    timestamp_collector(time.time() - start_time, "ProcessTesseract_MaximumConfidenceLevel2")
    return image,temp[u]

def Tesseract_Image_To_Data_Postprocess(img_data):
    img_data = img_data.dropna()
    n_boxes = len(img_data['text'])
    pd_index = []
    for i in range(n_boxes):
        pd_index.append(i)
    s = pd.Series(pd_index)
    img_data = img_data.set_index([s])
    num = 2
    num2 = 2
    num3 = 2
    text = ""
    for i in range(n_boxes):
        if int(img_data.loc[i, 'block_num']) < num:
            if int(img_data.loc[i, 'line_num']) < num2:
                if int(img_data.loc[i, 'par_num']) < num3:
                    text += img_data.loc[i, 'text'] + " "
                else:
                    num3 += 1
                    text += "\n"
                    text += img_data.loc[i, 'text'] + " "
            else:
                num2 += 1
                text += "\n"
                text += img_data.loc[i, 'text'] + " "
        else:
            num += 1
            text += "\n"
            text += img_data.loc[i, 'text'] + " "
    timestamp_collector(time.time() - start_time, "Tesseract_Image_To_Data_PostProcess")
    return text

def Tesseract_CleanText_1(text):
    '''Make text lowercase, remove text in square brackets, remove punctuation and remove words containing numbers.'''
    text = text.lower()
    text = re.sub('—', '-', text)
    text = re.sub('…', '', text)
    text = re.sub('“', '', text)
    remove = string.punctuation
    remove = remove.replace("-", "")
    remove = remove.replace("/", "")
    remove = remove.replace(".", "")
    remove = remove.replace(":", "")
    remove = remove.replace(",", "")

    remove = remove.replace("|", "")
    pattern = r"[{}]".format(remove)  # create the pattern
    text = re.sub(pattern, "", text)
    #text = re.sub('\w*\d\w*', '', text)
    text = os.linesep.join([s for s in text.splitlines() if s])
    timestamp_collector(time.time() - start_time, "Tesseract_CleanText_1")
    return text



def Tesseract_CleanText_2(text):
    text = ftfy.fix_text(text)
    text = ftfy.fix_encoding(text)
    timestamp_collector(time.time() - start_time, "Tesseract_CleanText_2")
    return text

def ExtractValue_PredefinedForeList(detectedText, predefinedList):
    #print(detectedText)
    result = ["#####"] * len(predefinedList)
    textlines = detectedText.split("\n")
    PrintLog(textlines)
    for textline in textlines:
        for keyword in predefinedList:
            if result[predefinedList.index(keyword)] == "#####":
                if keyword in textline:
                    #result.append(predefinedText," : ")
                    try:
                        textline = textline.split(keyword)
                        textline = textline[-1].split(':')
                        textline = textline[-1].replace("-","")
                        result[predefinedList.index(keyword)] = textline
                        break
                    except:
                        print("Error occurred at ExtractValue_PredefinedForeList")
    if isDebug:
        PrintLog("### Extracted Value ### :")
        PrintLog(result)
    timestamp_collector(time.time() - start_time, "ExtractValue_PredefinedForeList")
    return result

def ExtractValue_PredefinedForeBackList(detectedText, predefinedForeList, predefinedBackList):
    if isDebug:
        PrintLog("### Extracted Value ### :")
    result = ["#####"] * len(predefinedForeList)
    textlines = detectedText.split("\n")
    for textline in textlines:
        for keyword in predefinedForeList:
            if result[predefinedForeList.index(keyword)] == "#####":
                if keyword in textline:
                    a = textline.find(keyword)
                    for gredword in predefinedBackList:
                        if gredword in textline:
                            ### RE, not work, to be done
                            ##reString =  keyword + '(*?)' + gredword
                            ##output = re.search(reString, textline).group(1)
                            b = textline.find(gredword)
                            output = textline[a+len(keyword):b]
                            ## finetune work ##
                            if "T" in output:
                                output = output.replace("T","+")
                            if len(output) < 6:
                                detected = True
                                textline = textline[b+len(gredword):]
                                result[predefinedForeList.index(keyword)] = output
                                if isDebug:
                                    PrintLog(keyword + " : " + " ")
                                    PrintLog(output)
                                break
    return result

def ExtractValue_SpecificPattern(detectedText, regularExpression, returnGroupIndex, deliminator, isRemoveCRLF, isRemoveSpace):
    if isDebug:
        PrintLog("### Extracted Value ### :")
    if isRemoveSpace:
        detectedText = detectedText.replace(" ", "")
    if isRemoveCRLF:
        detectedText = detectedText.replace("\n", " ")
    extractedValue = ""
    try:
        if len(deliminator) > 0:
            textlines = detectedText.split(deliminator)
            for textline in textlines:
                if isDebug:
                    PrintLog("textline : "+ textline)
                result = re.search(regularExpression, textline)
                if result:
                    extractedValue = result.group(returnGroupIndex)
                    if isDebug:
                        PrintLog("extracted : "+ extractedValue)
                    break
        else:
            result = re.search(regularExpression, detectedText)
            if result:
                extractedValue = result.group(returnGroupIndex)
                if isDebug:
                    PrintLog("extracted : "+ extractedValue)
    except:
        if isDebug:
            PrintLog("Error occured in ExtractValue_SpecificPattern")
    timestamp_collector(time.time() - start_time, "ExtractValue_SpecificPattern")
    return extractedValue

def ExtractValue_BetweenLines(textlines,KeywordBeforeLine,KeywordAfterLine,regularExpression):
    textlines=textlines.split("\n")
    a,b=0,0
    for i in range(len(textlines)):
        if(KeywordBeforeLine in textlines[i]):
            a=i
            break
    for i in range(len(textlines)):
        if(KeywordAfterLine in textlines[i]):
            b=i
            break
    value=""
    PrintLog(str(a) + str(b))
    if(b-a==2 or (b==0 and a!=0)):
        for i in (range(len(textlines)-a)):
            result = re.search(regularExpression, textlines[a+i+1])
            if result:
                value = result.group(0)
                if isDebug:
                    PrintLog("extracted : "+ value)
                break
    elif(b-a>2):
        for i in range(a+1,b):
            value+=textlines[i].strip()
    return value

def ExtractValue_LastLine(textlines):
    textlines=textlines.split("\n")
    return textlines[-1]

def Store_CSV(json_export_data):
    filepath = EXPORT_FOLDER_PATH + 'export-data.csv'
    successful = False
    data_file = ""
    try:
        with open(filepath, newline='') as f:
            reader = csv.reader(f)
            row1 = next(reader)
        if(list(json_export_data.keys()) == row1):
            # if it is same header
            data_file = open(filepath, 'a', newline='')
            csv_writer = csv.writer(data_file)
            csv_writer.writerow(json_export_data.values())
        else:
            # if it is different header
            data_file = open(filepath, 'w', newline='')
            csv_writer = csv.writer(data_file)
            header = json_export_data.keys()
            csv_writer.writerow(header)
            csv_writer.writerow(json_export_data.values())
        successful = True
    except:
        PrintLog("CSV exception error")
        data_file = open(filepath, 'w', newline='')
        csv_writer = csv.writer(data_file)
        header = json_export_data.keys()
        csv_writer.writerow(header)
        csv_writer.writerow(json_export_data.values())
    finally:
        data_file.close()
    return successful

def SegmentImage_Logo(img, xmlpath):
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    LogoCascade = cv2.CascadeClassifier(xmlpath)
    found = LogoCascade.detectMultiScale(img_gray, minSize =(20, 20))
    if isDebug:
        PrintLog(str(len(found))+ " Logo is detected")

    # HERE: Need Adrian to finetune the best logo to be reference and processed.
    if len(found)==1:
        x, y, w, h = found[len(found)-1]
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 5)
        length_rectangle,width_retangle = w*6,w*2
        cv2.rectangle(img, (x, y+w), (x + 5, y+w + 5), (255, 0, 0), 2)
        region = img[ y+w:y+width_retangle+w,x:x+length_rectangle]
        if isDebug:
            img_rgb = cv2.cvtColor(region,cv2.COLOR_BGR2RGB)
            fig1, (ax1) = plt.subplots(1, 1, figsize=(100, 100))
            ax1.imshow(img_rgb.astype('uint8'),cmap=plt.cm.gray)
            ax1.set_title("Region")
            ax1.set_axis_off()
            plt.show()
        return region
    return img

def ConvertPDFToImage(filepath):
    file_name = os.path.basename(filepath)
    PrintLog(file_name)
    #output_filepath = OUTPUT_FOLDER_PATH + file_name
    #print(output_filepath)
    PrintLog("Reading PDF file: "+ filepath)
    pages = convert_from_path(filepath, dpi=200)
    #file_name_no_ext = os.path.splitext(file_name)[0]
    #output_filepath = RAW_FOLDER_PATH + file_name_no_ext + '.jpg'
    k=0
    m=[]
    x=[]
    RRR=[]
    file_name_no_ext = os.path.splitext(file_name)[0]
    PrintLog(file_name_no_ext)
    for page in pages:
        output_filepath = RAW_FOLDER_PATH + file_name_no_ext +' '+ str(k) +'.jpg'
        #output_filepath=RAW_FOLDER_PATH + str(k) + '.jpg'
        output_filepath_2 = OUTPUT_FOLDER_PATH + file_name_no_ext +' '+ str(k) +'.jpg'
        page.save(output_filepath,'JPEG')
        page.save(output_filepath_2,'JPEG')
        m.append(output_filepath)
        x.append(output_filepath_2)
        t=Image.open(output_filepath_2)
        f=t.convert('RGB')
        RRR.append(f)
        k+=1
    RRR[0].save(OUTPUT_FOLDER_PATH+'ProcessedPDF.pdf',save_all=True,append_images=RRR[1:])
    return x,OUTPUT_FOLDER_PATH+'ProcessedPDF.pdf',m,file_name_no_ext

def checkNama(nama):
    for s in range (len(nama)):
        if(nama[s].isdigit()):

            return False
    return True

def checkspace(nama):
    c=0
    for s in nama:
        if s==' ':
            c+=1
    return c

def Detect_OCRAFONT(gray,location,t):
    Result=[]
    for (i, (x, y, w, h)) in enumerate(location):
        group = gray[y - 6:y +h + 6, x - 6:x + w + 6]
        #group = cv2.threshold(group, 100, 255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
        digitCnts = cv2.findContours(group.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        digitCnts = imutils.grab_contours(digitCnts)
        digitCnts = contours.sort_contours(digitCnts,method="left-to-right")[0]
        for c in digitCnts:
            (x, y, w, h) = cv2.boundingRect(c)
            roi = group[y:y + h, x:x + w]
            if isDebug:
                fig1, (ax1) = plt.subplots(1, 1, figsize=(25, 8))
                ax1.imshow(roi.astype('uint8'),cmap=plt.cm.gray)
                ax1.set_title("Cropped Region")
                ax1.set_axis_off()
                plt.show()
            if(t==0):
                Number = pytesseract.image_to_string(roi, lang="num_4",config='--psm 6')
            elif(t==1):
                Number = pytesseract.image_to_string(roi, lang="ind",config='--psm 4')
            #print(Number)
            Result.append(str(Number))
    return Result

def Crop_OCRATYPEFONT(image,n):
    RectangleKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (10, 3))
    SquareKernel   =  cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    #print('shape',image.shape)
    if(image.shape[1]>300):
        image      = imutils.resize(image,width=300)
    gray       = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    ImgTophat     = cv2.morphologyEx(gray, cv2.MORPH_TOPHAT, RectangleKernel)
    gradient_X      = cv2.Sobel(ImgTophat, ddepth=cv2.CV_32F, dx=1, dy=0,ksize=-1)
    gradient_X      = np.absolute(gradient_X)
    (minimumvalue, maximumvalue) = (np.min(gradient_X), np.max(gradient_X))
    gradient_X = (255 * ((gradient_X - minimumvalue) / (maximumvalue - minimumvalue)))
    gradient_X = gradient_X.astype("uint8")
    gradient_X = cv2.morphologyEx(gradient_X, cv2.MORPH_CLOSE, RectangleKernel)
    threshold = cv2.threshold(gradient_X, 0, 255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    thresh = cv2.morphologyEx(threshold, cv2.MORPH_CLOSE, SquareKernel)
    cntrs = cv2.findContours(thresh, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    cntrs = imutils.grab_contours(cntrs)
    location = []
    for (i, c) in enumerate(cntrs):
        (x, y, w, h) = cv2.boundingRect(c)
        #bpjs num ,ktp, bpjs cardn num
        #(95>w>70 and 11>h>7 and x>18 and n==0) (47>w>21 and 14>h>8 and y<60 and n==2)
        if ( (110>w>70 and 15>h>5 and y<100 and n==0) or ( 135>w>110 and 14>h>7 and n==1) or  (50>w>21 and 20>h>8 and y<100 and n==2) ): #(47>w>21 and 14>h>8 and y<60 and n==2)):#(38>w>21 and 14>h>8 and n==2)  ) : #bpjs num
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
            location.append((x, y, w, h))
            PrintLog(x+y+w+h)
    location.sort(key=lambda x:x[0])
    number=Detect_OCRAFONT(gray,location,0)
    number=''.join(number)
    if  len(number)!=11 and n==0:
        number=Detect_OCRAFONT(gray,location,1)
    elif n==2 and len(number)!=16:
        number=Detect_OCRAFONT(gray,location,1)

    number=''.join(number)
    PrintLog('number '+str(re.sub("[^0-9]","",number)))
    return re.sub("[^0-9]","",number)
#syarizal

def SegmentImage_3_Region_3(img,img_,area):
    PrintLog(img.shape)
    Temp_img=img.copy()
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    #LogoCascade = cv2.CascadeClassifier('cascade (6)_tanggal_14.xml') cascade ini =cascade sabtu 9
    LogoCascade = cv2.CascadeClassifier('bpjs-cascade.xml')
    found = LogoCascade.detectMultiScale(img_gray, minSize =(20, 20))
    if isDebug and len(found)==1:
        PrintLog(str(len(found))+ " Logo is detected")
        for i in found:
            x,y,w,h=i
            Temp_y=y
    number_region=img
    text_region=img_
    if len(found)==1:
        PrintLog(str(x)+str(y)+str(w)+str(h))
        if(x-3*w<0):
            x_=0
        else:
            x_=x-3*w
        for i in range (5):
            x-=(w/2)
            y-=(w/2)

        y_=y+int(w/2)

        number_region=img[int(y_)-55 : int(y_)-50 + w+int(w/2),x_:x_+5*w]
        #cv2.rectangle(img, (x_,k), (x_ + 5*w, Temp_y), (0, 255, 0), 3)
        text_region=img_[int(y_)-100+ w+int(w/2):Temp_y,x_:x_+5*w]
        if isDebug:
            image_number = cv2.cvtColor(number_region,cv2.COLOR_BGR2RGB)
            image_text = cv2.cvtColor(text_region,cv2.COLOR_BGR2RGB)
            fig1, (ax1, ax2) = plt.subplots(1, 2, figsize=(25, 8))
            ax1.imshow(image_number.astype('uint8'),cmap=plt.cm.gray)
            ax1.set_title("Detected image_number")
            ax1.set_axis_off()
            ax2.imshow(image_text.astype('uint8'),cmap=plt.cm.gray)
            ax2.set_title("Detected text_region")
            ax2.set_axis_off()
            plt.show()
    timestamp_collector(time.time() - start_time, "SegmentImage_3_Region_3")
    return number_region,text_region


def RemovePurpleRegion(img):
    height,width = img.shape[0],img.shape[1]
    for loop1 in range(height):
        for loop2 in range(width):
            r,g,b = img[loop1,loop2]
            img[loop1,loop2] = 0,g,0
    timestamp_collector(time.time() - start_time, "RmovePurplRegion")
    return img

def ChangePixelValue(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    for i in range(gray.shape[0]):
        for j in range(gray.shape[1]):
            if gray[i][j]<70:
                gray[i][j]=0
    timestamp_collector(time.time() - start_time, "ChangePixelValue")
    return gray

def ProcessTesseractOCRA(image,n):
    if(n==1):
        image_to_string_result = pytesseract.image_to_string(image, lang="num_4",config="--psm 6")

        img_data = pytesseract.image_to_data(image,lang="num_4",config="--psm 6", output_type='data.frame')
        #print(img_data)
    else:
        image_to_string_result = pytesseract.image_to_string(image, lang="ind",config="--psm 4")
        img_data = pytesseract.image_to_data(image,lang="ind",config="--psm 6", output_type='data.frame')
        #print(img_data)
    result = Tesseract_CleanText_1(image_to_string_result)
    result = Tesseract_CleanText_2(result)
    image_to_string_result = result.upper()
    img_data = img_data.dropna()
    total = img_data.sum(axis=0)
    count = img_data.count(axis=0)
    avgConf = total.conf / count.conf
    avgConf_str = str(("%.2f" % avgConf) + " %")
    if avgConf < 50:
        PrintLog("===== THIS IMAGE IS STRAIGHTLY NOT ABLE TO BE PROCESSED =====")
        PrintLog("===== ERROR : EXTREMELY LOW CONFIDENCE LEVEL            =====")

    #result = Tesseract_Image_To_Data_Postprocess(img_data)
    #result = Tesseract_CleanText_1(result)
    #result = Tesseract_CleanText_2(result)
    #image_to_data_result = result.upper()
    #image_to_data_image = image
    #if isDebug:
    #    print(image_to_data_result)
    timestamp_collector(time.time() - start_time, "ProcessTesseractOCRA")
    return avgConf_str, image_to_string_result

def ImageColorFilter(image, lowColor, highColor, newColor):
    hsv=cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    #hsv1=cv2.cvtColor(image1,cv2.COLOR_BGR2HSV)

    # Define lower and uppper limits for blue 17,137,176
    # now range is green to blue, still need
    #blue_lo=np.array([1,25,100])
    #blue_hi=np.array([218,255,255])
    blue_lo=np.array(lowColor)
    blue_hi=np.array(highColor)

    # Mask image to only select blue
    mask=cv2.inRange(hsv,blue_lo,blue_hi)
    #mask1=cv2.inRange(hsv1,blue_lo,blue_hi)

    # Change image to white where we found blue
    image[mask>0] = newColor
    timestamp_collector(time.time() - start_time, "ImageColorFilter")
    return image


# def Post_Success(OUTPUT_JSN_FOLDER_PATH, file_name, Conf, BalanceChecking):
#     try:
#         with FTP(host) as ftp :
#             ftp.login(user=user, passwd=password)
#             print(ftp.getwelcome())
#             ftp.cwd('/var/www/html/maybank-ocr/uploads/json/')

#             with open(OUTPUT_JSN_FOLDER_PATH+re.sub('\.','',file_name[:-4])+'.txt', 'rb') as f:
#                 ftp.storbinary('STOR ' + re.sub('\.','',file_name[:-4])+'.json', f)
#             ftp.quit()
#         #post_status_to_webapp = requests.post('https://dev-box.tvextract.com//panggilAku',{'nama_file':file_name, 'conf_lv':Conf , 'calculation':BalanceChecking })
#         post_status_to_webapp = requests.post('http://10.148.0.3:80/index.php/panggilAku',{'nama_file':file_name, 'conf_lv':Conf , 'calculation':BalanceChecking })
#         print("post success")
#         timestamp_collector(time.time() - start_time, "Post_Success")
#     except:
#         Error_Handling(file_name,"Post Json Failed")
#     return True
def Error_Handling(file_name, message):
    #error_message = requests.post('https://dev-box.tvextract.com//panggilAku/index_error',{'nama_file':file_name, 'message':message})
    error_message = requests.post(URL_Error ,{'nama_file':file_name, 'message':message})
    timestamp_collector(time.time() - start_time, "Error_Handling")
    return error_message

def timestamp_collector(ctime, process_name):
    f = open(FILE_NAME_IN_PROCESS, "a")
    f.write(process_name + " took " + str(ctime) + " seconds" + '\n')
    f.close()


def ConvertFileToImageByChris(filepath):
    file_name = os.path.basename(filepath)
    process_filepath = PROCESS_FOLDER_PATH + file_name
    img,list_path = [],[]
    if filepath.lower().endswith(('.png', '.jpg', '.jpeg','.JPG')):
        PrintLog("Reading image file: "+ filepath)
        image = cv2.imread(filepath)#[...,::-1]
        img.append(image)
        file_name = os.path.basename(filepath)
        myfiles = {'image' : open(process_filepath, 'rb')}
        post_status_to_webapp = requests.post(URL_Receive,{'filename':file_name},files=myfiles)
        if isDeploy:
            list_path.append(process_filepath)

    elif filepath.lower().endswith(('.pdf')):
        PrintLog("Reading PDF file: "+ filepath)
        pages = convert_from_path(filepath, dpi=250)
        file_name_no_ext = os.path.splitext(file_name)[0]
        i = 0
        list_path=[]
        for page in pages:
            output_filepath = PROCESS_FOLDER_PATH + file_name_no_ext + '.jpg'
            page.save(output_filepath, 'JPEG')
            image = cv2.imread(output_filepath)
            img.append(image)
            output_filepath = PROCESS_FOLDER_PATH + file_name_no_ext + "_" + str(i) + '.jpg'
            output_filepath2 = PROCESS_FOLDER_PATH + file_name_no_ext + "_" + str(i) + '.jpg'
            send_webapp = URL_WebApp + file_name_no_ext + "_" + str(i) + '.jpg'
            page.save(output_filepath, 'JPEG')
            page.save(output_filepath2, 'JPEG')
            file_name = os.path.basename(filepath)
            test = '/var/www/maybank-ocr-ml/MayBank_TVEXTRACT/process/' + str(file_name_no_ext) + "_" + str(i) + '.jpg'
            myfiles = {'image' : open(test, 'rb')}
            post_status_to_webapp = requests.post(URL_Receive,{'filename':file_name},files=myfiles)
            i = i + 1
            if isDeploy:
                list_path.append(send_webapp)
    elif filepath.lower().endswith(('.tif','.tiff',)):
        PrintLog("Reading image file: "+ filepath)
        img_read = Image.open(filepath) #mandiri.tif[0]dst
        file_name_no_ext = os.path.splitext(file_name)[0]
        for i in range(0,250):
            try:
                img_read.seek(i)
                img_read.save(PROCESS_FOLDER_PATH + file_name_no_ext + "_" + str(i) +'.jpg')
                img.append(cv2.imread(PROCESS_FOLDER_PATH + file_name_no_ext + "_" + str(i) +'.jpg'))
                send_webapp = URL_WebApp + file_name_no_ext + "_" + str(i) + '.jpg'
                try:
                    file_name = os.path.basename(filepath)
                    process_image = PROCESS_FOLDER_PATH + file_name_no_ext + "_" + str(i) + '.jpg'
                    myfiles = {'image' : open(process_image, 'rb')}
                    post_status_to_webapp = requests.post(URL_Receive,{'filename':file_name},files=myfiles)
                    if isDeploy:
                        list_path.append(send_webapp)
                except:
                    message = "Error when stor an image"
                    PrintLog(message)
                i = i + 1
            except :
                message = "tiff cannot be read"
                PrintLog(message)
                break

    else:
        errorMessage = "file cannot be read"
        PrintLog(errorMessage)
    timestamp_collector(time.time() - start_time, "ConvertFileToImageByChris")
    return img, list_path

def Post_Success(OUTPUT_JSN_FOLDER_PATH, file_name, Conf, BalanceChecking):
    try:
        contents = open(OUTPUT_JSN_FOLDER_PATH+re.sub('\.','',file_name[:-4])+'.txt', 'rb').read()
        post_status_to_webapp = requests.post(URL_Receive,{'filename':file_name,'calculation':BalanceChecking, 'json':contents })
        print("post success")
        timestamp_collector(time.time() - start_time, "Post_Success")
    except:
        Error_Handling(file_name,"Post Json Failed")
    return True
