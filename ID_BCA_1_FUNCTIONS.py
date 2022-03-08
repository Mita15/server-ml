from MB_tvxt_common_BCA import *
from ftplib import FTP
import requests
import calendar
from calendar import monthrange
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

FACE_XML_PATH       = XML_FOLDER_PATH  + "haarcascade_frontalface_alt.xml"

OUTPUT_TIME_FOLDER_PATH = TVEXTRACT_FOLDER + "time/"

# By default (server) to retrieve process output file at
# OUTPUT_FOLDER_PATH  = "/var/www/html/tvextract-web/output/"
#Uncheck below if run in local directory
#OUTPUT_FOLDER_PATH   = r"[YOUR LOCAL OUTPUT DIRECTORY]"
OUTPUT_FOLDER_PATH      = "/home/tvx/"
OUTPUT_XLS_FOLDER_PATH  = OUTPUT_FOLDER_PATH + "xls/"
OUTPUT_JSN_FOLDER_PATH  = OUTPUT_FOLDER_PATH + "json/"
OUTPUT_RECON_FOLDER_PATH = OUTPUT_FOLDER_PATH + "recon/"
date_type=4
# pytesseract.pytesseract.tesseract_cmd   = r"/opt/tesseract/./tesseract"                 
# iPDF2IMG_POPPLER_PATH                   = r"C:\\Program Files (x86)\\poppler-0.68.0\\bin"

def CheckDate(TEXT, date_type):
	F=0
	if date_type == 4:
		if ExtractValue_SpecificPattern(TEXT,'^(\d{2}/\d{2}\s|\s\d{2}/\d{2}\s)',0,"",True,False)!='':
			F=1
		elif ExtractValue_SpecificPattern(TEXT,'^(\d{2}[1]\d{2}\s)',0,"",True,False)!='':
			F=1
		elif ExtractValue_SpecificPattern(TEXT,'^(\d{2}[7]\d{2}\s)',0,"",True,False)!='':
			F=1
		# elif ExtractValue_SpecificPattern(TEXT,'^(\d{2}[7][01]\s|\d{2}[7][02]\s|\d{2}[7][03]\s|\d{2}[7][04]\s|\d{2}[7][05]\s|\d{2}[7][06]\s|\d{2}[7][07]\s|\d{2}[7][08]\s|\d{2}[7][09]\s|\d{2}[7][10]\s|\d{2}[7][11]\s|\d{2}[7][12]\s)',0,"",True,False)!='':
		#     F=1
		elif ExtractValue_SpecificPattern(TEXT,'^(\d{2}/\s\d{2}\s)',0,"",True,False)!='':
			F=1
		elif ExtractValue_SpecificPattern(TEXT,'^(\d{2}[1]/\d{2}\s)',0,"",True,False)!='':
			F=1
#         elif ExtractValue_SpecificPattern(TEXT,'^([0-9]\d{2}/\d{2}\s)',0,"",True,False)!='': #118/05
#             F=1
		elif ExtractValue_SpecificPattern(TEXT,'^(\d{2}/\d{2}[0-9]\s)',0,"",True,False)!='': #02/141 #added
			F=1
#         elif ExtractValue_SpecificPattern(TEXT,'^(\d{2}[a-zA-Z0-9]\s\d{2}\s|\d{2}[a-zA-Z0-9]\d{2}\s|\d{3}\s\d{2})',0,"",True,False)!='': #14105 #14305 #14705 #14405 #221 09 #107
#             F=1
#         elif ExtractValue_SpecificPattern(TEXT,'^([A-Za-z.,--_]+\s\d{2}/\d{2})',0,"",True,False)!='': #. 15/05 #MOT #OT MMOT
#             F=1
#         elif ExtractValue_SpecificPattern(TEXT,'^([A-Za-z.,-_\s]\d{2}/\d{2}\s)',0,"",True,False)!='': # 25/07
#             F=1
#         elif ExtractValue_SpecificPattern(TEXT,'^(\d{2}/\d{1}[A-Za-z-.,_]+\s)',0,"",True,False)!='': #01/1D
#             F=1
#         elif ExtractValue_SpecificPattern(TEXT,'^(\d{1}\D/\d{2}\s)',0,"",True,False)!='': #1S/05
#             F=1
#         elif ExtractValue_SpecificPattern(TEXT,'^(\s?\d{2}/\d{1}\s)',0,"",True,False)!='': #12/1
#             F=1
# #         elif ExtractValue_SpecificPattern(TEXT,'^([a-zA-Z.,-_]+\s\d{2}[a-zA-Z0-9]\d{2}\s)',0,"",True,False)!='': #e 30106
# #             F=1
#         elif ExtractValue_SpecificPattern(TEXT,'^([a-zA-Z.,-_]\s\d{2}[a-zA-Z0-9]\d{2}\s)',0,"",True,False)!='': #e 30106
#             F=1
#         elif ExtractValue_SpecificPattern(TEXT,'^(\d{1}/\d{2}\s)',0,"",True,False)!='': #8/08 baru
#             F=1
		# elif ExtractValue_SpecificPattern(TEXT,'^(\d{2}\s/\d{2}/\d{2}\s)',0,"",True,False)!='': #08 updated
		#     F=1
#         elif ExtractValue_SpecificPattern(TEXT,'^(\d{1}\s)',0,"",True,False)!='': #0 baru
#             F=1
#         elif ExtractValue_SpecificPattern(TEXT,'^(\D\d{1}/\s\d{2}\s)|^([A-Z]\d{1}/\s\d{2}\s)',0,"",True,False)!='': #:6/10 baru
#             F=1
#         elif ExtractValue_SpecificPattern(TEXT,'^([A-Za-z]+/[A-Za-z]+\s|\D\d{1}/[a-zA-Z]+\s|\s?[a-zA-Z]+/\D\d{1}\s|\d{2}/\W\s|\s?\d{2}/\D\D\s|[A-Z]/\d{2}\s|\d{1}/[A-Z][A-Z]\s|[A-Z]/\d{1}[A-Z]\s)',0,"",True,False)!='': #U/M #UU/MM #O1/LZ #23// #23/IL #M/OT #M/07 #4/OT #O/1G
#             F=1
#         elif ExtractValue_SpecificPattern(TEXT,'^([a-zA-Z.,-_/]+\s\d{2}/\d{2}\s)',0,"",True,False)!='': #,/X 30/07 #/07 #1/07. #4/0
#             F=1
#         elif ExtractValue_SpecificPattern(TEXT,'^([A-Za-z.,-_:]+\s\d{2}\d{2}\s)',0,"",True,False)!='': #-- 3107 #3107 # 3107
#             F=1
		elif ExtractValue_SpecificPattern(TEXT,'^(\d{2}/\d{2}:\s)',0,"",True,False)!='':
			F=1
		elif ExtractValue_SpecificPattern(TEXT,'^(-\s\d{2}/\d{2}\s|-\s\d{2}[1]\d{2}\s|-\s\d{2}[1]\d{2}\s|[1]\s\d{2}[1]\d{2}\s|[1]\s\d{2}[7]\d{2}\s|[1]\s\d{2}/\d{2}\s)',0,"",True,False)!='':
			F=1
	if F == 1:
		return True
	timestamp_collector(time.time() - start_time, "CheckDate")
	return False

def GetDate(TEXT, date_type):
	Date=''
	if date_type == 4:
		if ExtractValue_SpecificPattern(TEXT,'^(\d{2}/\d{2}\s|\s\d{2}/\d{2}\s)',0,"",True,False)!='':
			Date = ExtractValue_SpecificPattern(TEXT,'^(\d{2}/\d{2}\s|\s\d{2}/\d{2}\s)',0,"",True,False)
		elif ExtractValue_SpecificPattern(TEXT,'^(\d{2}[1]\d{2}\s)',0,"",True,False)!='':
			Date = ExtractValue_SpecificPattern(TEXT,'^(\d{2}[1]\d{2}\s)',0,"",True,False)
		elif ExtractValue_SpecificPattern(TEXT,'^(\d{2}[7]\d{2}\s)',0,"",True,False)!='':
			Date = ExtractValue_SpecificPattern(TEXT,'^(\d{2}[7]\d{2}\s)',0,"",True,False)
		# ini di command supaya deskripsi yang berbentuk -> '3070' tidak terambil
		# elif ExtractValue_SpecificPattern(TEXT,'^(\d{2}[7][01]\s|\d{2}[7][02]\s|\d{2}[7][03]\s|\d{2}[7][04]\s|\d{2}[7][05]\s|\d{2}[7][06]\s|\d{2}[7][07]\s|\d{2}[7][08]\s|\d{2}[7][09]\s|\d{2}[7][10]\s|\d{2}[7][11]\s|\d{2}[7][12]\s)',0,"",True,False)!='':
			# Date = ExtractValue_SpecificPattern(TEXT,'^(\d{2}[7][01]\s|\d{2}[7][02]\s|\d{2}[7][03]\s|\d{2}[7][04]\s|\d{2}[7][05]\s|\d{2}[7][06]\s|\d{2}[7][07]\s|\d{2}[7][08]\s|\d{2}[7][09]\s|\d{2}[7][10]\s|\d{2}[7][11]\s|\d{2}[7][12]\s)',0,"",True,False)
		elif ExtractValue_SpecificPattern(TEXT,'^(\d{2}/\s\d{2}\s)',0,"",True,False)!='':
			Date = ExtractValue_SpecificPattern(TEXT,'^(\d{2}/\s\d{2}\s)',0,"",True,False)
#         elif ExtractValue_SpecificPattern(TEXT,'^([0-9]\d{2}/\d{2}\s)',0,"",True,False)!='': #118/05
#             Date = ExtractValue_SpecificPattern(TEXT,'^([0-9]\d{2}/\d{2}\s)',0,"",True,False)
		elif ExtractValue_SpecificPattern(TEXT,'^(\d{2}/\d{2}[0-9]\s)',0,"",True,False)!='': #02/141 #added
			Date = ExtractValue_SpecificPattern(TEXT,'^(\d{2}/\d{2}[0-9]\s)',0,"",True,False)
		elif ExtractValue_SpecificPattern(TEXT,'^(\d{2}[1]/\d{2}\s)',0,"",True,False)!='':
			Date = ExtractValue_SpecificPattern(TEXT,'^(\d{2}[1]/\d{2}\s)',0,"",True,False)
#         elif ExtractValue_SpecificPattern(TEXT,'^(\d{2}[a-zA-Z0-9]\s\d{2}\s|\d{2}[a-zA-Z0-9]\d{2}\s|\d{3}\s\d{2})',0,"",True,False)!='': #14105 #14305 #14705 #14405 #221 09 #107
# #             Date=ExtractValue_SpecificPattern(TEXT,'^(\d{2}[a-zA-Z0-9]\s\d{2}\s|\d{2}[a-zA-Z0-9]\d{2}\s|\d{3}\s\d{2})',0,"",True,False)
#         elif ExtractValue_SpecificPattern(TEXT,'^([A-Za-z.,--_]+\s\d{2}/\d{2})',0,"",True,False)!='': #. 15/05 #MOT #OT MMOT
#             Date=ExtractValue_SpecificPattern(TEXT,'^([A-Za-z.,--_]+\s\d{2}/\d{2})',0,"",True,False)
#         elif ExtractValue_SpecificPattern(TEXT,'^([A-Za-z.,-_\s]\d{2}/\d{2}\s)',0,"",True,False)!='': # 25/07
#             Date=ExtractValue_SpecificPattern(TEXT,'^([A-Za-z.,-_\s]\d{2}/\d{2}\s)',0,"",True,False)
#         elif ExtractValue_SpecificPattern(TEXT,'^(\d{2}/\d{1}[A-Za-z-.,_]+\s)',0,"",True,False)!='': #01/1D
#             Date=ExtractValue_SpecificPattern(TEXT,'^(\d{2}/\d{1}[A-Za-z-.,_]+\s)',0,"",True,False)
#         elif ExtractValue_SpecificPattern(TEXT,'^(\d{1}\D/\d{2}\s)',0,"",True,False)!='': #1S/05
#             Date=ExtractValue_SpecificPattern(TEXT,'^(\d{1}\D/\d{2}\s)',0,"",True,False)
#         elif ExtractValue_SpecificPattern(TEXT,'^(\s?\d{2}/\d{1}\s)',0,"",True,False)!='': #12/1
#             Date=ExtractValue_SpecificPattern(TEXT,'^(\s?\d{2}/\d{1}\s)',0,"",True,False)
#         elif ExtractValue_SpecificPattern(TEXT,'^([a-zA-Z.,-_]+\s\d{2}[a-zA-Z0-9]\d{2}\s)',0,"",True,False)!='': #e 30106
#             Date=ExtractValue_SpecificPattern(TEXT,'^([a-zA-Z.,-_]+\s\d{2}[a-zA-Z0-9]\d{2}\s)',0,"",True,False)
#         elif ExtractValue_SpecificPattern(TEXT,'^([a-zA-Z.,-_]\s\d{2}[a-zA-Z0-9]\d{2}\s)',0,"",True,False)!='': #e 30106
#             Date=ExtractValue_SpecificPattern(TEXT,'^([a-zA-Z.,-_]\s\d{2}[a-zA-Z0-9]\d{2}\s)',0,"",True,False)
#         elif ExtractValue_SpecificPattern(TEXT,'^(\d{1}/\d{2}\s)',0,"",True,False)!='': #8/08 baru
#             Date = ExtractValue_SpecificPattern(TEXT,'^(\d{1}/\d{2}\s)',0,"",True,False)
		elif ExtractValue_SpecificPattern(TEXT,'^(\d{2}\s\d{2}/\d{2}\s)',0,"",True,False)!='': #08 updated
			Date = ExtractValue_SpecificPattern(TEXT,'^(\d{2}\s)',0,"",True,False)
#         elif ExtractValue_SpecificPattern(TEXT,'^(\d{1}\s)',0,"",True,False)!='': #0 baru
#             Date = ExtractValue_SpecificPattern(TEXT,'^(\d{1}\s)',0,"",True,False)
		elif ExtractValue_SpecificPattern(TEXT,'^(\D\d{1}/\d{2}\s)|^([A-Z]\d{1}/\s\d{2}\s)',0,"",True,False)!='': #:6/10 baru
			Date = ExtractValue_SpecificPattern(TEXT,'^(\D\d{1}/\d{2}\s)|^([A-Z]\d{1}/\s\d{2}\s)',0,"",True,False)
