'''
Created on 12-Aug-2017

@author: kiran
'''
import csv
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import *
import requests
import urllib3 
import urlopen  # for Python 3: from urllib.request import urlopen
from bs4 import BeautifulSoup
import configparser
# from mergecsv import *

global from_date,to_date

def selxpath(wid1,uname1,pwd1,from_date,to_date): 
    driver = webdriver.Chrome()
    driver.get("http://www.cghs.nic.in")
    loginform = driver.find_element_by_xpath("//form[@name='f1']")
    driver.find_element_by_xpath("//form[@name='f1']//input[@name='dispensary_code']").send_keys(wid1)
    driver.find_element_by_xpath("//form[@name='f1']//input[@name='uid']").send_keys(uname1)
    driver.find_element_by_xpath("//form[@name='f1']//input[@name='pwd']").send_keys(pwd1)
    driver.find_element_by_xpath("//form[@name='f1']//input[@type='submit']").click()
    def alert_accept():
        try:
            alert = driver.switch_to_alert()
#             print "Aler text:" + alert.text
            alert.accept()
            print ("Alert detected, accept it")
            return True
        except UnexpectedAlertPresentException:
            print ("Hum..., continue?")
            return False
        except NoAlertPresentException:
            print ("No alert here")
            return False
    while alert_accept() == True:
        alert_accept()    
    driver.switch_to_frame("left_frame")
    driver.find_element_by_xpath("//*[@id='sa12']").click()
    driver.switch_to_default_content()
    driver.switch_to_frame("right_frame")
    def selectDate(date, var):
        try:
            driver.find_element_by_xpath(var).click()
            dateList = date.split("/")
            print(dateList)
            day = dateList[0]
            month = int(dateList[1])
            year = dateList[2]
            
            driver.find_element_by_xpath("//*[@id='spanYear']").click()
            yearXpath = "//*[contains(text(), '"+year+"')]"
            driver.find_element_by_xpath(yearXpath).click()
            monthsAr = ['January', 'February','March','April','May','June','July','August','September','October','November','December']
            
            driver.find_element_by_xpath("//*[@id='spanMonth']").click()
#             monthXpath = " //*[contains(text(), '"+month-1]+"')] "
            mnt=str(month-1)
            monthXpath ="//*[@id='m"+mnt+"']"
            driver.find_element_by_xpath(monthXpath).click()
            dateXpath = "//*[@href = 'javascript:dateSelected="+day+";closeCalendar();']"
            
            driver.find_element_by_xpath(dateXpath).click()
            time.sleep(2)
        except:
            print("Could not select date")
            pass
#     date='14/8/2017'
    date=from_date
    selectDate(date, "//*[@id='AutoNumber1']/tbody/tr[2]/td[2]/img")
#     date='14/8/2017'
    date=to_date
    selectDate(date, "//*[@id='AutoNumber1']/tbody/tr[3]/td[2]/img")
    driver.find_element_by_xpath("//*[@id='AutoNumber1']/tbody/tr[4]/td[1]/b/input").click()
    driver.switch_to_default_content()
    driver.switch_to_frame("right_frame")
    trno=driver.find_elements_by_xpath("/html/body/div[4]/center/div/table/tbody/tr")
    
    trno=len(trno)
    filegen(wid)
    for i in range(2, trno):
        i = str(i)
        row = driver.find_element_by_xpath("/html/body/div[4]/center/div/table/tbody/tr[" + i + "]")
        line1=[]
        for j in range(2, 4):
            j = str(j)
            try:
                line = (driver.find_element_by_xpath("/html/body/div[4]/center/div/table/tbody/tr[" + i + "]/td[" + j + "]").text)
            except:
                pass
            print(line)
        
            line1.append(line)
        print(line1)
        line1.append(wid)
        wr.writerow(line1)
    
def filegen(fname1):
    f = open(path+fname1+'.csv', 'w', newline='') 
    global wr
    wr = csv.writer(f, dialect='excel')


def main(from_date,to_date):
    global driver,line1,line,wid,path
    
    path ='C:\\CGHSFilesdownload\\TEMP\\' # use your path
    line =[]
    line1=[]
    conf =configparser.ConfigParser()
    conf.read("C:\\CGHSFilesdownload\\config.ini")
#     for fname_sec in conf.sections():
#         fname=conf[fname_sec]['wid']
#             
    for each_section in conf.sections():      
        wid =conf[each_section]['wid']
        uname =conf[each_section]['uname']
        pwd =conf[each_section]['pwd']
        
        selxpath(wid,uname,pwd,from_date,to_date)
        
#     mergerfile()    
# if __name__ == "__main__":
    
#     main()
