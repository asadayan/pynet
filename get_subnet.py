# /usr/bin/
import sys
import httplib
import urllib
import json
import re
import config



url = config.URL()
headers = config.HEADERS()
data={}
count=0
net_list=[]
def subnet():
  conn = httplib.HTTPConnection(url)
  conn.request("GET", config.SUBNETS())
  r1=conn.getresponse()
  data=r1.read()
  subnet=re.findall(r"[\d]+\.[\d]+\.[\d]+\.[\d]+",data)
  for i in subnet:
    if  i[-1]=='0':
      net_list.append(i)
  conn.close()
  return net_list


