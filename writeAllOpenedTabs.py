# -*- coding: utf-8 -*-
"""
Created on Wed Nov  1 13:38:31 2023

@author: Krishna
"""
from selenium import webdriver

with open('links.txt', 'at', newline='', encoding='utf-8') as f:
    
    driver = webdriver.Chrome()
    driver.get("https://www.instagram.com/")
    urls = []
    
    
    #Collecting all URLs-------------------------------------------------------
    input("Press any key when you're ready")
    for i in range(0, len(driver.window_handles), 1):
        driver.switch_to.window(driver.window_handles[i])
        urls.append(driver.current_url)
    
    
    #Removing redundancy-------------------------------------------------------      
    urls = list(dict.fromkeys(urls))
    
    
    
    #Writing to the file-------------------------------------------------------      
    for url in urls:
        f.write(f"{url}\n")
    f.close()
    
    '''LOGIN TO INSTA, ONCE IT'S OPENED, OPEN MAXIMUM TABS'''
        
    print(urls)
    print("\n\n\n\nDone")
    driver.quit()
