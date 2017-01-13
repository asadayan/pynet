#/usr/bin/
import sys
import re
import os

#filename=sys.argv[1]
def CLI(filename):
  c=[]
  fhandler=open(filename,'r')
  cli=list(fhandler) 
  for i in cli:
    c.append(i[:-1])
  return c

#print CLI(filename)