#         elif ExtractValue_SpecificPattern(TEXT,'^([A-Za-z]+/[A-Za-z]+\s|\D\d{1}/[a-zA-Z]+\s|\s?[a-zA-Z]+/\D\d{1}\s|\d{2}/\W\s|\s?\d{2}/\D\D\s|[A-Z]/\d{2}\s|\d{1}/[A-Z][A-Z]\s|[A-Z]/\d{1}[A-Z]\s)',0,"",True,False)!='': #U/M #UU/MM #O1/LZ #23// #23/IL #M/OT #M/07 #4/OT #O/1G
#             Date = ExtractValue_SpecificPattern(TEXT,'^([A-Za-z]+/[A-Za-z]+\s|\D\d{1}/[a-zA-Z]+\s|\s?[a-zA-Z]+/\D\d{1}\s|\d{2}/\W\s|\s?\d{2}/\D\D\s|[A-Z]/\d{2}\s|\d{1}/[A-Z][A-Z]\s|[A-Z]/\d{1}[A-Z]\s)',0,"",True,False)
#         elif ExtractValue_SpecificPattern(TEXT,'^([a-zA-Z.,-_/]+\s\d{2}/\d{2}\s)',0,"",True,False)!='': #,/X 30/07 #/07 #1/07. #4/0
#             Date=ExtractValue_SpecificPattern(TEXT,'^([a-zA-Z.,-_/]+\s\d{2}/\d{2}\s)',0,"",True,False)
#         elif ExtractValue_SpecificPattern(TEXT,'^([A-Za-z.,-_]+\s\d{2}\d{2}\s|\d{2}\d{2}\s|\s\d{2}\d{2}\s)',0,"",True,False)!='': #-- 3107 #3107 # 3107
#             Date = ExtractValue_SpecificPattern(TEXT,'^([A-Za-z.,-_:]+\s\d{2}\d{2}\s)',0,"",True,False)
		elif ExtractValue_SpecificPattern(TEXT,'^(\d{2}/\d{2}:\s)',0,"",True,False)!='':
			Date=ExtractValue_SpecificPattern(TEXT,'^(\d{2}/\d{2}:\s)',0,"",True,False)
			Date=str(Date)
		elif ExtractValue_SpecificPattern(TEXT,'^(-\s\d{2}/\d{2}\s|-\s\d{2}[1]\d{2}\s|-\s\d{2}[1]\d{2}\s|[1]\s\d{2}[1]\d{2}\s|[1]\s\d{2}[7]\d{2}\s|[1]\s\d{2}/\d{2}\s)',0,"",True,False)!='':
			Date = ExtractValue_SpecificPattern(TEXT,'^(-\s\d{2}/\d{2}\s|-\s\d{2}[1]\d{2}\s|-\s\d{2}[1]\d{2}\s|[1]\s\d{2}[1]\d{2}\s|[1]\s\d{2}[7]\d{2}\s|[1]\s\d{2}/\d{2}\s)',0,"",True,False)
	timestamp_collector(time.time() - start_time, "GetDate")
	return Date

def GetDate_WF(TEXT, date_type):
	Date=''
	dsc = 0
	if date_type == 4:
		if ExtractValue_SpecificPattern(TEXT,'^(\d{2}/\d{2}\s|\s\d{2}/\d{2}\s)',0,"",True,False)!='':
			Date = ExtractValue_SpecificPattern(TEXT,'^(\d{2}/\d{2}\s|\s\d{2}/\d{2}\s)',0,"",True,False)
			Date = re.sub(' ','',Date)
			dsc = 0
		elif ExtractValue_SpecificPattern(TEXT,'^(\d{2}/\s\d{2}\s)',0,"",True,False)!='':
			Date = ExtractValue_SpecificPattern(TEXT,'^(\d{2}/\s\d{2}\s)',0,"",True,False)
			Date = re.sub(' ','',Date)
			dsc = 0
#         elif ExtractValue_SpecificPattern(TEXT,'^([0-9]\d{2}/\d{2}\s)',0,"",True,False)!='': #118/05
#             Date = ExtractValue_SpecificPattern(TEXT,'^([0-9]\d{2}/\d{2}\s)',0,"",True,False)
#             Date = re.sub(' ','',Date)
#             dt = list(Date)
#             dt[0]=''
#             Date = ''.join(dt)
#             dsc = 1
		elif ExtractValue_SpecificPattern(TEXT,'^(\d{2}/\d{2}[0-9]\s)',0,"",True,False)!='': #02/141 #added
			Date = ExtractValue_SpecificPattern(TEXT,'^(\d{2}/\d{2}[0-9]\s)',0,"",True,False)
			Date = re.sub(' ','',Date)
			dt = list(Date)
			dt[5]=''
			Date = ''.join(dt)
			dsc = 1
		elif ExtractValue_SpecificPattern(TEXT,'^(\d{2}[1]/\d{2}\s)',0,"",True,False)!='':
			Date = ExtractValue_SpecificPattern(TEXT,'^(\d{2}[1]/\d{2}\s)',0,"",True,False)
			Date = re.sub(' ','',Date)
			dt = list(Date)
			dt[2]=''
			Date = ''.join(dt)
			dsc = 1
#         elif ExtractValue_SpecificPattern(TEXT,'^(\d{2}[a-zA-Z0-9]\s\d{2}\s|\d{2}[a-zA-Z0-9]\d{2}\s|\d{3}\s\d{2})',0,"",True,False)!='': #14105 #14305 #14705 #14405 #221 09 #107
#             Date=ExtractValue_SpecificPattern(TEXT,'^(\d{2}[a-zA-Z0-9]\s\d{2}\s|\d{2}[a-zA-Z0-9]\d{2}\s|\d{3}\s\d{2})',0,"",True,False)
#             Date = re.sub(' ','',Date)
#             dt = list(Date)
#             dt[2]='/'
#             Date = ''.join(dt)
#             dsc = 1
#         elif ExtractValue_SpecificPattern(TEXT,'^([A-Za-z.,--_]+\s\d{2}/\d{2})',0,"",True,False)!='': #. 15/05 #MOT #OT MMOT
#             Date=ExtractValue_SpecificPattern(TEXT,'^([A-Za-z.,--_]+\s\d{2}/\d{2})',0,"",True,False)
#             Date=re.sub(' ','',Date)
#             Date=re.sub('\.','',Date)
#             Date=re.sub(',','',Date)
#             Date=re.sub('-','',Date)
#             Date=re.sub('_','',Date)
#             Date=re.sub('[A-Za-z]','',Date)
#             dsc = 1
#         elif ExtractValue_SpecificPattern(TEXT,'^([A-Za-z.,-_\s]\d{2}/\d{2}\s)',0,"",True,False)!='': # 25/07
#             Date=ExtractValue_SpecificPattern(TEXT,'^([A-Za-z.,-_\s]\d{2}/\d{2}\s)',0,"",True,False)
#             Date=re.sub(' ','',Date)
#             Date=re.sub('\.','',Date)
#             Date=re.sub(',','',Date)
#             Date=re.sub('-','',Date)
#             Date=re.sub('_','',Date)
#             Date=re.sub('[A-Za-z]','',Date)
#             dsc = 1
#         elif ExtractValue_SpecificPattern(TEXT,'^(\d{2}/\d{1}[A-Za-z-.,_]+\s)',0,"",True,False)!='': #01/1D
#             Date=ExtractValue_SpecificPattern(TEXT,'^(\d{2}/\d{1}[A-Za-z-.,_]+\s)',0,"",True,False)
#             Date=re.sub(' ','',Date)
#             dt = list(Date)
#             dt[4]='0'
#             Date = ''.join(dt)
#             dsc = 1
#         elif ExtractValue_SpecificPattern(TEXT,'^(\d{1}\D/\d{2}\s)',0,"",True,False)!='': #1S/05
#             Date=ExtractValue_SpecificPattern(TEXT,'^(\d{1}\D/\d{2}\s)',0,"",True,False)
#             Date=re.sub(' ','',Date)
#             dt = list(Date)
#             dt[1]='5'
#             Date=''.join(dt)
#             dsc = 1
#         elif ExtractValue_SpecificPattern(TEXT,'^(\s?\d{2}/\d{1}\s)',0,"",True,False)!='': #12/1
#             Date=ExtractValue_SpecificPattern(TEXT,'^(\s?\d{2}/\d{1}\s)',0,"",True,False)
#             Date=re.sub(' ','',Date)
#             Date=Date[:4]+'0'
#             dsc = 1
		elif ExtractValue_SpecificPattern(TEXT,'^(\d{2}[1]\d{2}\s)',0,"",True,False)!='':
			Date = ExtractValue_SpecificPattern(TEXT,'^(\d{2}[1]\d{2}\s)',0,"",True,False)
			Date=re.sub(' ','',Date)
			dt = list(Date)
			dt[2]='/'
			Date=''.join(dt)
			dsc = 1
		elif ExtractValue_SpecificPattern(TEXT,'^(\d{2}[7]\d{2}\s)',0,"",True,False)!='':
			Date = ExtractValue_SpecificPattern(TEXT,'^(\d{2}[7]\d{2}\s)',0,"",True,False)
			Date=re.sub(' ','',Date)
			dt = list(Date)
			dt[2]='/'
			Date=''.join(dt)
			dsc = 1
		# elif ExtractValue_SpecificPattern(TEXT,'^(\d{2}[7][01]\s|\d{2}[7][02]\s|\d{2}[7][03]\s|\d{2}[7][04]\s|\d{2}[7][05]\s|\d{2}[7][06]\s|\d{2}[7][07]\s|\d{2}[7][08]\s|\d{2}[7][09]\s|\d{2}[7][10]\s|\d{2}[7][11]\s|\d{2}[7][12]\s)',0,"",True,False)!='':
		#     Date = ExtractValue_SpecificPattern(TEXT,'^(\d{2}[7][01]\s|\d{2}[7][02]\s|\d{2}[7][03]\s|\d{2}[7][04]\s|\d{2}[7][05]\s|\d{2}[7][06]\s|\d{2}[7][07]\s|\d{2}[7][08]\s|\d{2}[7][09]\s|\d{2}[7][10]\s|\d{2}[7][11]\s|\d{2}[7][12]\s)',0,"",True,False)
		#     Date=re.sub(' ','',Date)
		#     dt = list(Date)
		#     dt[2]='/'
		#     Date=''.join(dt)
		#     dsc = 1
#         elif ExtractValue_SpecificPattern(TEXT,'^([a-zA-Z.,-_]\s\d{2}[a-zA-Z0-9]\d{2}\s)',0,"",True,False)!='': #e 30106
#             Date=ExtractValue_SpecificPattern(TEXT,'^([a-zA-Z.,-_]\s\d{2}[a-zA-Z0-9]\d{2}\s)',0,"",True,False)
#             Date = re.sub(' ','',Date)
#             dt = list(Date)
#             dt[0]=''
#             dt[3]='/'
#             Date = ''.join(dt)
#             if Date == ExtractValue_SpecificPattern(Date,'\d{2}/\d{2}[0-9]+',0,"",True,False): #'61/06410' #updated
#                 Date = ExtractValue_SpecificPattern(Date,'\d{2}/\d{2}',0,"",True,False)
#             dsc = 1
#         elif ExtractValue_SpecificPattern(TEXT,'^(\d{1}/\d{2}\s)',0,"",True,False)!='': #8/08 baru
#             Date = ExtractValue_SpecificPattern(TEXT,'^(\d{1}/\d{2}\s)',0,"",True,False)
#             Date = re.sub(' ','',Date)
#             Date = '0'+Date[0:]
#             dsc = 1
		elif ExtractValue_SpecificPattern(TEXT,'^(\d{2}\s\d{2}/\d{2}\s)',0,"",True,False)!='': #08 updated
			Date = ExtractValue_SpecificPattern(TEXT,'^(\d{2}\s)',0,"",True,False)
			Date = re.sub(' ','',Date)
			Date = '01/'+Date[0:]
			dsc = 1
#         elif ExtractValue_SpecificPattern(TEXT,'^(\d{1}\s)',0,"",True,False)!='': #0 baru
#             Date = ExtractValue_SpecificPattern(TEXT,'^(\d{1}\s)',0,"",True,False)
#             Date = re.sub(' ','',Date)
#             Date = '01/0'+Date[0:]
#             dsc = 1
		elif ExtractValue_SpecificPattern(TEXT,'^(\D\d{1}/\d{2}\s)|^([A-Z]\d{1}/\s\d{2}\s)',0,"",True,False)!='': #:6/10 baru
			Date = ExtractValue_SpecificPattern(TEXT,'^(\D\d{1}/\d{2}\s)|^([A-Z]\d{1}/\s\d{2}\s)',0,"",True,False)
			Date = re.sub(' ','',Date)
			dt = list(Date)
			dt[0]='0'
			Date = ''.join(dt)
			dsc = 1
