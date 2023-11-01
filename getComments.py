# -*- coding: utf-8 -*-
"""
Created on Sun Oct 29 11:59:42 2023

@author: Krishna

Useful URLs:
    
https://www.selenium.dev/documentation/webdriver/elements/locators/
https://pypi.org/project/selenium/
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
#from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.relative_locator import locate_with
#from selenium.webdriver.support import expected_conditions as EC
#from selenium.webdriver.support.ui import WebDriverWait
#from selenium.common.exceptions import TimeoutException
#import time
import re
import csv
#import os


def getTextFromAnchor(content): #To separate anchor content
    cleanAnchor = map(''.join, re.findall(r'<a\s[^>]*>([^<]*)</a>|\b(\w+://[^<>\'"\t\r\n\xc2\xa0]*[^<>\'"\t\r\n\xc2\xa0 .,()])', content))
    return list(cleanAnchor)


def cleanHashTags(content): #Replaces all anchors with mentioned IDs
    #cleanAnchor will have the mentioned ID text 
    cleanAnchor = getTextFromAnchor(content)
    for i in cleanAnchor:
        leftOut = content.split(i)              #Splits using each of the ids
        woAnchor = leftOut[0].split('<a ')[0]   #Leaves the anchor tag and takes it's left part
        content = woAnchor+i+leftOut[1][4:]     #Combines the left + mentioned_id + right
    return content
    

def setClasses():
    cmntClass = input("\nEnter the comment class :")
    #_aacl, #Span covering Comments. #The classes will change, so correct it. Previously _aade
    idClass = input("\nEnter the ID class :")
    #If not logged in, use h3 class, Previously _a9zc
    if(cmntClass=='' and idClass==''):
        cmntClass, idClass = '_aacl','_a9zc'
    return cmntClass, idClass


def writeCSV(instaData):
    #Setting file for wriiting down InstaComments
    fields = ['Label','Comments','ID']

    # Write the data to the CSV file
    with open('instaComments.csv', 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        #writer.writerow(fields)
        for row in instaData:
            writer.writerow(row)
            

def getComments(instURL):
    driver = webdriver.Chrome()
    driver.get(instURL)
    driver.implicitly_wait(30)
    #-----------------------------------------------Setting classes-----------------------------------------------
    cmntClass, idClass = setClasses()
    #---------------------------------------------------Get Data--------------------------------------------------
    elements = driver.find_elements(By.CLASS_NAME,cmntClass)
    instaData = []
    for e in elements[2:-1]:#Trim down the post content and leave the comments. If you need to see, try removing the slice
        content = e.get_attribute('innerHTML')
        #-----------------------------------------------Get IDs---------------------------------------------------
        try:
            idElement = driver.find_element(locate_with(By.CLASS_NAME, idClass).near(e))
            idContent = idElement.get_attribute('innerHTML')
            
            print(getTextFromAnchor(idContent)[0])
            instaID = getTextFromAnchor(idContent)[0]
        except:#Reached end of comments
            break
        #---------------------------------------------Get Comments------------------------------------------------
        if '<a' in content:
            #Checks for mentions in the comment
            content = cleanHashTags(content)
            
        print(content)
        instaComment = content
        #------------Preparing data-------------#
        instaData.append(['--',instaComment,instaID])
        
    return instaData


def getUrls():
    pUrl = input("Type profile URL : ")
    allUrls = [pUrl]
    return allUrls
    
    #GetPostURLs from profile
    #Common URL structure
    #a class = "x1i10hfl ....." href="/p/CzBbZ9xIWh4/
    #For reel, it will be /reel/CzBbsexsyhU/

instURL=input("Enter the URL : ")
instaData = getComments(instURL)
writeCSV(instaData)



