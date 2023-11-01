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


def cleanHashTags(content): #Replaces all anchors with hashTags
    CLEANR = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
    content = re.sub(CLEANR, '', content)
    return content

    

def setClasses():
    '''cmntClass = input("\nEnter the comment class :")
    #_aacl, #Span covering Comments. #The classes will change, so correct it. Previously _aade
    idClass = input("\nEnter the ID class :")
    #If not logged in, use h3 class, Previously _a9zc'''
    
    
    cmntClass, idClass = '',''
    
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
    for e in elements[2:-2]:#Trim down the post content and leave the comments. If you need to see, try removing the slice
        content = e.get_attribute('innerHTML')
        
        #-----------------------------------------------Get IDs---------------------------------------------------
        try:
            idElement = driver.find_element(locate_with(By.CLASS_NAME, idClass).near(e))
            idContent = idElement.get_attribute('innerHTML')
            
            print(cleanHashTags(idContent))
            instaID = cleanHashTags(idContent)
        except:#Reached end of comments
            break
        #---------------------------------------------Get Comments------------------------------------------------
        
        #----------------------------------------------Anchors----------------------------------------------------
        
        skipContent = 0
        if '<a' in content:
            content = cleanHashTags(content)
                
            if(not(('#' in content) or ('@' in content))): #Not hash tags, not mentions
                skipContent = 1
        
        if(skipContent == 0):
            print(content)
            instaComment = content
            
            #----------------------------------------Preparing data-----------------------------------------------
            instaData.append(['--',instaComment,instaID])
        
    return instaData


def setProfClass():
    #profClass = input("\nEnter the post class :")
    profClass = 'x1i10hfl' 
    if(profClass ==''):
        profClass = '_aacl'
    return profClass


def getUrls(pUrl):
    #pUrl = input("Type profile URL : ")
    #pUrl = "https://www.instagram.com/therock/"
    allUrls = []
    
    driver = webdriver.Chrome()
    driver.get(pUrl)
    driver.implicitly_wait(30)
    
    profClass = setProfClass()
    posts = driver.find_elements(By.CLASS_NAME,profClass)
    
    for p in posts[:]:
        pHref = p.get_attribute('href')
        if(('https://www.instagram.com/reel/' in str(pHref)) or ('https://www.instagram.com/p/' in str(pHref))):
            print(pHref)
            allUrls.append(pHref)
        
    return allUrls

'''
allUrls = getUrls(input("Type profile URL : "))

for posts in allUrls:
    instURL = posts
    instaData = getComments(instURL)
    writeCSV(instaData)
'''

instURL = 'https://www.instagram.com/reel/Cy9b2u5PV25/'
instaData = getComments(instURL)
writeCSV(instaData)



