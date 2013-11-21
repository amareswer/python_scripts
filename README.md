python_scripts
==============
Selection of Python Scripts written by myself.

This can be used as learning material of example of python coding.

The below is one of the examples use of threading.

import requests
import csv
import sys
import subprocess
from threading import Thread
from time import sleep

alive_ips = []
dead_ips = []
threads=[]

summary = "/stats/summary/summary.html"
config_params = "/cgi/execAdvCom.bin?Command=85&PrintMsg=Config%20Params"
tx_monitor = "/cgi/execAdvCom.bin?Command=194&PrintMsg=TxMonitor"

def check_if_alive(ip):
    try:
        r = requests.get('http://'+ip+'',timeout=3)
        #alive_ips.append(ip)
        #print(r)
        #print("Good ip"+ip+"")
        alive_ips.append(ip)
        
    except requests.exceptions.Timeout:
        #print(requests.exceptions.Timeout)
        #print("Error with"+ip+"")
        dead_ips.append(ip)
        #dead_ips.append(ip)
        #print(dead_ips)
        #return dead_ips
       #print(ip)
        #return ip
    

def get_logs_for(filename,ip,logs_type):
    path="logs_download/"
    r = requests.get('http://'+ip+''+logs_type+'', auth=('avanti', 'avanti'),timeout=3)
    with open(path+filename+".html", 'wb') as fd:
        fd.write(r.content)
    r = ""
    sleep(2)




with open("device_list.csv",'r') as f:
    reader=csv.reader(f)
    for row in reader:
        device = row[0]
        ip = row[3]
        #if check_if_alive(ip) != False:
        t1 = Thread(target=get_logs_for, args=(device+"_summary",ip,summary,))
        threads.append(t1)
        t2 = Thread(target=get_logs_for, args=(device+"_config_params",ip,config_params,))
        threads.append(t2)
        t3 = Thread(target=get_logs_for, args=(device+"_tx_monitor",ip,tx_monitor,))
        threads.append(t3)
        #else:
        # print("Connection timed out on ip: "+ip+"")

for i in range(len(threads)):
    try:
        threads[i].start()
    except requests.exceptions.Timeout:
        print("Error with"+threads[i]+"")
    
"""
checks = []

with open("device_list.csv",'r') as f:
reader=csv.reader(f)
for row in reader:
device = row[0]
ip = row[3]
# print(ip)
t4 = Thread(target=check_if_alive, args=(ip,))
checks.append(t4)
for i in range(len(checks)):
sleep(0.5)
checks[i].start()

#print(alive_ips)

for i in range(len(alive_ips)):
try:
print(alive_ips[i])
t1 = Thread(target=get_logs_for, args=(device+"_summary",str(alive_ips[i]),summary,))
threads.append(t1)
t2 = Thread(target=get_logs_for, args=(device+"_config_params",str(alive_ips[i]),config_params,))
threads.append(t2)
t3 = Thread(target=get_logs_for, args=(device+"_tx_monitor",str(alive_ips[i]),tx_monitor,))
threads.append(t3)
except:
print("Error with"+alive_ips[i]+"")

for i in range(len(threads)):
threads[i].start()
sleep(2)
#print(check_if_alive("10.32.73.6"))
#print(check_if_alive("10.32.65.202"))

"""