#         elif ExtractValue_SpecificPattern(TEXT,'^([A-Za-z]+/[A-Za-z]+\s|\D\d{1}/[a-zA-Z]+\s|\s?[a-zA-Z]+/\D\d{1}\s|\d{2}/\W\s|\s?\d{2}/\D\D\s|[A-Z]/\d{2}\s|\d{1}/[A-Z][A-Z]\s|[A-Z]/\d{1}[A-Z]\s)',0,"",True,False)!='': #U/M #UU/MM #O1/LZ #23// #23/IL #M/OT #M/07 #4/OT #O/1G
#             Date = ExtractValue_SpecificPattern(TEXT,'^([A-Za-z]+/[A-Za-z]+\s|\D\d{1}/[a-zA-Z]+\s|\s?[a-zA-Z]+/\D\d{1}\s|\d{2}/\W\s|\s?\d{2}/\D\D\s|[A-Z]/\d{2}\s|\d{1}/[A-Z][A-Z]\s|[A-Z]/\d{1}[A-Z]\s)',0,"",True,False)
#             Date = re.sub(' ','',Date)
#             dsc = 1
#         elif ExtractValue_SpecificPattern(TEXT,'^([a-zA-Z.,-_/]+\s\d{2}/\d{2}\s)',0,"",True,False)!='': #,/X 30/07 #/07 #1/07. #4/0
#             Date=ExtractValue_SpecificPattern(TEXT,'^([a-zA-Z.,-_/]+\s\d{2}/\d{2}\s)',0,"",True,False)
#             Date = re.sub(' ','',Date)
#             dt = list(Date)
#             dt[0]=''
#             dt[1]=''
#             dt[2]=''
#             Date = ''.join(dt)
#             Date = re.sub('\.','',Date)
#             if Date == ExtractValue_SpecificPattern(Date,'\d{3}/\d{2}',0,"",True,False): #731/07  #updated
#                 dt = list(Date)
#                 dt[0]=''
#                 Date = ''.join(dt)
#             dsc = 1
#         elif ExtractValue_SpecificPattern(TEXT,'^([A-Za-z.,-_:]+\s\d{2}\d{2}\s|\d{2}\d{2}\s|\s\d{2}\d{2}\s)',0,"",True,False)!='': #-- 3107 #3107 # 3107
#             Date = ExtractValue_SpecificPattern(TEXT,'^([A-Za-z.,-_:]+\s\d{2}\d{2}\s|\d{2}\d{2}\s|\s\d{2}\d{2}\s)',0,"",True,False)
#             Date=re.sub(' ','',Date)
#             Date=re.sub('\.','',Date)
#             Date=re.sub(',','',Date)
#             Date=re.sub('-','',Date)
#             Date=re.sub('_','',Date)
#             Date=re.sub(':','',Date)
#             Date=re.sub('[A-Za-z]','',Date)
#             Date = Date[:2] + '/' + Date[2:]
#             if Date == ExtractValue_SpecificPattern(Date,'\d{2}/\d{2}[0-9]+',0,"",True,False): #'31/103110'  #updated
#                 Date = ExtractValue_SpecificPattern(Date,'\d{2}/\d{2}',0,"",True,False)
#             dsc = 1
		elif ExtractValue_SpecificPattern(TEXT,'^(\d{2}/\d{2}:\s)',0,"",True,False)!='':
			Date=ExtractValue_SpecificPattern(TEXT,'^(\d{2}/\d{2}:\s)',0,"",True,False)
			Date=re.sub(' ','',Date)
			dt = list(Date)
			if dt[2] == '1' or dt[2] == '7':
				dt[2]='/'
			dt[5]=''
			Date = ''.join(dt)
		elif ExtractValue_SpecificPattern(TEXT,'^(-\s\d{2}/\d{2}\s|-\s\d{2}[1]\d{2}\s|-\s\d{2}[1]\d{2}\s|[1]\s\d{2}[1]\d{2}\s|[1]\s\d{2}[7]\d{2}\s|[1]\s\d{2}/\d{2}\s)',0,"",True,False)!='':
			Date = ExtractValue_SpecificPattern(TEXT,'^(-\s\d{2}/\d{2}\s|-\s\d{2}[1]\d{2}\s|-\s\d{2}[1]\d{2}\s|[1]\s\d{2}[1]\d{2}\s|[1]\s\d{2}[7]\d{2}\s|[1]\s\d{2}/\d{2}\s)',0,"",True,False)
			dt = list(Date)
			print(dt)
			if dt[4] != '/':
				dt[4]= '/'
			dt[0] = ''
			dt[1] = ''
			Date = ''.join(dt)
			print(Date)
#         elif ExtractValue_SpecificPattern(result,'^(\d{2}/\d{2}[:]\s)',0,"",True,False)!='':
#             Date=ExtractValue_SpecificPattern(result,'^(\d{2}/\d{2}[:]\s)',0,"",True,False)
#             Date = re.sub(' ','',Date)
#             dt = list(Date)
#             if dt[2] == '1' or dt[2] == '7':
#                 dt[2]='/'
#             dt[5]=''
#             Date = ''.join(dt)
#     timestamp_collector(time.time() - start_time, "GetDate4")
	return Date

# def checkFormat(Date):
# 	year_default = '2020'
# 	try:
# 		date=datetime.datetime.strptime(Date,'%d/%m/%Y').strftime('%d-%m-%Y')
# 		flag=0
# 		if datetime.datetime.strptime(date,'%d-%m-%Y')>datetime.datetime.now():
# 			flag=1
# 	except:
# 		date = Date+'/'+str(year_default)
# 		try :
# 			date=datetime.datetime.strptime(Date,'%d/%m/%Y').strftime('%d-%m-%Y')
# 			flag=1
# 			if datetime.datetime.strptime(date,'%d-%m-%Y')>datetime.datetime.now():
# 				flag=1
# 		except:
# 			date=Date
# 			flag=1
# 	return  date,flag

#17 Jan 2022
def checkFormat(Date):
	# year_default = '2020'
	try:
		date=datetime.datetime.strptime(Date,'%d/%m').strftime('%d-%m')
		flag=0
		if datetime.datetime.strptime(date,'%d-%m')>datetime.datetime.now():
			flag=1
	except:
		# date = Date+'/'+str(year_default)
		try :
			date=datetime.datetime.strptime(Date,'%d/%m').strftime('%d-%m')
			flag=1
			if datetime.datetime.strptime(date,'%d-%m')>datetime.datetime.now():
				flag=1
		except:
			date=Date
			flag=1
	return  date,flag

def getValue(date, s):
	if(ExtractValue_SpecificPattern(s, 'SALDO AWAL', 0, "", True, False) == ''):
		desc = ExtractValue_SpecificPattern(s, date + '(.*?)\d{1,3}\.',1,"",True,False)
		mutasi = ExtractValue_SpecificPattern(s, desc + '(.*?)$',1,"",True,False)
		balance = ExtractValue_SpecificPattern(s, desc + '(.*?)$',1,"",True,False)
	else:
		desc = 'SALDO AWAL'
		mutasi = ExtractValue_SpecificPattern(s, desc + ' (.*?)$',1,"",True,False)
	timestamp_collector(time.time() - start_time, "getValue")
	return desc,mutasi

def getDesc(Description,text) : 
	if ExtractValue_SpecificPattern( text,'',0,"",True,False)!='': 
		Description+= re.sub(ExtractValue_SpecificPattern( text,'',0,"",True,False),'',text)
	else:
		Description+=text
	Description+=' '
	timestamp_collector(time.time() - start_time, "getDesc")
	return Description

def Fillempty(  TED,a,b,c,Result):
	n=0
	Empty = '#####'

	s,e = datetime.datetime.strptime(a, "%d/%m/%Y"), datetime.datetime.strptime(b, "%d/%m/%Y")
	GENERATEDATE = [s + datetime.timedelta(days=x) for x in range(0, (e-s).days)]
	for date in GENERATEDATE:
		if (date.year < datetime.datetime.now().year) or (date.year == datetime.datetime.now().year) :

			if len(Result)==0:
				Result.append([["Date","Description", "CPTY", "Bank CPTY", "Mutation","Balance","Flag"],[datetime.datetime.strptime(date.strftime("%d/%m/%Y"),'%d/%m/%Y').strftime('%d-%m-%Y'),'-', '-', '-', Empty,str(TED[-1]['Balance']),2]])
			else:
				Result.append([["Date","Description", "CPTY", "Bank CPTY", "Mutation","Balance","Flag"],[datetime.datetime.strptime(date.strftime("%d/%m/%Y"),'%d/%m/%Y').strftime('%d-%m-%Y'),'-', '-', '-', Empty,str(Result[-1][1][-1]),2]])
			n=1
		else:
			continue
		
	if n==1:
		Compare_Date=datetime.datetime.strptime(GENERATEDATE[-1].strftime("%d/%m/%Y"),'%d/%m/%Y')+datetime.timedelta(days=1)
	else:
		Compare_Date=datetime.datetime.strptime(c,'%d-%m-%Y')+datetime.timedelta(days=1)
	return Result,Compare_Date.strftime("%d/%m/%Y")

def CheckDesc_Before(TED,n,result1):
	x=0
	for i in range(n+1,len(result1.splitlines())-1):
		if ExtractValue_SpecificPattern(result1.splitlines()[i],'\d{2}/\d{2}',0,"",True,False)!='':
			break
		else:
			TED[-1]['Description']=getDesc(TED[-1]['Description'],result1.splitlines()[i])
			x+=1
	timestamp_collector(time.time() - start_time, "CheckDesc_Before")
	return TED,x



def CheckTransaction(TED,Z,result1,Result,p,f,CM): 
	Date=datetime.datetime.strptime(TED[-1]['Date'],'%d-%m').strftime('%d-%m')
	RDATE=datetime.datetime.strptime(Date,'%d-%m').strftime('%d/%m')  
	m=datetime.datetime.strptime(Date,'%d-%m')+datetime.timedelta(days=1)   
	newdate_c=datetime.datetime.strptime(m.strftime("%d-%m"),'%d-%m').strftime('%d/%m')  
	newdate_c_2=datetime.datetime.strptime(m.strftime("%d-%m"),'%d-%m').strftime('%d-%m')  
	TempDate=getDate_1(RDATE,result1.splitlines()[Z],CM) 
	try:
		TempDate=datetime.datetime.strptime(TempDate,'%d/%m').strftime('%d/%m') 
	except:
		TempDate=newdate_c
	if  m<datetime.datetime.strptime(TempDate,'%d/%m')  and  RDATE!=TempDate:
		Result,Compare_Date=Fillempty(TED,newdate_c,TempDate,newdate_c_2,Result)
		p = 1
	else:
		if RDATE!=TempDate:  
			Compare_Date,p=newdate_c,1
		elif RDATE==TempDate:
			Compare_Date,f=datetime.datetime.strptime(RDATE,'%d/%m').strftime('%d/%m'),1
	compare_date=Compare_Date
	timestamp_collector(time.time() - start_time, "CheckTransaction")
	return Result,compare_date,p,f

def findindex(text,k):
	S=False
	n = 0
	if k==1:
		for i in range(len(text)-1):
			#HEAD CONTENT
				if 'KETERANGAN' in text[i].split(' ') and 'MUTASI' in text[i].split(' ') and 'SALDO' in text[i].split(' '):
					S=True
					
				elif 'MUTASI' in text[i].split(' ') and 'REKENING' in text[i].split(' ') and 'INI.' in text[i].split(' '):
					S=True
					
				elif 'MULASI' in text[i].split(' ') and 'REKENING' in text[i].split(' ') and 'INI.' in text[i].split(' '):
					S=True
					
				elif 'MUTASI' in text[i].split(' ') and 'REKENING' in text[i].split(' ') and 'INI,' in text[i].split(' '):
					S=True
					
				elif 'MUTASI' in text[i].split(' ') and 'REKENING' in text[i].split(' ') and 'INI, I' in text[i].split(' '):
					S=True
				
				elif 'MUTASI' in text[i].split(' ') and 'REKEPING' in text[i].split(' ') and 'INI, I' in text[i].split(' '):
					S=True

				if S:
					if CheckDate(text[i+1],date_type):
						n = i
						break
	else:
		for i in range(len(text)-1):
			try: 
				if CheckDate(text[i+1],date_type):
					n = i
					S=True
					break
			except IndexError:
				message='Keyword Cannot Be Found'
#                 error_message=Error_Handling(file_name,message)
				print(error_message)
#                 sys.exit()
	timestamp_collector(time.time() - start_time, "findindex")
	return n,S

def getDate_2(text):
	Date=''
	if ExtractValue_SpecificPattern(text,'\d{2}/\d{2}',0,"",True,False)!='':
		Date=ExtractValue_SpecificPattern(text,'\d{2}/\d{2}',0,"",True,False)
	if ExtractValue_SpecificPattern(text,'\d{2}/ \d{2}',0,"",True,False)!='':
		Date=ExtractValue_SpecificPattern(text,'\d{2}/ \d{2}',0,"",True,False)
		Date=re.sub(' ', '',Date)
	elif ExtractValue_SpecificPattern(text,r'(\d+/\d+)',0,"",True,False)!='':
		Date=ExtractValue_SpecificPattern(text,r'(\d+/\d+)',0,"",True,False)
		a=Date
		if len(Date)>10:
			Date=''
		else:
			Date=a
	timestamp_collector(time.time() - start_time, "getDate_2")
	return Date

def FirstChecking(text):
	m,n=ExtractValue_SpecificPattern(text,'NO OF CREDIT (\d+)',0,"",True,False),[]
	if m!='':
		y=text.splitlines()
		for i in range(text.splitlines().index(m),text.splitlines().index(m)+5):
			n.append(text.splitlines()[i])
			y.remove(text.splitlines()[i])
		timestamp_collector(time.time() - start_time, "FirstChecking")
		return '\n'.join(y),n
	timestamp_collector(time.time() - start_time, "FirstChecking")
	return text,n

def GetMonthYear(result1,L):
	R,Y='',''
	for j in result1.splitlines():
		if ExtractValue_SpecificPattern(j,'PERIODE : FROM ',0,"",True,False)!='':
			R=j
			break
	if R!='':
		Temp=ExtractValue_SpecificPattern(R,'DECEMBER|MARCH|OCTOBER|SEPTEMBER|FEBRUARY|APRIL|MAY|AUGUST|JUNE|JANUARY|JULY|NOVEMBER',0,"",False,False)
		Y=[L[Temp],ExtractValue_SpecificPattern(R,'\d{4}',0,"",False,False)]
	timestamp_collector(time.time() - start_time, "GetMonthYear")
	return Y    
def getMutationBalance(B,C,D):
	Mutasi=D if re.sub(' ','',C)=='0.00' else C 
	u=list(re.sub(',','.',Mutasi[::-1]))
	u[2]=','
	res=''.join(u)[::-1]
	Mutasi='- '+res if re.sub(' ','',C)=='0.00' else res 
	u=list(re.sub(',','.',B[::-1]))
	u[2]=','
	Balance=''.join(u)[::-1]
	timestamp_collector(time.time() - start_time, "getMutationBalance")
	return Mutasi,Balance

