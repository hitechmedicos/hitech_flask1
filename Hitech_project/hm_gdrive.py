
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from sys import path
import os
import time
import shutil
import configparser
from test.test_dbm import _fname

gauth = GoogleAuth()
# Try to load saved client credentials
gauth.LoadCredentialsFile("C:\\GDownload\\mycreds.txt")
if gauth.credentials is None:
    # Authenticate if they're not there
    gauth.LocalWebserverAuth()
elif gauth.access_token_expired:
    # Refresh them if expired
    gauth.Refresh()
else:
    # Initialize the saved creds
    gauth.Authorize()
# Save the current credentials to a file
gauth.SaveCredentialsFile("C:\\GDownload\\mycreds.txt")

drive = GoogleDrive(gauth)
def file_move(src,fsname,dest,fdname):
    shutil.move(os.path.join(src,fsname),os.path.join( dest,fdname))


def getCreatedDateOfFile(file):
    fileCreatedDate = file['createdDate']
    fileCreatedDate, head, tail = fileCreatedDate.partition(".")
    fileCreatedDate = fileCreatedDate.replace(":", "").replace("-", "").replace("T","")
    return fileCreatedDate


# Downloading data from gdrive
#sample_format
#mtype : 'application/rar'(mimeType)
#pid : 0BxgDvyagf53aUFR0b3hKbmphdHM (parent folder id)
def file_download(mtype,pid,dsrc):
#     pid ='0B86tEvECvMdySEllTDRMQzNKNHM'
    file_list = drive.ListFile({'q':"'%s' in parents and mimeType = 'application/zip' and trashed=false" % pid}).GetList()

#     dsname="C:\\GDownload\\"
#     dsfname="webcraq.zip"
    for file1 in file_list:
        if int(getCreatedDateOfFile(file1)) > int(lastUploadedTime):
            pass
            print(getCreatedDateOfFile(file1))
            print(int(lastUploadedTime))
            print('title: %s, id: %s' % (file1['title'], file1['id']))
            file6 = drive.CreateFile({'id' : file1['id']})
            file6.GetContentFile(dsrc+file1['title'])
            print (file6)
            print (type(file_list))
            print(file_list)
            file_move(srce,file1['title'], deste,file1['title'])
        else:
            print('OLD File: '+file1['title'])



def main():
    global lastUploadedTime 
    global srce,deste
    lastUploadedTime = open("C:\\GDownload\\lastUploadedTime.txt", "r").read()
    
    conf =configparser.ConfigParser()
    conf.read("C:\\GDownload\\config.ini")
    for each_section in conf.sections():      
        pid1 =conf[each_section]['pid']
        mtype1 =conf[each_section]['mtype']
        srce=conf[each_section]['src']
        deste=conf[each_section]['dest']
        # fsname1=conf[each_section]['srcfile']
        # fdname1=conf[each_section]['destfile']
        # print  ( "pid with : "+pid1+" with mtype :" + mtype1+" src&dest : "+srce+deste+"fsname1&fdname1: " +fsname1+fdname1)
        file_download(mtype1, pid1,srce)
        # file_move(srce,fsname1, deste,fdname1)
    lastUploadedTime = open("C:\\GDownload\\lastUploadedTime.txt", "w").write(time.strftime("%Y%m%d%H%M%S", time.gmtime()))
    print("\n================ DONE ================\n")
   
if __name__ == "__main__":
    
    main()

