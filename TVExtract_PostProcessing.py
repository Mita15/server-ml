#TVExtract_PostProcessing.py
'''To restructure the source code using refactoring technique, many occasions we use software design patterns, 
such as singleton, multifacet etc as factoring patterns to improve source code robustness, adaptivity and 
more stable quality code into class structure. This can be achieved using more parameters; and in long run, 
shorter delivery time and higher quality products. Refer to https://refactoring.guru/design-patterns/python'''

# Developer     : Dr Sean Tan, Christian
# Version       : v1.0
# Latest update : 202103182200
# Project       : TVExtract_PostProcessing.py

import math
from flask import Flask, request, json
from os import listdir
from os.path import isfile, join
from pdf2image import convert_from_path
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
import requests
from PIL import Image

import TVExtract_Common
tve_common      = None

def TVExtract_PostProcessing_setCommon(tvextract_common):
    global tve_common
    tve_common = tvextract_common
    print(tve_common, "Created")

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
    tve_common.timestamp_collector(time.time() - tve_common.start_time, "Tesseract_Image_To_Data_PostProcess")
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
    tve_common.timestamp_collector(time.time() - tve_common.start_time, "Tesseract_CleanText_1")
    return text

def Tesseract_CleanText_2(text):
    text = ftfy.fix_text(text)
    text = ftfy.fix_encoding(text)
    tve_common.timestamp_collector(time.time() - tve_common.start_time, "Tesseract_CleanText_2")
    return text

def ExtractValue_PredefinedForeList(detectedText, predefinedList):
    #to get name of the ID card
    result = ["#####"] * len(predefinedList)
    textlines = detectedText.split("\n")
    tve_common.PrintLog(textlines)
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
    if tve_common.IS_DEBUG:
        tve_common.PrintLog("### Extracted Value ### :")
        tve_common.PrintLog(result)
    tve_common.timestamp_collector(time.time() - tve_common.start_time, "ExtractValue_PredefinedForeList")
    return result

def ExtractValue_PredefinedForeBackList(detectedText, predefinedForeList, predefinedBackList):
    #to get name of the ID card
    if tve_common.IS_DEBUG:
        tve_common.PrintLog("### Extracted Value ### :")
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
                                if tve_common.IS_DEBUG:
                                    tve_common.PrintLog(keyword + " : " + " ")
                                    tve_common.PrintLog(output)
                                break
    return result

def ExtractValue_SpecificPattern(detectedText, regularExpression, returnGroupIndex, deliminator, isRemoveCRLF, isRemoveSpace):
    #use to extract values for card and statement
    if tve_common.IS_DEBUG:
        tve_common.PrintLog("### Extracted Value ### :")
    if isRemoveSpace:
        detectedText = detectedText.replace(" ", "")
    if isRemoveCRLF:
        detectedText = detectedText.replace("\n", " ")
    extractedValue = ""
    try:
        if len(deliminator) > 0:
            textlines = detectedText.split(deliminator)
            for textline in textlines:
                if tve_common.IS_DEBUG:
                    tve_common.PrintLog("textline : "+ textline)
                result = re.search(regularExpression, textline)
                if result:
                    extractedValue = result.group(returnGroupIndex)
                    if tve_common.IS_DEBUG:
                        tve_common.PrintLog("extracted : "+ extractedValue)
                    break
        else:
            result = re.search(regularExpression, detectedText)
            if result:
                extractedValue = result.group(returnGroupIndex)
                if tve_common.IS_DEBUG:
                    tve_common.PrintLog("extracted : "+ extractedValue)
    except:
        if tve_common.IS_DEBUG:
            tve_common.PrintLog("Error occured in ExtractValue_SpecificPattern")
    tve_common.timestamp_collector(time.time() - tve_common.start_time, "ExtractValue_SpecificPattern")
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
    tve_common.PrintLog(str(a) + str(b))
    if(b-a==2 or (b==0 and a!=0)):
        for i in (range(len(textlines)-a)):
            result = re.search(regularExpression, textlines[a+i+1])
            if result:
                value = result.group(0)
                if tve_common.IS_DEBUG:
                    tve_common.PrintLog("extracted : "+ value)
                break
    elif(b-a>2):
        for i in range(a+1,b):
            value+=textlines[i].strip()
    return value

def ExtractValue_LastLine(textlines):
    textlines=textlines.split("\n")
    return textlines[-1]