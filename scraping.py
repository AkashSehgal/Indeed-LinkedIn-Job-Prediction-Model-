#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  2 21:21:46 2020

@author: akash_sehgal
"""


from selenium import webdriver
import random
import time
import csv
import re
import os, os.path
import errno
from os import listdir
from os.path import isfile, join
import os

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise

def safe_open_w(path):
    ''' Open "path" for writing, creating any parent directories as needed.
    '''
    mkdir_p(os.path.dirname(path))
    return open(path, 'w')

def getJobs(url,index, directory,location, regex):
    
    #open the browser and visit the url
    driver = webdriver.Chrome('./chromedriver')
    driver.minimize_window()
    #driver.set_window_position(-2000,0)
    driver.get(url)
    pageSource = driver.page_source
    filename = "./"+ directory + "/" + location + "_"+ str(index)+".html"

    print( "Writing Page Source to " + filename )
    try:
        # writing to csv file  
        with safe_open_w(filename) as file:  
        # creating a csv writer object      
             file.write(pageSource)  
            
        time.sleep(random.randint(1, 5))
        
        job_title ='NA'
        
        try:
            job_title= driver.find_element_by_class_name('jobsearch-JobInfoHeader-title').text.replace('\n',' ')
        except:
            job_title='NA'
        try:
            job_Desc = driver.find_element_by_class_name('jobsearch-jobDescriptionText').text.replace('\n',' ').replace(',',' ')
        except:
            job_Desc = 'NA'
        
        job_Desc = job_Desc.lower()
        job_Desc=re.sub(regex, ' ', job_Desc)
        
        row = [job_title,job_Desc]    
        #rows.append(row)       
        filename = "./" + directory + "CSV/" + location + "_" + str(index)+ ".csv"
        fields = ["Title", "Description"];
        print( "\nWriting data to " + filename )
        # writing to csv file  
        with safe_open_w(filename) as csvfile:  
            # creating a csv writer object  
            csvwriter = csv.writer(csvfile)  
            
            # writing the fields  
            csvwriter.writerow(fields)  
            
            # writing the data rows  
            csvwriter.writerow(row)
    except:
        print( "Ignoring the file because of unknown error : " + filename)
    
    driver.quit()
 

"""
A function that uses selenium and chromedriver to get tweets from a Twitter account.
url is the link the account
scrollNum is the number of times we want to scroll to load more tweets.
"""

def getJobsUrls(url, jobUrls):
    #open the browser and visit the url
    driver = webdriver.Chrome('./chromedriver')
    driver.minimize_window()
    driver.get(url)
    time.sleep(2)


    #write the tweets to a file
    fw=open('urls.txt','a',encoding='utf8')
    writer=csv.writer(fw,lineterminator='\n')#create a csv writer for this file
    for i in range(0,1):

        
        #find all elements that have the value "tweet" for the data-testid attribute
        all_jobs = driver.find_elements_by_class_name('result')
        #print(len(tweets),' tweets found\n')
       
        for job in all_jobs:

        
            aTag='NA'
            
            try:
                aTag = job.find_element_by_tag_name("a").get_attribute("href")
            except:
                aTag = 'None'
                      
            print("Job URL : " + aTag)
            writer.writerow([aTag])
            jobUrls.append(aTag)

        #scroll down twice to load more tweets
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        
        time.sleep(2)

    fw.close()
    driver.quit();
    
def locFromUrl( url ):
    result = re.search('(.*)&l=(.*)%2C(.*)', url)
    location = result.group(2)
    return location
        
def populateJobs( filename, startIndex, endIndex, url, regex):
    
    location = locFromUrl( url )
    jobUrls = [];
    fileIndex = startIndex
    startIndex = startIndex * 10
    endIndex =  endIndex * 10
    for i in range(startIndex, endIndex, 10):
        newUrl = url + '&start=' + str(i) 
        getJobsUrls(newUrl, jobUrls)
    
    i = fileIndex * 15
    for jobsUrl in jobUrls:
        getJobs(jobsUrl, i, filename, location, regex);
        i= i + 1;
    
    print("Done")
    

def getIndeedJobs(url,regex_data):
    
    populateJobs("IndeedJobs", 0, 1,  url,regex_data) 
    

def mergecsv( directory ):
    onlyfiles = [f for f in listdir(directory) if isfile(join(directory, f))]

    
    for csvFileStr in onlyfiles:
        if csvFileStr.endswith("csv"):
            print( csvFileStr )
            csvpath = "./"+directory+"/"+csvFileStr
            csv=open(csvpath,"r")
            merged=open(directory+"_merged.csv","a")

            # Iterate over each line in the file
            
            for line in csv.readlines():
                if line.startswith("Title"):
                    #Ignoring the header.
                    line
                else :
                    merged.write(line)
            
            csv.close()
            merged.close()
            os.rename(csvpath, csvpath+".merged")
        
    

url='https://www.indeed.com/jobs?q=Data%20Engineers&l=Redmond%2C%20WA&radius=100&vjk=dd628fd803dd06db';
#regexdata = "data sci[a-z]+"
#regexdata =  "software eng[a-z]+"
regex_data = "data eng[a-z]+"
getIndeedJobs(url,regex_data)

mergecsv( "IndeedJobsCSV" )



print( "Done!")
    
    
