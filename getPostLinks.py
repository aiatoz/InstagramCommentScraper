# -*- coding: utf-8 -*-
"""
Created on Wed Nov  1 10:10:05 2023

@author: Krishna
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.relative_locator import locate_with
import re
import csv
#import os

def setProfClass():
    profClass = input("\nEnter the post class :")
    #_aacl, #Span covering Comments. #The classes will change, so correct it. Previously _aade
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
    
allUrls = getUrls(input("Type profile URL : "))