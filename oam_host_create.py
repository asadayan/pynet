# /usr/bin/
import sys
import httplib
import json
import re
import time

def CLI(filename):
  c=[]
  fhandler=open(filename,'r')
  cli=list(fhandler)
  for i in cli:
    c.append(i[:-1])
  return c

def KEY(value):
  o=re.split('\.',value)
  return int(o[-1])

def NETVNI(value):
  o=re.split(',',value)
  return o

def INCNET(value,i,count):
  o=re.split('\.',value)
  r=map(int,o)
  if r[3] <254 and r[2]<5 :
    r[3] +=1
    r[2]=5
  elif r[3] == 255 and r[2]>5:
    r[2] +=1
  if count > 1: r[2] +=i
  r=map(str,r)
  j="."
  out=j.join(r)
  return out



c=0
bdy=[]
data=[]
final=[]
dev_data={}
############### Getting Subnet and VNI from file######################################
subnet_vni=CLI('pub_prv_subnet')
for i in subnet_vni:
  #print NETVNI(i)
  data.append(NETVNI(i))

######################################

for x,y in data:
  final.append((INCNET(x,0,1),y))

#print final



asw_dev_ip=CLI('asw_dev_ip')
asw_dev_ip.sort(key=KEY)
#print asw_dev_ip

dsw_dev_ip=CLI('dsw_dev_ip')
dsw_dev_ip.sort(key=KEY)

dst_asw=sorted(asw_dev_ip,key=KEY,reverse=True)
asw_vtep=CLI('asw_vtep')

asw_vtep.sort(key=KEY)

#print asw_vtep
dst_vtep=sorted(asw_vtep,key=KEY,reverse=True)

dsw_vtep=CLI('dsw_vtep')
vni=CLI('vni')

url = '172.25.241.50'

source_net=[]
dst_net=[]
key1=[]
key2=[]
fdata1=[]
fdata2=[]
newcount=1
index=0
ddata1={}
ddata2={}
#### x is host ip address and y is VNI ############################
for x,y in final:
  a=x
  c=1
  for i in range(1,7):
    if newcount%2==1:
      a=INCNET(a,40,c)
      if a!=None : source_net.append(a)
    elif newcount%2==0:
      a=INCNET(a,40,c)
      if a!=None : dst_net.append(a)
    c +=1

  if len(source_net) != 0:
    fdata1.append(source_net)
    key1.append((y,asw_dev_ip[index],asw_vtep[index]))
  if len(dst_net) != 0 :
    fdata2.append(dst_net)
    key2.append((y,asw_dev_ip[index],asw_vtep[index]))
  source_net=[]
  dst_net=[]
  newcount +=1
  index +=2

#print "Key1:",key1,'\n'
#print "Key1-sorted:",sorted(key1)
#print "Data1:",fdata1,'\n'
#print "Data1-sorted:",sorted(fdata1)
#print "Key2:",key2,'\n'
#print "Data2:",fdata2,'\n'

ddata1=dict(zip(key1,fdata1))
ddata2=dict(zip(key2,fdata2))

#print sorted(ddata1),'\n'
#print sorted(ddata2),'\n'


headers = {
    "Content-type": "application/json"
}


for x,y in ddata1.items():
  #print x,y,'\n\n\n'
  print  "vtep:ip =>",x[2]
  for i,j in ddata2.items():
    #print i,j,'\n\n\n'
    #print y,'\n'
    #print j,'\n'
    if i[0]==x[0]:
      for srcip in y:
        for dstip in j:
          body = {
                  "host_detect_task":
                   {
                        "sample_info" :
                        {
                            "src_ip" : srcip,
                            "dst_ip" : dstip,
                            "src_port" : 100,
                            "dst_port" : 100,
                            "protocol" : 17,
                            "samples" : 200
                         },
                                   "vni" : x[0] ,
                                   "origin_device" :x[1],
                                   "origin_vtep" : x[2],
                                   "timeout" : 50,
                                   "persistent_time" : 5

                    }

                 }
          #print body,'\n'
          conn = httplib.HTTPConnection(url, 8181)
          conn.request("POST", "/oam/host_detect_task",json.dumps(body), headers)
          response=conn.getresponse()
          if response is not None:
            print response.status, response.reason
            data = response.read()
            print data
          conn.close()

