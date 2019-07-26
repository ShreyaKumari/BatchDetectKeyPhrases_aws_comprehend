# -*- coding: utf-8 -*-
"""
Created on Fri Jul 26 11:24:49 2019

@author: shreya kumari
"""

import boto3
import json
client = boto3.client('comprehend',region_name='us-east-1')
filename = "pdf_log.txt"

def fun(y):
    if 'ResultList' in y :
                     print(len(y['ResultList'])) 
                     n=len(y['ResultList'])
                     i=0
                     while(i<n):
                         n1=len(y['ResultList'][i]['KeyPhrases'])
                         j=0
                         while(j<n1):
                             score=y['ResultList'][i]['KeyPhrases'][j]['Score']
                             word=y['ResultList'][i]['KeyPhrases'][j]['Text']
                             ans.update({word:score})
                             j=j+1
                         i=i+1
countdoc=0
countbytes=0
ans={}
pass1=[]
text=""
count=0
cou=1
with open(filename, 'r') as filehandle:
    for line in filehandle:
        a=countbytes+(len(text.encode('utf-8')))
        if(a<=5000):
            text=line+text
            countbytes=a
        else:
            if(countdoc<=25):
               countdoc=countdoc+1
               pass1.append(text)
               pass1.append('.')
            else:
                 x=json.dumps(client.batch_detect_key_phrases(TextList=pass1, LanguageCode='en'), sort_keys=True, indent=4)
                 y = json.loads(x)
                 fun(y)
                 pass1=[]
                 countdoc=0
            text=line
            countbytes=0                     
if(countdoc>0):
    count=count+1
    x=json.dumps(client.batch_detect_key_phrases(TextList=pass1, LanguageCode='en'), sort_keys=True, indent=4)
    y = json.loads(x)
    fun(y)
                    
                    
    
a=len(ans)
for key, value in sorted(ans.items(), key=lambda item: item[1]):
    if(count>=a-4):
         with open('resultt.txt', 'a') as outfile:
             outfile.write(key)
             outfile.write("\n")
         print("%s: %s" % (key, value))
    count=count+1            
print("Done!")