def CalculateConfidenceLevel(X): 
	m,l=[],[]
	for c in X:
		total = c.sum(axis=0)
		count = c.count(axis=0)
		m.append(total.conf)
		l.append(count.conf)
	timestamp_collector(time.time() - start_time, "CalculateConfidenceLevel")
	return sum(m)/sum(l)

def getName(text,file_name):
	name = ''
	periode = ''
	year=''
	norek=''
	found = False
	for i in range(len(text.splitlines())):
		line = text.splitlines()[i]
		if line.find('KCP') > -1 or line.find('KCU') > -1:
			name = text.splitlines()[i+1]
			name = ExtractValue_SpecificPattern(name, "(.*?)" + "NO. REKENING", 1, "", True, False)
			norek = ExtractValue_SpecificPattern(text, "(?:NO. REKENING : | NO. REKENING I | NO. REKENING 3 )(.*?\d* )", 1, "", True, False)
			periode = ExtractValue_SpecificPattern(text,'(?:PERIODE I |PERIODE H | PERIODE : |PERIODE : |PERIODE :  |HAR 4 PERIODE I |\nPERIODE I |PERIODE .| PERIODE 3 |PERIODE 3 )(.*?JANUARI \d{2,4}|FEBRUARI \d{2,4}|MARET \d{2,4}|APRIL \d{2,4}|MEI \d{2,4}|JUNI \d{2,4}|JULI \d{2,4}|AGUSTUS \d{2,4}|SEPTEMBER \d{2,4}|OKTOBER \d{2,4}|NOVEMBER \d{2,4}|DESEMBER \d{2,4})\s|\n',1,"",True,False)
			year = ExtractValue_SpecificPattern(periode,'(?:JANUARI |FEBRUARI |MARET |APRIL |MEI |JUNI |JULI |AGUSTUS |SEPTEMBER |OKTOBER |NOVEMBER |DESEMBER )(.*?\d{4})',1,"",True,False)
			if periode == '':
				periode = ExtractValue_SpecificPattern(text,'(?:PERIODE I | PERIODE : |PERIODE H |PERIODE : |PERIODE :  |HAR 4 PERIODE I |\nPERIODE I |PERIODE . )(.*?JANUARI \d{2,4}|FEBRUARI \d{2,4}|MARET \d{2,4}|APRIL \d{2,4}|MEI \d{2,4}|JUNI \d{2,4}|JULI \d{2,4}|AGUSTUS \d{2,4}|SEPTEMBER \d{2,4}|OKTOBER \d{2,4}|NOVEMBER \d{2,4}|DESEMBER \d{2,4}|JANUARI\d{2,4}|FEBRUARI\d{2,4}|MARET\d{2,4}|APRIL\d{2,4}|MEI\d{2,4}|JUNI\d{2,4}|JULI\d{2,4}|AGUSTUS\d{2,4}|SEPTEMBER\d{2,4}|OKTOBER\d{2,4}|NOVEMBER\d{2,4}|DESEMBER\d{2,4})',1,"",True,False)
				if periode == ExtractValue_SpecificPattern(text,'(?:PERIODE I | PERIODE : |PERIODE H |PERIODE : |PERIODE :  |HAR 4 PERIODE I |\nPERIODE I |PERIODE . )(.*?JANUARI\d{2,4}|FEBRUARI\d{2,4}|MARET\d{2,4}|APRIL\d{2,4}|MEI\d{2,4}|JUNI\d{2,4}|JULI\d{2,4}|AGUSTUS\d{2,4}|SEPTEMBER\d{2,4}|OKTOBER\d{2,4}|NOVEMBER\d{2,4}|DESEMBER\d{2,4})',1,"",True,False):
					year = ExtractValue_SpecificPattern(periode,'(?:JANUARI|FEBRUARI|MARET|APRIL|MEI|JUNI|JULI|AGUSTUS|SEPTEMBER|OKTOBER|NOVEMBER|DESEMBER)(.*?\d{4})',1,"",True,False)
				else :
					year = ExtractValue_SpecificPattern(periode,'(?:JANUARI |FEBRUARI |MARET |APRIL |MEI |JUNI |JULI |AGUSTUS |SEPTEMBER |OKTOBER |NOVEMBER |DESEMBER )(.*?\d{4})',1,"",True,False)
			break
		elif line.find('KCP') > -1 or line.find('KCU') > -1:
			name = text.splitlines()[i+1]
			periode = ExtractValue_SpecificPattern(text,'(?:PERIODE I |PERIODE H |PERIODE : | PERIODE : |PERIODE :  |HAR 4 PERIODE I |\nPERIODE I |PERIODE . )(.*?JANUARI \d{2,4}|FEBRUARI \d{2,4}|MARET \d{2,4}|APRIL \d{2,4}|MEI \d{2,4}|JUNI \d{2,4}|JULI \d{2,4}|AGUSTUS \d{2,4}|SEPTEMBER \d{2,4}|OKTOBER \d{2,4}|NOVEMBER \d{2,4}|DESEMBER \d{2,4})',1,"",True,False)
			year = ExtractValue_SpecificPattern(periode,'(?:JANUARI |FEBRUARI |MARET |APRIL |MEI |JUNI |JULI |AGUSTUS |SEPTEMBER |OKTOBER |NOVEMBER |DESEMBER )(.*?\d{4})',1,"",True,False)
#             if (periode == '' and name == '') or (periode == '' and name !='') or (periode !='' and name == ''):
#                 found=False
#             else :
#                 found=True
			break
		# else :
		# 	message='Data Does Not Match'
			# PrintLog(message)
		# 	print(message)
		   #  error_message=Error_Handling(file_name,message)
		   #  sys.exit()
	# timestamp_collector(time.time() - start_time, "getName")        
	return name,periode,norek,year,found
	
def StoreCSV(TED,extractedResult,userdefinedlist,file_name):
	ColumnName =  ["PERIODE", "NAMA","BANK","CURRENCY","EXCHANGE","ACCOUNT NO","Date","Description", "CPTY", "Bank CPTY","Mutation","Balance"]
	
	S=[{
		'PERIODE':extractedResult[0],
		'NAMA':extractedResult[1],
		'BANK':extractedResult[2],
		'CURRENCY':extractedResult[3],
		'EXCHANGE':extractedResult[4],
		'ACCOUNT NO':extractedResult[5],
		'Date':TED[0]['Date'],
		'CPTY':TED[0]['CPTY'],
		'Bank CPTY':TED[0]['Bank CPTY'],
		'Description':TED[0]['Description'],
		'Mutation':TED[0]['Mutation'],
		'Balance':TED[0]['Balance']}]
	with open(OUTPUT_CSV_FOLDER_PATH+file_name+'.csv','w',newline='') as f:   
		wr = csv.DictWriter(f, fieldnames = ColumnName) 
		wr.writeheader() 
		wr.writerows(S)
	with open(OUTPUT_CSV_FOLDER_PATH+file_name+'.csv','a+',newline='') as f: 
		wr = csv.DictWriter(f, fieldnames = ColumnName) 
		wr.writerows(TED[1:])
		
def Text_Cleaner(text):
	text=re.sub(";EUR'“BWXL%-","",text)
	text=re.sub(";EZ&”&XL i:-g:;%':gg%%%g%","",text)
	text=re.sub(";EZ&%“XL%-%:;%':Q&'","",text)
	text=re.sub(";EZ&%“L%-E:;","",text)
	text=re.sub(";EZ&%“L&:L&ZS&%&'","",text)
	text=re.sub('“','',text)
	text=re.sub(',','',text)
	text=re.sub(';','',text)
	timestamp_collector(time.time() - start_time, "Text_Cleaner")
	return text

def GetNextDate(k,result1):
	for c in range(k,len(result1.splitlines())):
		if getDate_2(result1.splitlines()[c])!='':
			Date=getDate_2(result1.splitlines()[c]) 
			try:
				Date=datetime.datetime.strptime(Date,'%d/%m').strftime('%d/%m')
				timestamp_collector(time.time() - start_time, "GetNextDate")
				return Date
			except:
				print("Error occurred when getting a date")

def RemoveFooter(result1):
	x=result1.splitlines()
	T=[]

	y=re.sub('\n','',ExtractValue_SpecificPattern(result1, 'SALDO AWAL (.*?)\n|SALDO AML (.*?)\n',0,'',False,False))
	if y in x:
		index = x.index(y)
		for z in range(index,len(x)):
			T.append(result1.splitlines()[z])
			x.remove(result1.splitlines()[z])
	y=re.sub('\n','',ExtractValue_SpecificPattern(result1, 'BERSAMBUNG KE HALAMAN BERIKUT',0,'',False,False))
	if y in x:
		index = x.index(y)
		for z in range(index,len(x)):
			T.append(result1.splitlines()[z])
			x.remove(result1.splitlines()[z])
	y=re.sub('\n','',ExtractValue_SpecificPattern(result1, 'MUTASI CR (.*?)\n|MTASI CR (.*?)\n|MUITASI CR (.*?)\n',0,'',False,False))
	if y in x:
		index = x.index(y)
		for z in range(index,len(x)):
			T.append(result1.splitlines()[z])
			x.remove(result1.splitlines()[z])
	y=re.sub('\n','',ExtractValue_SpecificPattern(result1, 'MUTASI DB (.*?)\n|MJITASI DB (.*?)\n|MUITASI DB (.*?)\n',0,'',False,False))
	if y in x:
		index = x.index(y)
		for z in range(index,len(x)):
			T.append(result1.splitlines()[z])
			x.remove(result1.splitlines()[z])
	y=re.sub('\n','',ExtractValue_SpecificPattern(result1, 'SALDO AKHIR (.*?)\n|SALDO AKHI R (.*?)\n',0,'',False,False))
	if y in x:
		index = x.index(y)
		for z in range(index,len(x)):
			T.append(result1.splitlines()[z])
			x.remove(result1.splitlines()[z])
	timestamp_collector(time.time() - start_time, "RemoveFooter")
	return '\n'.join(x), '\n'.join(T)
	
def CalculateBalance(Temp_Mutasi, Temp_Balance, Temp_Date):
	j,idxx=[],[]
	for i in Temp_Date:
		j.append(i[3:])
	for g in set(j):
		idxx.append(len(j)-list(reversed(j)).index(g)-1)
	idxx.sort()
	s=1
	for m in range(1,len(idxx)):
		for h in range(s,idxx[m]+1):
			a,b,c = '','',''
			try:
				a,b,c = re.sub('\.','', re.sub('\,','', Temp_Mutasi[h])),re.sub('\.','', re.sub('\,','', Temp_Balance[h-1])),re.sub('\.','', re.sub('\,','', Temp_Balance[h]))
				try:
					if (int(a)+int(b))!=int(c):
						print(a,b,c)
						print('NOT Balanced')
						timestamp_collector(time.time() - start_time, "CalculateBalance")
						return 'NOT BALANCED'
				except:
					print("Error when Calculating")
					print(a,b,c)
					timestamp_collector(time.time() - start_time, "CalculateBalance")
					return 'NOT BALANCED'
			except:
				print("Error when Converting")
				print(a,b,c)
				timestamp_collector(time.time() - start_time, "CalculateBalance")
				return 'NOT BALANCED'
		s=idxx[m]+1
	timestamp_collector(time.time() - start_time, "CalculateBalance")
	return 'BALANCE'

def getCPTY(desc, bank,text):
	BankCPTY, CPTY = '-', '-'
	List_Bank = ['MANDIRI','MAYBANK', 'BCA', 'BNI', 'BRI', 'PERMATA', 'DANAMON', 'CIMB', 'CIMB NIAGA', 'PANIN', 'OCBC']
	List_Bank.remove("BCA")
	Detected_Bank = ExtractValue_SpecificPattern(desc, "LLG-(.*?)\d", 1, "", False, False)

	if(Detected_Bank != ''):
		BankCPTY = Detected_Bank
		CPTY = ExtractValue_SpecificPattern(desc, BankCPTY + "\d{4} (.*?) \d", 1, "", False, False)

	else:
		if CPTY != '':
			CPTY = text
		else:
			CPTY = '-'
	timestamp_collector(time.time() - start_time, "getCPTY")
	return BankCPTY, CPTY


def cleanExtracted(list_x):
	list_y = []
	CUT_MONTH = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']
	MONTH = ['JANUARI', 'FEBRUARI', 'MARET', 'APRIL', 'MEI', 'JUNI', 'JULI', 'AGUSTUS', 'SEPTEMBER', 'OKTOBER', 'NOVEMBER', 'DESEMBER']
	CurrencyCode = ['AED', 'AFN', 'ALL', 'AMD', 'ANG', 'AOA', 'ARS', 'AUD', 'AWG', 'AZN', 'BAM', 'BBD', 'BDT', 'BGN', 'BHD', 'BIF', 'BMD', 'BND', 'BOB', 'BOV', 'BRL', 'BSD', 'BTN', 'BWP', 'BYN', 'BZD', 'CAD', 'CDF', 'CHE', 'CHF', 'CHW', 'CLF', 'CLP', 'CNY', 'COP', 'COU', 'CRC', 'CUC', 'CUP', 'CVE', 'CZK', 'DJF', 'DKK', 'DOP', 'DZD', 'EGP',
				'ERN', 'ETB', 'EUR', 'FJD', 'GBP', 'GEL', 'GHS', 'GIP', 'GMD', 'GNF', 'GTQ', 'GYD', 'HKD', 'HNL', 'HRK', 'HTG', 'HUF', 'IDR', 'ILS', 'INR', 'IQD', 'IRR', 'ISK', 'JMD', 'JOD', 'JPY', 'KES', 'KGS', 'KHR', 'KMF', 'KPW', 'KYD', 'KZT', 'LAK', 'LBP', 'LKR', 'LRD', 'LSL', 'LYD', 'MAD', 'MDL', 'MGA', 'MKD', 'MMK', 'MNT', 'MOP', 
				'MRU', 'MUR', 'MVR', 'MWK', 'MXN', 'MXV', 'MZN', 'NAD', 'NGN', 'NIO', 'NOK', 'NPR', 'NZD', 'OMR', 'PAB', 'PEN', 'PGK', 'PHP', 'PKR', 'PLN', 'PYG', 'QAR', 'RON', 'RSD', 'RUB', 'RWF', 'SAR', 'SBD', 'SCR', 'SDG', 'SEK', 'SGD', 'SHP', 'SLL', 'SOS', 'SRD', 'SSP', 'STN', 'SVC', 'SYP', 'SZL', 'THB', 'TJS', 'TMT', 'TND', 'TOP', 
				'TRY', 'TTD', 'TWD', 'TZS', 'UAH', 'UGX', 'USD', 'USN', 'UYI', 'UYU', 'UZS', 'VEF', 'VND', 'VUV', 'WST', 'XAF', 'XCD', 'XDR', 'XOF', 'XPF', 'XSU', 'XUA', 'YER', 'ZAR', 'ZMW', 'ZWL']

	for i in range(len(list_x)):
		n = 0
		temp = list_x[i]
		temp = re.sub(',', '', temp)
		temp = re.sub('\.', '', temp)
		temp = (' '.join(temp.split()))
		
		if i == 3:
			for j in range(len(CurrencyCode)):
				if ExtractValue_SpecificPattern(temp, CurrencyCode[j], 0, "", True, False) != "":
					temp = ExtractValue_SpecificPattern(temp, CurrencyCode[j], 0, "", True, False)
		list_y.append(temp)
	timestamp_collector(time.time() - start_time, "cleanExtracted")
	return list_y

