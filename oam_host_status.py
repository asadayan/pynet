# /usr/bin/
import sys
import httplib
import urllib
import json
import re

url = '172.25.241.50'
headers = {
    "Content-type": "application/json"
}
data={}
id=[]
z={}
idnet=[]
count=0
conn = httplib.HTTPConnection(url, 8181)
conn.request("GET", "/oam/host_detect_task")
r1=conn.getresponse()
data=r1.read()
data0=re.split('task_id',data)
taskid=re.findall(r"\"task_id...[\d\w]+-[\d\w]+-[\d\w]+-[\d\w]+-[\d\w]+",data)
status=re.findall(r".status...\w+.",data)
flow=re.findall(r".src_ip...\d+\.\d+\.\d+\.\d+...dst_ip...\d+\.\d+\.\d+\.\d+...src_port..\d+..dst_port..\d+..protocol.:\d+..samples..\d+",data)
oam=re.findall(r".vni...\d+...origin_device.:.\d+\.\d+\.\d+\.\d+.,.origin_vtep.:.\d+\.\d+\.\d+\.\d+.,.timeout.:\d+,.persistent_time.:\d+",data)
for i in status:
  id.append([i,flow[count],oam[count]])
  count=count+1
z=dict(zip(taskid,id))
print '+'*120,'\n'
for x,y in z.items():
  print x,'\n'
  print y[0],'\n'
  print y[1],'\n'
  print y[2],'\n'
  print '+'*120,'\n'


