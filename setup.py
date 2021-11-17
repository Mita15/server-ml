import math
from flask import Flask, request
from os import listdir
from os.path import isfile, join
from pdf2image import convert_from_path
import numpy as np
import csv
import cv2
import ftfy
import imutils
import json
import matplotlib.pyplot as plt
import os
import pandas as pd
import pytesseract
import re
import string
import time, datetime
import xml.etree.ElementTree as ET
from PyPDF2 import PdfFileReader, PdfFileWriter
import sys, subprocess
import pikepdf
from matplotlib.pyplot import broken_barh
import calendar
from calendar import monthrange