def ReconCalculation(Result, data):
	j,idx,s=[],[],0
	Balance = []
	for i in range(len(Result)):
		try:
			int(Result[i][1][0][3:5])
			j.append(Result[i][1][0][3:5])
		except:
			j.append(Result[i][1][0][3:6])
	for g in set(j):
		idx.append(len(j)-list(reversed(j)).index(g)-1)
	idx.sort()
	months = list(set(j))
	for m in range(len(months)):
		found = 0
		for mon in range(len(data)):
			print(list(set(j))[m])
			if int(data[mon][0]) == int(months[m]) and found == 0:
				found = 1
				balance_check = float(data[mon][1])
				end_balance = float(data[mon][2])
				for h in range(s,idx[m]+1):
					a, b =re.sub(' ','',re.sub('\,','.',re.sub('\.','',Result[h][1][4]))), re.sub(' ','',re.sub('\,','.',re.sub('\.','',Result[h][1][5])))
					if( Result[h][1][6] == 2):
						# Result[h][1][6] = 0
						continue
					
					try:
						balance_check += float(a)
						d = float(b)
						
					except:
						print("Error when Calculation in line", h)
						print(a,b)
						print(balance_check)
						Result[h][1][6] = 3
						break
					if balance_check != d:
						Result[h][1][6] = 3
						break
				if(balance_check != end_balance):
					Balance.append("MONTH " + str(data[mon][0]) + " NOT BALANCED")
					print(balance_check, end_balance)
				else:
					Balance.append("MONTH " + str(data[mon][0]) + " BALANCED")

		if found == 0:
			Result, Balance = CalculateBalanceAlt(Result, Balance,str(months[m]),  s+1,idx[m]+1)
		s=idx[m]+1
	timestamp_collector(time.time() - start_time, "ReconCalculation")
	return Balance, Result

def CalculateBalanceAlt(Result, Balance, month, start, end):
	j,idxx=[],[]
	for i in range(len(Result)):
		j.append(Result[i][1][0][3:])
	for g in set(j):
		idxx.append(len(j)-list(reversed(j)).index(g)-1)
	idxx.sort()
	s=1
	for h in range(start,end):
		a,b,c = re.sub('\.','', re.sub('\,','', Result[h][1][4])),re.sub('\.','', re.sub('\,','', Result[h-1][1][5])),re.sub('\.','', re.sub('\,','', Result[h][1][5]))
		try:
			if (int(a)+int(b))!=int(c):
				print(a,b,c)
				print('NOT Balanced')
				Result[h][1][6] = 3
				Balance.append("MONTH" + month + "NOT BALANCED")
				break
		except:
			print("Error when Calculating")
			print(a,b,c)
			Result[h][1][6] = 3
			Balance.append("MONTH " + month + " NOT BALANCED")
			break
	Balance.append("MONTH " + month + " BALANCED")
	
	timestamp_collector(time.time() - start_time, "CalculateBalanceAlt")
	return Result, Balance
def getDate_1(date,text,x):
	if ExtractValue_SpecificPattern(text,'\d{2,3}/\d{2,3}',0,"",True,False)!='':
		Temp=ExtractValue_SpecificPattern(text,'\d{2,3}/\d{2,3}',0,"",True,False)
		if int(Temp[0:2])<int(date[0:2]):
			s=ExtractValue_SpecificPattern(text,r'(\d+/\d+)',0,"",True,False)
			Date='' if len(s)>10 else s[0:2]+date[2:]
		else:
			Date=ExtractValue_SpecificPattern(text,'\d{2,3}/\d{2,3}',0,"",True,False)          
	timestamp_collector(time.time() - start_time, "getDate_1")
	return Date
# def Fillempty_first(a,b,Result, Balance):
# 	Empty = '#####'
# 	s = datetime.datetime.strptime(a, "%d-%m-%Y")
# 	e = datetime.datetime.strptime(b, "%d-%m-%Y")
 
# 	GENERATEDATE = [s + datetime.timedelta(days=x) for x in range(0, (e-s).days)]
# 	a=[]
# 	for date in GENERATEDATE:
# 		a.append([["Date","Description", "CPTY", "Bank CPTY", "Mutation","Balance", "Flag"],[datetime.datetime.strptime(date.strftime("%d/%m/%y"),'%d/%m/%y').strftime('%d-%m-%Y'),'-','-','-', Empty,str(Balance), 2]])
# 	return a

#17 Jan 2022
def Fillempty_first(a,b,Result, Balance):
	Empty = '#####'
	s = datetime.datetime.strptime(a, "%d-%m")
	e = datetime.datetime.strptime(b, "%d-%m")
 
	GENERATEDATE = [s + datetime.timedelta(days=x) for x in range(0, (e-s).days)]
	a=[]
	for date in GENERATEDATE:
		a.append([["Date","Description", "CPTY", "Bank CPTY", "Mutation","Balance", "Flag"],[datetime.datetime.strptime(date.strftime("%d/%m"),'%d/%m').strftime('%d-%m'),'-','-','-', Empty,str(Balance), 2]])
	return a

# def FillingEmpty(Result):
# 	Filled_Result = []
# 	Empty = '#####'
# 	for i in range(len(Result)):
# 		if i==len(Result)-1:
# 			Filled_Result.append(Result[i])
# 		else:
# 			s = datetime.datetime.strptime(Result[i][1][0], "%d-%m-%Y")
# 			e = datetime.datetime.strptime(Result[i+1][1][0], "%d-%m-%Y")
# 			Filled_Result.append(Result[i])
# 			if (e-s).days > 1:
# 				GENERATEDATE = [s + datetime.timedelta(days=x) for x in range(1, (e-s).days)]
# 				for date in GENERATEDATE:
# 					Filled_Result.append([["Date","Description", "CPTY", "Bank CPTY", "Mutation","Balance", "Flag"],[datetime.datetime.strptime(date.strftime("%d/%m/%y"),'%d/%m/%y').strftime('%d-%m-%Y'),'-','-','-', Empty,Result[i][1][5], 2]])            
# 	return Filled_Result

#17 Jan 2022
def FillingEmpty(Result):
	Filled_Result = []
	Empty = '#####'
	for i in range(len(Result)):
		if i==len(Result)-1:
			Filled_Result.append(Result[i])
		else:
			s = datetime.datetime.strptime(Result[i][1][0], "%d-%m")
			e = datetime.datetime.strptime(Result[i+1][1][0], "%d-%m")
			Filled_Result.append(Result[i])
			if (e-s).days > 1:
				GENERATEDATE = [s + datetime.timedelta(days=x) for x in range(1, (e-s).days)]
				for date in GENERATEDATE:
					Filled_Result.append([["Date","Description", "CPTY", "Bank CPTY", "Mutation","Balance", "Flag"],[datetime.datetime.strptime(date.strftime("%d/%m"),'%d/%m').strftime('%d-%m'),'-','-','-', Empty,Result[i][1][5], 2]])            
	return Filled_Result

def CheckDateN(line):
    # if ExtractValue_SpecificPattern(line, "\d{2}/\d{2}", 0, "", True, False) != "" and ExtractValue_SpecificPattern(line, "TANGGAL :\d{2}/\d{2}", 0, "", True, False) == "":
    #     return True
    #19 Jan 2022
    if ExtractValue_SpecificPattern(line, "^(\d{2}/\d{2}\s)", 0, "", True, False) != "" and ExtractValue_SpecificPattern(line, "TANGGAL :\d{2}/\d{2}", 0, "", True, False) == "":
        return True

def convertStrMoney(s):
    money = ''
    c1 = 0
    c2 = 0
    s = re.sub('\.|,', '', s)
    s = s[::-1]
    for i in range(len(s)):
        money+=s[i]

        c1+=1
        if c1 == 2:
            money += '.'

        elif c1 > 2:
            c2+=1
            if c2%3 == 0 and c2 != 0 and i != len(s)-1:
                money += ','
    return money[::-1]
    
def getValueN(n):
    date, desc, mutasi, saldo = '', '', '', ''
    # date = ExtractValue_SpecificPattern(n, "\d{2}/\d{2}", 0, "", True, False)
    # desc = ExtractValue_SpecificPattern(n, date + "\s(.*?)\d{1,3},", 1,'', True, False)
    #19 Jan 2022
    date = ExtractValue_SpecificPattern(n, "^(\d{2}/\d{2}\s)", 0, "", True, False)
    desc = ExtractValue_SpecificPattern(n, date + "(.*?)\d{1,3},", 1,'', True, False)
    mutasi = ExtractValue_SpecificPattern(n, desc + "[\d{1,3},]*\d{1,3}\.\d{2}", 0,'', True, False)
    if ExtractValue_SpecificPattern(desc, "[\d{1,3},]*\d{1,3}\.\d{2}", 0,'', True, False) != "":    
        desc = ExtractValue_SpecificPattern(n, date + "\s(.*?)\d{1,3}\.|,", 1,'', True, False)
        mutasi = ExtractValue_SpecificPattern(n, desc + "[\d{1,3},]*\d{1,3}\.\d{2}", 0,'', True, False)
    mutasi = re.sub(desc, "", mutasi)

    if ExtractValue_SpecificPattern(n, "DB", 0,'', True, False):
        mutasi2 = "-"+mutasi
    else:
        mutasi2 = mutasi
    n = re.sub(" DB", "", n)
    saldo = ExtractValue_SpecificPattern(n, mutasi + "(.*?)$", 1,'', True, False)

    return date, desc.lstrip(' '), mutasi2.lstrip(' '), saldo.lstrip(' ')


def getDescN(Description,text) :
    if ExtractValue_SpecificPattern( text,'\d{2}/\d{2}',0,"",True,False)=='': 
        Description+=' '
        Description+=text
    else:
        Description+= re.sub(ExtractValue_SpecificPattern(text,'\d{2}/\d{2}/\d{2}',0,"",True,False),'',text)
    return Description

def getCPTYN(desc, bank, name):
    BankCPTY, CPTY = '-', '-'
    Detected_CPTY = ''
    Detected_Bank = []

    List_Bank = ['MANDIRI','MAYBANK', 'BCA', 'BNI', 'BRI', 'PERMATA', 'DANAMON', 'CIMB', 'PANIN', 'OCBC', 'HSBC', 'UOB', 'CITIBANK']
    List_Bank.remove(bank)
    desc = desc.split()
    Detected_Bank = list(set(desc)&set(List_Bank))
    if(len(Detected_Bank) != 0):
        BankCPTY = str(Detected_Bank[0])
    return BankCPTY, CPTY

def Fillempty_firstN(a,b,Result, Balance):
    Empty = '#####'
    s = datetime.datetime.strptime(a, "%d-%m")
    e = datetime.datetime.strptime(b, "%d-%m")
 
    GENERATEDATE = [s + datetime.timedelta(days=x) for x in range(0, (e-s).days)]
    Result=[]
    for date in GENERATEDATE:
        Result.append([["Date","Description", "CPTY", "Bank CPTY", "Mutation","Balance", "Flag"],[datetime.datetime.strptime(date.strftime("%d/%m"),'%d/%m').strftime('%d-%m'),'-','-','-', Empty,str(Balance), 2]])
    return Result

def FillingEmptyN(Result):
    n=0
    Filled_Result = []
    # Empty = '#####'
    Empty = '-'
    for i in range(len(Result)):
        if i==len(Result)-1:
            Filled_Result.append(Result[i])
            
            day = Result[i][1][0][:2]
            month = Result[i][1][0][3:5]
            daystofill = 0
            try:
                year = Result[i][1][0][6:]
                unused, daystofill = calendar.monthrange(int(year),int(month))
            
            except:
                today = datetime.datetime.now()
                unused, daystofill = calendar.monthrange(today.year,int(month))
            if int(day) < int(daystofill):
                print(daystofill)
                todate = str(daystofill) + Result[i][1][0][2:]
                print(Result[i][1][0], '|', todate)
                s = datetime.datetime.strptime(Result[i][1][0], "%d-%m")
                e = datetime.datetime.strptime(todate , "%d-%m")
                GENERATEDATE = [s + datetime.timedelta(days=x) for x in range(1, (e-s).days)]
                for date in GENERATEDATE:
                    Filled_Result.append([["Date","Description","CPTY","Bank CPTY","Mutation","Balance", "Flag"],[datetime.datetime.strptime(date.strftime("%d/%m"),'%d/%m').strftime('%d-%m'),'-','-','-', Empty,Result[i][1][3], 2]])
                Filled_Result.append([["Date","Description","CPTY","Bank CPTY","Mutation","Balance", "Flag"],[todate,'-','-','-', Empty,Result[i][1][3], 2]])
        else:
            # print("Date : ", Result[i][1][0], '|', Result[i+1][1][0])
            s = datetime.datetime.strptime(Result[i][1][0], "%d-%m")
            e = datetime.datetime.strptime(Result[i+1][1][0], "%d-%m")
            Filled_Result.append(Result[i])
            if (e-s).days > 1:
                GENERATEDATE = [s + datetime.timedelta(days=x) for x in range(1, (e-s).days)]
                for date in GENERATEDATE:
                    Filled_Result.append([["Date","Description","CPTY","Bank CPTY","Mutation","Balance", "Flag"],[datetime.datetime.strptime(date.strftime("%d/%m"),'%d/%m').strftime('%d-%m'),'-','-','-', Empty,Result[i][1][3], 2]])
    return Filled_Result

# SEBELUM DEPLOY, LIAT DULU CEKDATE SAMPE CEKFORMATDATE
def PROCESS_ID_BCA_TYPE_1():
    
    Temp_Mutasi, Temp_Balance, Temp_Date,List_Path, MONTHYEAR,Temp_Debit,Temp_Credit,Temp_Result,Result,JJ,TED,Temp_Img_Data,Temp_Footer,Results,temp_date=[],[],[],[],[],[],[],[],[],[],[],[], [], [], []
    arrayThreshold=[[300,cv2.THRESH_TRUNC]]
#     arrayThreshold=[[250,cv2.THRESH_TRUNC],[255,cv2.THRESH_TRUNC],[260,cv2.THRESH_TRUNC],[300,cv2.THRESH_TRUNC]]
    r=[]
    TED=[]
    Total_Result_2=[]
    Total_Result2=[]
    Total_Result=[]
    Temp_Result=[]
    Temp_Footer=[]
    Temp_Img_Data=[]
    Temp_Debit=[]
    Temp_Credit=[]
    Temp_Mutasi=[]
    Temp_Balance=[]
    Temp_Date=[]
    Total_Result = []
    Result=[]
    Result2=[]
    Result3=[]
    Result4=[]
    FLAG=[]
    flag_=0
    DATE1,MONTH1=[],[]
    DATE,MONTH=[],[]
    p,f,compare_date=0,0,''
    Empty = '-'
    Date=''
    Description = ''
    Test_CPTY,Month='',''
    Mutasi = 0
    Balance = 0
    first_page = 0
    listpath = []
    start_counting, Check_Balance, found = False, '', False
    DIC={'JANUARY':'01','FEBRUARY':'02', 'MARCH':'03','APRIL':'04', 'MAY':'05','JUNE':'06', 'JULY':'07', 'AUGUST':'08','SEPTEMBER':'09','OCTOBER':'10', 'NOVEMBER':'11',
         'DECEMBER':'12'}
    filepath = ReadFile(-1)
    file_name = os.path.basename(filepath)
    check = False
    REGEX = '(REKENING GIRO\n|REKENING TAHAPAN\n)((.|\n)*)(.*?)NO. REKENING : \d+\n(.*?)HALAMAN : (.*)\n(.*?)PERIODE : (.*)\n((.|\n)*)MATA UANG : [A-Z][A-Z][A-Z]\n((.|\n)*)CATATAN:\n((.|\n)*)TANGGAL KETERANGAN CBG MUTASI SALDO\n((.|\n)*)((\d{2}/\d{2} (.*) ((\d{1,3},)*)?\d{1,3}\.\d{2} (DB |)((\d{1,3},)*)?\d{1,3}\.\d{2}\n((.|\n)*))*)((.|\n)*)(SALDO AWAL : (.*)\nMUTASI CR : (.*)\nMUTASI DB : (.*)\nSALDO AKHIR : (.*))?'
    try:
        result, list_text = ReadNativePDF(filepath)
        check = IsNativePDF(list_text, REGEX)
    
    except:
        check = False
    img, listpath = ConvertFileToImageByChris(filepath)
    PrintLog('img: ' + str(len(img)))
    Bank = 'BCA'
    if check == False:   
        print("This is not native") 
        for R in range(len(img)):
            Message = "Currently Page " + str(R+1)
            # PrintLog(Message)
            processedimglvl1, img_data ,parameter, conf = ProcessTesseract_MaximumConfidenceLevel1(img[R], arrayThreshold, 1)
            x = 0
            text = Tesseract_Image_To_Data_Postprocess(img_data)
            Temp_Img_Data.append(img_data)
            result1 = ProcessTesseract(processedimglvl1,1)
            
            file = open("/var/html/main/txt/"+str(R+1)+' '+str(file_name)+".txt","w")
            file.write(result1) 
            file.close()
            
    #         file = open(OUTPUT_FOLDER_PATH+str(R+1)+' '+str(file_name)+".txt","w")
    #         file.write(result1) 
    #         file.close()
            
            Temp_Result.append(result1)
            result, footer = RemoveFooter(result1)
            idx,S = findindex(result1.splitlines(), 1)
            if S==False:
                idx,S = findindex(result1.splitlines(), 0)
                    
                    
            if R==0 :
                if S:
                    LL=['UNIT KERJA','DANAMON','lAPORAN REKENING','BRI','CIMB','CIF','CIF NUMBER']
                    h=result1.splitlines()[:idx]
                    a='\n'.join(h) 
                    if len(set(LL) & set(a.split()))!=0 or  ExtractValue_SpecificPattern(a,'OPENING BALANCE|ACCOUNT HUMBER|POSTING DATE|PERIODE LAPORAN|TANGGAL CETAK|ACCOUNT NUMBER|ACCOUNT TYPE|PENCETAKAN|PANIN|DIGITAL CUSTOMER INFORMATION|TRANSACTION INGUIRY|TRANSACTION INQUIRY',0,"",True,False)!='':
                        message='Data Does Not Match'
                        # PrintLog(message)
                        print(set(LL) & set(a.split()))
                        print('Result : ',ExtractValue_SpecificPattern(a,'OPENING BALANCE|ACCOUNT HUMBER|POSTING DATE|PERIODE LAPORAN|TANGGAL CETAK|STATEMENT OF ACCOUNT|ACCOUNT NUMBER|ACCOUNT TYPE|PENCETAKAN|PANIN|DIGITAL CUSTOMER INFORMATION|TRANSACTION INGUIRY|TRANSACTION INQUIRY',0,"",True,False))
                        
                        print(message)
                        error_message=Error_Handling(file_name,message)
                        sys.exit()
                    a='\n'.join(result1.splitlines()[-5:])
                    if ExtractValue_SpecificPattern(a,'OCBC NISP|1500-999|TRANSACTION INGUIRY|TRANSACTION INQUIRY',0,"",True,False)!='':
                        message='Data Does Not Match'
                        # PrintLog(message)
                        print(message)

                        error_message=Error_Handling(file_name,message)
                        sys.exit()
            Message = "Page " + str(R+1) + " index is " + str(idx)
            # PrintLog(Message) 
            # print(idx)

            if found == False:
                name,periode,norek,year,found = getName(result1,file_name)
    #         print('result = ', result)
            for i in range(idx+1+x, len(result.splitlines())):
                o=i
                if CheckDate(result.splitlines()[i],date_type):
    #                 print('year : ',year)
                    Flag = 0
                    Message = "Checking Date Successfully"
                    # PrintLog(Message)
                    a,Date=result.splitlines()[i],''
                    # if ExtractValue_SpecificPattern(a,'\d{2}/\s\d{2}',0,"",True,0)!='':
                    #    t=[(m.start(0)) for m in re.finditer( '\d{2}/\s\d{2}',a)]
                    #    if len(t)!=0 and t[0]<3:
                    #        Date=ExtractValue_SpecificPattern(a,'\d{2}/\s\d{2}',0,"",True,False) 
                    if Date=='':
                        Date=GetDate(a,date_type)# Date=ExtractValue_SpecificPattern(a,'(\d{6}|\d{2}7\d{2}|\d{2}1\d{2}|\d{3}\s\d{2}|\d{2}/\d{2})',0,"",True,False)
                        PrintLog("Date : "+ Date)
    #                     Date+=year
    #                     print('Date+year : ',Date)
                    Description=ExtractValue_SpecificPattern(a,Date+'(.*?) \d{1,11}(\.|\,|\:)',1,"",True,0)#\d{1,4}
                    # print('hi:',Date+' '+Description)
                    Temp=Date+Description
                    # print(Temp)
                    Temp=re.sub(Temp,'',a)
                    # print('resub Temp : ', Temp)
                    Temp_=re.sub('DB','',Temp)
                    Temp_=re.sub(':',',',Temp_)
                    Temp_=re.sub(ExtractValue_SpecificPattern(Temp_,'(.*?\d{1,2}.\d{1,4},\D+ )',1,"",True,0),'',Temp_)
                    k=list(Temp_)
                    for s in range(len(k)-2):
                        if (k[s]==',' and k[s+1]==' ' and k[s+2].isdigit()) or (Temp_[s].isdigit() and Temp_[s+1]==' ' and Temp_[s+2]==',') or (Temp_[s]=='.' and Temp_[s+1]==' ' and Temp_[s+2].isdigit()):
                            k[s+1]=''
            #                 if k[s].isdigit() and k[s+1]==' ' and k[s+2]=='-':
            #                     k[s+1]=' '
                    Temp_=" ".join(''.join(k).split())
                    PrintLog('Temp_ :'+Temp_)
                    PrintLog('Description : ' + Description)

                    if ExtractValue_SpecificPattern(Temp_,'(.*?)(?: \d{1,4}(\,|\.)| \d{1,11}(\,|\.)| -\d{1,4}(\,|\.))',1,"",True,0) !='':
                        Message = "Checking Mutation Successfully"
                        # PrintLog(Message)
                        Mutasi= ExtractValue_SpecificPattern(Temp_,'(.*?)(?: \d{1,4}(\,|\.)| \d{1,11}(\,|\.)| -\d{1,4}(\,|\.))',1,"",True,0)
                        print('Mutasi = ', Mutasi)
                        if '/' in Mutasi :
                            try :
                                Flag=1
                                print(Mutasi)
                                Mutasi2= ExtractValue_SpecificPattern(Temp_,Mutasi+'(.*? \d{1,4}(\,|\.)+\d{1,4}(\,|\.)\d{1,4}(\,|\.)+\d{1,2})',1,"",True,0)
                                print('ini mutasi ' ,Mutasi2)
                                Mutasi=''
                                Mutasi = Mutasi2
                                if ExtractValue_SpecificPattern(Temp_,Mutasi+'(.*? \d{1,4}(\,|\.)+\d{1,4}(\,|\.)\d{1,4}(\,|\.)+\d{1,2})',1,"",True,0) != '':
                                    Balance=re.sub(Mutasi,'',Temp_)
                                    Balance=re.sub('(\.\,)','.',re.sub(',','.',Balance))
                                    Balance=list(Balance)
                                    for i in range(len(Balance)-1,1,-1):
                                        if Balance[i]=='.':
                                            Balance=','
                                            break
                                    Balance=''.join(Balance)
                                    print('Balance = ', Balance)
                                else :
                                    Balance = '-'
                                    print('Balance = ', Balance)
                            except:
                                Flag=1
                                Mutasi=Mutasi
                        else :
                            Balance=re.sub(Mutasi,'',Temp_)
                            Balance=re.sub('(\.\,)','.',re.sub(',','.',Balance))
                            Balance=list(Balance)
                            for i in range(len(Balance)-1,1,-1):
                                if Balance[i]=='.':
                                    Balance[i]=','
                                    break
                            Balance=''.join(Balance)
                            print('Balance 2 = ', Balance)
                            # fix code : if Balance has 4 digit before . or , 
                            k=list(re.sub(' ','',Balance))
                            for s in range(len(k)-5):
                                s=0
                                if (k[s].isdigit() and k[s+1].isdigit() and k[s+2].isdigit() and k[s+3].isdigit() and k[s+4]=='.'):
                                    k[s+1]=''
                                    Balance="".join(''.join(k).split())
                                if (k[s].isdigit() and k[s+1].isdigit() and k[s+2].isdigit() and k[s+3].isdigit() and k[s+4]==','):
                                    k[s+1]=''
                                    Balance="".join(''.join(k).split())
                    else:
                        Message = "Checking Mutation Successfully"
                        # PrintLog(Message)
                        Mutasi=Temp_
                        Balance='-'
                    #                 Date_=Date

                    #                 Date_=GetDate(re.sub(' ','',Date),date_type)
                    Mutasi=re.sub('(\,\.)','.',re.sub(',','.',Mutasi))        
                    Mutasi=list(Mutasi)
                    for i in range(len(Mutasi)-1,1,-1):
                        if Mutasi[i]=='.':
                            Mutasi[i]=','
                            break
                    Mutasi=''.join(Mutasi) 
                    Mutasi='-'+Mutasi if 'DB' in Temp else Mutasi
                    Balance = re.sub("[^0-9.,\-]", "", Balance)
                    Mutasi = re.sub("[^0-9.,\-]", "", Mutasi)
                    if 'SALDO AWAL' in Description:
                        Message = "Checking SALDO AWAL Successfully"
                        # PrintLog(Message)
                        Balance = Mutasi
                        Mutasi = '-'
                    #fixing 22159925310,25
                    u = list(re.sub(' ','',Balance))
                    if Balance!='-':
                        try :
                            if Balance !='' and '.' not in u[0:5] and (u[2]=='1' and u[3]=='5'):
                                if '.' not in u[4:9] and u[7]=='5':
                                    u[3]='.'
                                    u[7]='.'
                                    Balance=''.join(u)
                                    Flag=1
                                else:
                                    u[3]='.'
                                    Balance=''.join(u)
                                    Flag=1
                        except:
                            Flag=1
                            Balance=Balance
                else:
                    Message = "Checking Description Successfully"
                    # PrintLog(Message)
                    Description = getDesc(Description,result.splitlines()[i])
                    Test_CPTY = ExtractValue_SpecificPattern(result.splitlines()[i], "(.*?)$", 0, "", True, False)
                if Date != '':
                    Date2=GetDate_WF(Date,date_type)
                    # Date2=Date2+'/'+year
                    # PrintLog("Date2 : "+ Date2)
                    try:
                        sc=int(Mutasi)
                    except:
                        sc=''
                    if Mutasi=='' or Balance=='' or (sc!='' and len(str(sc))<3):
                        Flag=1
                    
    #             print('Date : ', Date2)
    #             print('Description : ', Description)
    #             print('Mutasi : ', Mutasi)
    #             print('Balance : ', Balance)
                if  o==len(result.splitlines())-1:
                    try:
                        BankCPTY, CPTY = getCPTY(Description, Bank, Test_CPTY)
                        Test_CPTY=''
                        Result2.append([["Date","Description", "CPTY", "Bank CPTY", "Mutation","Balance","Flag"],[Date2,Description,CPTY, BankCPTY,str(Mutasi),str(Balance),Flag]])
                        Result3.append([["Date","Description", "CPTY", "Bank CPTY", "Mutation","Balance","Flag"],[Date2,Description,CPTY, BankCPTY,str(Mutasi),str(Balance),Flag]])
                        Temp_Mutasi.append(Mutasi)
                        Temp_Balance.append(Balance)
                        Temp_Date.append(Date2)
                    except:
                        print("Error on Date")
                        continue
                if  o!=len(result.splitlines())-1 and CheckDate(result.splitlines()[o+1],date_type):
                    try:
                        BankCPTY, CPTY = getCPTY(Description, Bank, Test_CPTY)
                        Test_CPTY=''
                        Result2.append([["Date","Description", "CPTY", "Bank CPTY", "Mutation","Balance","Flag"],[Date2,Description,CPTY, BankCPTY,str(Mutasi),str(Balance),Flag]])
                        Result3.append([["Date","Description", "CPTY", "Bank CPTY", "Mutation","Balance","Flag"],[Date2,Description,CPTY, BankCPTY,str(Mutasi),str(Balance),Flag]])
                        Temp_Mutasi.append(Mutasi)
                        Temp_Balance.append(Balance)
                        Temp_Date.append(Date2)
                    except:
                        print("Error on Date")
                        continue
                
                for i in range(len(Result2)):
                    pairs = zip(Result2[i][0], Result2[i][1])
                    json_values = ('"{}": "{}"'.format(x,y) for x,y in pairs)
                    my_string = '{' + ', '.join(json_values) + '}'
                    TED.append(json.loads(my_string))
                Total_Result += Result2
                Result2=[]

        Result4=[]
        FLAG=[]
        n=0
        DATE1,MONTH1,YEAR1=[],[],[]
        Result2=Total_Result
        PrintLog('semua tanggal : '+ Result2[0][1][0])
        for s in range(len(Result2)):
            # if year != '' :
            # 	Result2[s][1][0]=Result2[s][1][0]+'/'+year
            # else :
            # 	year_defaults='2020'
            # 	Result2[s][1][0] = Result2[s][1][0]+'/'+year_defaults
            _,f=checkFormat(Result2[s][1][0])
            if f==0:
                n=s
                break
        DATE,MONTH,YEAR=[],[],[]
        for c in range(len(Result2)):
            # ##
            # if year != '' :
            #     Result2[c][1][0]=Result2[c][1][0]+'/'+year
            # else :
            #     year_defaults='2020'
            #     Result2[c][1][0] = Result2[c][1][0]+'/'+year_defaults
            #     Result2[c][1][6] = 1
            # ##
            Result2[c][1][0],Result2[c][1][6]=checkFormat(Result2[c][1][0])
            if Result2[c][1][6]==1 and c>n:
                Result2[c][1][0]=Result2[c-1][1][0]
            DATE.append(int(Result2[c][1][0][:2]))
            DATE1.append([Result3[c][1][0],int(Result2[c][1][0][:2])])
            MONTH.append(Result2[c][1][0][3:])
            MONTH1.append([Result3[c][1][0],Result2[c][1][0][3:]])
            FLAG.append(Result2[c][1][6])
            PrintLog('semua tanggal : ' + Result2[c][1][0])
        for s in range(n):
            MONTH[s]=Result2[n][1][0][3:] 
            DATE[s]=int(Result2[n][1][0][:2] )
            FLAG[s]=1
        # if len(set(MONTH))!=1:
        #     t,Z=0,True
        #     while Z:
        #         # print('month 1 : ',MONTH[t])
        #         # print('month 1 : ',MONTH[t+1])
        #         if t==0 and datetime.datetime.strptime(MONTH[t],'%m-%Y')>datetime.datetime.strptime(MONTH[t+1],'%m-%Y'):
        #             MONTH[t]=MONTH[t+1]
        #             FLAG[t]=1
        #         elif t>0 and datetime.datetime.strptime(MONTH[t],'%m-%Y')>datetime.datetime.strptime(MONTH[t+1],'%m-%Y')  :
        #             MONTH[t]=MONTH[t-1] 
        #             FLAG[t]=1
        #         elif t>0 and datetime.datetime.strptime(MONTH[t],'%m-%Y')>datetime.datetime.strptime(MONTH[t+1],'%m-%Y') and FLAG[t-1]==1 and FLAG[t+1]==1:
        #             MONTH[t]=MONTH[t-1]
        #             FLAG[t]=1
        #         elif t>0 and datetime.datetime.strptime(MONTH[t],'%m-%Y')>datetime.datetime.strptime(MONTH[t+1],'%m-%Y') and FLAG[t-1]==0 and FLAG[t+1]==0:
        #             MONTH[t]=MONTH[t-1]
        #             FLAG[t]=1
        #         elif t>0 and datetime.datetime.strptime(MONTH[t],'%m-%Y')<datetime.datetime.strptime(MONTH[t+1],'%m-%Y') and MONTH[t+1]==MONTH[t-1]:
        #             MONTH[t]=MONTH[t-1]
        #             FLAG[t]=1
        #         s,e=t,len(MONTH) - MONTH[::-1].index(MONTH[t]) - 1
        #         # s,e=t,len(MONTH) - MONTH[::-1].index(MONTH[t]) - 1
        #         if e-s>20:
        #             t+=1
        #             continue
        #         for R in range(s,e+1):
        #             if MONTH[R]!=MONTH[t]:
        #                 MONTH[R]=MONTH[t]
        #                 FLAG[R]=1
        #         t=e+1
        #         if t==len(MONTH)-1 or t==len(MONTH):
        #             Z=False

        #17 Jan 2022
        if len(set(MONTH))!=1:
            t,Z=0,True
            while Z:
                # print('month 1 : ',MONTH[t])
                # print('month 1 : ',MONTH[t+1])
                if t==0 and datetime.datetime.strptime(MONTH[t],'%m')>datetime.datetime.strptime(MONTH[t+1],'%m'):
                    MONTH[t]=MONTH[t+1]
                    FLAG[t]=1
                elif t>0 and datetime.datetime.strptime(MONTH[t],'%m')>datetime.datetime.strptime(MONTH[t+1],'%m')  :
                    MONTH[t]=MONTH[t-1] 
                    FLAG[t]=1
                elif t>0 and datetime.datetime.strptime(MONTH[t],'%m')>datetime.datetime.strptime(MONTH[t+1],'%m') and FLAG[t-1]==1 and FLAG[t+1]==1:
                    MONTH[t]=MONTH[t-1]
                    FLAG[t]=1
                elif t>0 and datetime.datetime.strptime(MONTH[t],'%m')>datetime.datetime.strptime(MONTH[t+1],'%m') and FLAG[t-1]==0 and FLAG[t+1]==0:
                    MONTH[t]=MONTH[t-1]
                    FLAG[t]=1
                elif t>0 and datetime.datetime.strptime(MONTH[t],'%m')<datetime.datetime.strptime(MONTH[t+1],'%m') and MONTH[t+1]==MONTH[t-1]:
                    MONTH[t]=MONTH[t-1]
                    FLAG[t]=1
                s,e=t,len(MONTH) - MONTH[::-1].index(MONTH[t]) - 1
                # s,e=t,len(MONTH) - MONTH[::-1].index(MONTH[t]) - 1
                if e-s>20:
                    t+=1
                    continue
                for R in range(s,e+1):
                    if MONTH[R]!=MONTH[t]:
                        MONTH[R]=MONTH[t]
                        FLAG[R]=1
                t=e+1
                if t==len(MONTH)-1 or t==len(MONTH):
                    Z=False
        
        j=[]
        for n in range(len(MONTH)):
            j.append(MONTH[n])          
        kk=[]
        for s in MONTH:
            if s not in kk:
                kk.append(s)
        MY,Date_,FLAG_,MY2,Date_2,FLAG_2=[],[],[],[],[],[]

        for k in range(len(kk)):
            s,e=MONTH.index(kk[k]),len(MONTH) - MONTH[::-1].index(kk[k]) 
            MY.append(MONTH[s:e])
            MY2.append(MONTH[s:e])
            Date_.append(DATE[s:e])
            Date_2.append(DATE[s:e])
            FLAG_.append(FLAG[s:e])
            FLAG_2.append(FLAG[s:e])
        for u in range(len(Date_)):
            MONTH=Date_[u]
            FLAG=FLAG_[u]
            t,Z=0,True
            while Z and len(MONTH)!=1:
                if t==0 and MONTH[t]>MONTH[t+1]:
                    MONTH[t]=MONTH[t+1]
                    FLAG[t]=1
                elif t>0 and MONTH[t]>MONTH[t+1] :
                    MONTH[t]=MONTH[t-1] 
                    FLAG[t]=1
                elif t>0 and  MONTH[t]>MONTH[t+1] and FLAG[t-1]==1 and FLAG[t+1]==1:
                    MONTH[t]=MONTH[t-1]
                    FLAG[t]=1
                elif t>0 and MONTH[t]>MONTH[t+1] and FLAG[t-1]==0 and FLAG[t+1]==0:
                    MONTH[t]=MONTH[t-1]
                    FLAG[t]=1
                elif t>0 and MONTH[t]<MONTH[t+1] and (MONTH[t+1]==MONTH[t-1] or (MONTH[t]<MONTH[t+1] and MONTH[t]<MONTH[t-1])):
                    MONTH[t]=MONTH[t-1]
                    FLAG[t]=1
                elif t>0 and MONTH[t]<MONTH[t-1]:
                    MONTH[t]=MONTH[t-1]
                    FLAG[t]=1
                s,e=t,len(MONTH) - MONTH[::-1].index(MONTH[t])- 1
                if e-s>20:
                    t+=1
                    continue
                for R in range(s,e+1):
                    if MONTH[R]!=MONTH[t]:
                        MONTH[R]=MONTH[t]
                        FLAG[R]=1
                t=e+1
                if t==len(DATE)-1: #added
                    if int(DATE[t])<int(DATE[t-1]):
                        DATE[t]=DATE[t-1]
                        FLAG[t]=1
                        
                if t==len(MONTH)-1 or   t==len(MONTH):
                    Z=False
            Date_[u]=MONTH
            FLAG_[u]=FLAG    
        nd=[]
        nf=[]
        nd = [j for i in Date_ for j in i]
        nf = [j for i in FLAG_ for j in i]
        
        # for f in range(len(Result2)):
        #     #penambahan try except
        #     try:
        #         Result2[f][1][0]= datetime.datetime.strptime(str(nd[f])+'-'+j[f], "%d-%m-%Y").strftime("%d-%m-%Y")
        #         Result2[f][1][6]=nf[f]
        #     except:
        #         try:
        #             if '/' in Result2[f][1][0]:
        #                 Result2[f][1][0]=re.sub('/','',Result2[f][1][0])
        #                 Result2[f][1][0]= datetime.datetime.strptime(str(nd[f])+'-'+j[f], "%d-%m").strftime("%d-%m")
        #                 Result2[f][1][6]=nf[f]
        #         except:
        #             message='Machine cannot read the date'
        #             # PrintLog(message)
        #             print(message)
        #             error_message=Error_Handling(file_name,message)
        #             sys.exit()

        #17 Jan 2022
        for f in range(len(Result2)):
            #penambahan try except
            try:
                Result2[f][1][0]= datetime.datetime.strptime(str(nd[f])+'-'+j[f], "%d-%m").strftime("%d-%m")
                Result2[f][1][6]=nf[f]
            except:
                try:
                    if '/' in Result2[f][1][0]:
                        Result2[f][1][0]=re.sub('/','',Result2[f][1][0])
                        Result2[f][1][0]= datetime.datetime.strptime(str(nd[f])+'-'+j[f], "%d-%m").strftime("%d-%m")
                        Result2[f][1][6]=nf[f]
                except:
                    message='Machine cannot read the date'
                    # PrintLog(message)
                    print(message)
                    error_message=Error_Handling(file_name,message)
                    sys.exit()



        
        for g in range(len(Result3)):
            if Result3[g][1][6]==1 and Result2[f][1][6]==0:
                Result2[g][1][6]=1
        for g in range(len(Result2)):
            if Result2[g][1][5]!='' or Result2[g][1][5]!='-' :
                Bal=Result2[g][1][5]
                PrintLog(Bal)
                k = list(Bal)
                for s in range(len(k)-2):
                    try :
                        if (k[s].isdigit() and k[s+1].isdigit() and k[s+2].isdigit() and k[s+3].isdigit() and k[s+4]=='.'):
                            k[1]=''
                            Result2[g][1][6]=1
                            Result2[g][1][5]=" ".join(''.join(k).split())
                        elif (k[s].isdigit() and k[s+1].isdigit() and k[s+2].isdigit() and k[s+3].isdigit() and k[s+4].isdigit() and k[s+5]=='.'):
                            k[s+1]=''
                            k[s+3]=''
                            Result2[g][1][6]=1
                            Result2[g][1][5]=" ".join(''.join(k).split())
                        elif (k[s].isdigit() and k[s+1]=='.' and k[s+2]=='.' and k[s+3].isdigit()):
                            k[s+1]=''
                            Result2[g][1][6]=1
                            Result2[g][1][5]=" ".join(''.join(k).split())
                        elif (k[s].isdigit() and k[s+1]=='.' and k[s+2]==',' and k[s+3]=='.' and k[s+4].isdigit()):
                            k[s+1]='.'
                            k[s+2]=''
                            k[s+3]=''
                            Result2[g][1][6]=1
                            Result2[g][1][5]=" ".join(''.join(k).split())
                        elif (k[s].isdigit() and k[s+1].isdigit() and k[s+2].isdigit() and k[s+3].isdigit() and k[s+4]=='.'):
                            k[s+1]=''
                            Result2[g][1][6]=1
                            Result2[g][1][5]=" ".join(''.join(k).split())
                        # PrintLog(Result2[g][1][5])
                    except:
                        Result2[g][1][5]=Result2[g][1][5]
            if Result2[g][1][4]!='' or Result2[g][1][4]!='-' :
                Bal=Result2[g][1][4]
                k = list(Bal)
                for s in range(len(k)-2):
                    try :
                        if (k[s].isdigit() and k[s+1]=='.' and k[s+2]=='.' and k[s+3].isdigit()):
                            k[s+1]=''
                            Result2[g][1][6]=1
                            Result2[g][1][4]=" ".join(''.join(k).split())
                        elif (k[s].isdigit() and k[s+1]=='.' and k[s+2]==',' and k[s+3]=='.' and k[s+4].isdigit()):
                            k[s+2]=''
                            k[s+3]=''
                            Result2[g][1][6]=1
                            Result2[g][1][4]=" ".join(''.join(k).split())
                        elif (k[s].isdigit() and k[s+1]=='.' and k[s+2]=='.' and k[s+3]=='.' and k[s+4].isdigit()):
                            k[s+2]=''
                            k[s+3]=''
                            Result2[g][1][6]=1
                            Result2[g][1][4]=" ".join(''.join(k).split())
                        elif (k[s].isdigit() and k[s+1].isdigit() and k[s+2].isdigit() and k[s+3].isdigit() and k[s+4]=='.'):
                            k[s+1]='.'
                            Result2[g][1][6]=1
                            Result2[g][1][4]=" ".join(''.join(k).split())
                        elif (k[0].isdigit() and k[1].isdigit() and k[2].isdigit() and k[3].isdigit() and k[4].isdigit()and k[4]==','):
                            Result2[g][1][6]=1
                    except:
                        Result2[g][1][4]=Result2[g][1][4]
            # if Result2[-1][1][1]!='' or Result2[-1][1][1]!='-':
            # 	if 'KCP' in Result2[-1][1][1] or 'KCU' in Result2[-1][1][1]:
            # 		Result2[-1][1][6]=1

                
        try:
            recon_file_name = OUTPUT_RECON_FOLDER_PATH + file_name[:-4] + '.json'
            f = open(recon_file_name, "r")
            data_recon = json.load(f)
            if found_opbalance == False:
                OB,found_opbalance = getInBalance(data_recon)
        except:
            try:
                thousands_separator = "."
                decimal_separator =","
                RB=Result2[0][1][5]
                RB=re.sub('[,\.]','',RB)
                RM=Result2[0][1][4]
                RM=re.sub('[,\.]','',RM)
                RB=int(RB)/100
                RM=int(RM)/100
                OB=round(RB-RM,2)
                OB="{0:,.2f}".format(float(OB))
                if thousands_separator==".":
                    main_curr, decimal_curr = OB.split(".")[0], OB.split(".")[1]
                    new_main_curr = main_curr.replace(",",".")
                    OB = new_main_curr + decimal_separator + decimal_curr
            except:
                print('Error on Calculation')
        #added
        Temp_Date=[]
        for p in range(len(Result2)):
            Temp_Date.append(Result2[p][1][0])
            
        if first_page == 0:
            first_day = 1
            try:
                first_day = int(Result2[0][1][0][:2])
            except:
                first_page+=1
            if first_day != 1:
                try:
                    Total_Result_2 = Fillempty_first('1' + Result2[0][1][0][2:],Result2[0][1][0], Result2, OB)
                except:
                    print("Filling Early Fail") 
        Total_Result2 = FillingEmpty(Total_Result_2+Result2)
        try:
            Message = "Check Point Data Recon"
            # PrintLog(Message)
            recon_file_name = OUTPUT_RECON_FOLDER_PATH + file_name[:-4] + '.json'
            f = open(recon_file_name, "r")
            data_recon = json.load(f)
            if len(data_recon) > 0:
                BalanceChecking, Total_Result2 = ReconCalculation(Total_Result2, data_recon)
                Message = "Check Point ReconCalculationn"
                # PrintLog(Message)
            
            else:
                BalanceChecking = CalculateBalance(Temp_Mutasi, Temp_Balance, Temp_Date)
                Message = "Check Point CalculateBalance"
                # PrintLog(Message)
        except:
            BalanceChecking = CalculateBalance(Temp_Mutasi, Temp_Balance, Temp_Date)
            Message = "Check Point CalculateBalance exception"
            PrintLog(Message)
        for u in range(len(Total_Result2)):
            if Total_Result2[-1][1][1]!='' or Total_Result2[-1][1][1]!='-':
                if 'KCP' in Total_Result2[-1][1][1] or 'KCU' in Total_Result2[-1][1][1]:
                    Total_Result2 = np.delete(Total_Result2, -1, axis=0)

        #17 Jan 2022
        for yr in range(len(Total_Result2)):
            if year != '' :
                Total_Result2[yr][1][0]=Total_Result2[yr][1][0]+'-'+year
            else:
                year_default = '2020'
                Total_Result2[yr][1][0]=Total_Result2[yr][1][0]+'-'+year_default
                Total_Result2[yr][1][6] = 1
        
        Rev_TED = []
        for i in range(len(Total_Result2)):
            pairs = zip(Total_Result2[i][0], Total_Result2[i][1])
            json_values = ('"{}": "{}"'.format(x,y) for x,y in pairs)
            my_string = '{' + ', '.join(json_values) + '}'
            Rev_TED.append(json.loads(my_string))

        user_defined_list = ["PERIODE","NAME", "BANK", "MATA UANG","EXCHANGE", "NO. REKENING"]
        extractedResult = ExtractValue_PredefinedForeList(Temp_Result[0], user_defined_list)
        extractedResult = cleanExtracted(extractedResult)
        if periode == '':
            periode = '*****'
        extractedResult[0], extractedResult[1], extractedResult[2], extractedResult[5]=periode, name, "BCA", norek
        extractedResult[3] = re.sub(" ", "",re.sub("\d+", "", extractedResult[3]))
        ConfLv = round(CalculateConfidenceLevel(Temp_Img_Data),2)
        Conf = str(ConfLv) + ' %'
        user_defined_list = ["PERIODE","NAME", "BANK", "CURRENCY","EXCHANGE","ACCOUNT NO"]
        my_array = [user_defined_list, extractedResult]  
        pairs = zip(my_array[0], my_array[1])
        json_values = ('"{}": "{}"'.format(label, value) for label, value in pairs)
        field_string = '{' + ', '.join(json_values) + '}'
        field_turn = json.loads(field_string)
    
    elif check == True:
        print("This is native") 
        PrintLog("This is native") 
        new_line = ''
        sub = '\n'
        TED = []
        Total_Result = []
        List_Path = ""
        # print(len(list_text))
        header_found = False
        name, periode, currency, norek, exchange = '','','','','#####'
        #17 Jan 2022
        year = ''
        for i in range(len(list_text)):
            Result2 = []
            result1 = []
            saldo_awal = ''
            print(len(list_text[i]))
            for j in range(len(list_text[i])):
                if (list_text[i][j] == '\n' and new_line != '' ):
                    new_line = new_line.replace('\n','')
                    if new_line == '':
                        continue
                    result1.append(new_line)
                    new_line = ''
                elif j == len(list_text[i])-1:
                    new_line += list_text[i][j]
                    result1.append(new_line)
                new_line += list_text[i][j]
            cek_trx = False
            # print(len(result1))
            # print(result1)
            
            for n in range(len(result1)):
                line = result1[n]
                if ExtractValue_SpecificPattern(line, "Bersambung ke Halaman berikut|SALDO AWAL :", 0, "", True, False) != "":
                    cek_trx = False
                if cek_trx:
                    if CheckDateN(line) == True:
                        if ExtractValue_SpecificPattern(line, "SALDO AWAL", 0, "", True, False):
                            saldo_awal = ExtractValue_SpecificPattern(line, "[\d{1,3},]*\.\d{2}$", 0,'', True, False)
                            continue
                        date, desc, mutasi, saldo = '', '', '', ''
                        date, desc, mutasi, saldo = getValueN(line)
                        date = re.sub('\s','',date) #19 Jan 2022
                    else:
                        desc = getDescN(desc, line)
                        if ExtractValue_SpecificPattern(result1[n-1], "TANGGAL KETERANGAN CBG MUTASI SALDO", 0, "", True, False) != "":
                            Total_Result[-1][1][1] = desc
                            continue
                    PrintLog("Date: " + date)
                    PrintLog("Desc: " + desc)
                    PrintLog("Mutasi: " + mutasi)
                    PrintLog("Saldo: " + saldo)
                    CPTY, BankCPTY = getCPTYN(desc, "BCA", name)
                    if n!=len(result1)-1 and CheckDateN(result1[n+1]):
                        Result2.append([["Date","Description", "CPTY", "Bank CPTY", "Mutation","Balance","Flag"],[datetime.datetime.strptime(date,'%d/%m').strftime('%d-%m'),desc,CPTY, BankCPTY,mutasi,saldo,0]])
                    
                    if n==len(result1)-2 or ExtractValue_SpecificPattern(result1[n+1], "Bersambung ke Halaman berikut|SALDO AWAL :", 0, "", True, False) != "":
                            try:
                                Result2.append([["Date","Description", "CPTY", "Bank CPTY", "Mutation","Balance","Flag"],[datetime.datetime.strptime(date,'%d/%m').strftime('%d-%m'),desc,CPTY, BankCPTY,mutasi,saldo,0]])
                            except:
                                print("Error occurred onTime Data at line : "+str(o))
                if ExtractValue_SpecificPattern(line, "TANGGAL KETERANGAN CBG MUTASI SALDO", 0, "", True, False) != "":
                    cek_trx = True
                if header_found != True:
                    if ExtractValue_SpecificPattern(line, "NO. REKENING", 0, "", True, False):
                        name = ExtractValue_SpecificPattern(line, "(.*?) NO. REKENING",1, "", True, False)
                        norek = ExtractValue_SpecificPattern(line, "\d{1,14}",0, "", True, False)
                    if ExtractValue_SpecificPattern(line, "PERIODE",0, "", True, False):
                        periode = ExtractValue_SpecificPattern(line, "PERIODE : (.*?)$",1, "", True, False)
                        year = ExtractValue_SpecificPattern(periode, "\d{4}$",0, "", True, False)
                    if ExtractValue_SpecificPattern(line, "MATA UANG",0, "", True, False):
                        currency = ExtractValue_SpecificPattern(line, "MATA UANG : (.*?)$",1, "", True, False)
                        header_found= True

                PrintLog('periode: ' + periode)
                PrintLog('year: ' + year)
            Total_Result += Result2
        # for i in range(len(Total_Result)):
        #     print(Total_Result[i][1])
        Total_Result_2 = []
        if int(Total_Result[0][1][0][0:2]) != 1 :
            print(Total_Result[i][1][0])
            Total_Result_2 = Fillempty_firstN('01' + Total_Result[0][1][0][2:],Total_Result[0][1][0], Total_Result, Total_Result[0][1][5])
        Total_Result2 = FillingEmptyN(Total_Result_2+Total_Result)

        #17 Jan 2020
        for yr in range(len(Total_Result2)):
            if year != '' :
                Total_Result2[yr][1][0]=Total_Result2[yr][1][0]+'-'+year
            else:
                year_default = '2020'
                Total_Result2[yr][1][0]=Total_Result2[yr][1][0]+'-'+year_default
                try:
                    Total_Result2[yr][1][6] = 1
                except:
                    PrintLog("Flagging Failed")

        Rev_TED = []
        for i in range(len(Total_Result2)):
            pairs = zip(Total_Result2[i][0], Total_Result2[i][1])
            json_values = ('"{}": "{}"'.format(x,y) for x,y in pairs)
            my_string = '{' + ', '.join(json_values) + '}'
            Rev_TED.append(json.loads(my_string))
        user_defined_list = ["PERIODE","NAME", "BANK", "MATA UANG","EXCHANGE", "NO. REKENING"]
        extractedResult = [periode, name, "BCA", currency,exchange,norek]
        Conf = str(100) + ' %'
        user_defined_list = ["PERIODE","NAME", "BANK", "CURRENCY","EXCHANGE","ACCOUNT NO"]
        my_array = [user_defined_list, extractedResult]  
        pairs = zip(my_array[0], my_array[1])
        json_values = ('"{}": "{}"'.format(label, value) for label, value in pairs)
        field_string = '{' + ', '.join(json_values) + '}'
        field_turn = json.loads(field_string)
        Check_Balance = "BALANCE"
    
    Top_Head = ["CONF_LV", "CALCULATION", "IMG_RAW", "FIELD_LIST","TRANSACTION_LIST"]
    Top_Head_Value = [Conf, Check_Balance, listpath, field_turn, Rev_TED]
    # Top_Head_Value[3], Top_Head_Value[4]  = field_turn, TED
    
    mystring = {} 
    mystring[Top_Head[0]] = Top_Head_Value[0]
    mystring[Top_Head[1]] = Top_Head_Value[1]
    mystring[Top_Head[2]] = Top_Head_Value[2]
    mystring[Top_Head[3]] = Top_Head_Value[3]
    mystring[Top_Head[4]] = Top_Head_Value[4]
    
    json_formatted_str = json.dumps(mystring, indent=2)
    
    # StoreCSV(TED,extractedResult,user_defined_list,file_name)
    
    
    
    print(json_formatted_str)
    print("--- %s seconds ---" % (time.time() - start_time))
    with open(OUTPUT_JSN_FOLDER_PATH+file_name[:-4]+'.txt', "w") as d:  
        json.dump(mystring, d,indent=3)
    
    Post_Success(OUTPUT_JSN_FOLDER_PATH, file_name, Conf, Check_Balance)
    
    return (json_formatted_str)

PROCESS_ID_BCA_TYPE_1()
