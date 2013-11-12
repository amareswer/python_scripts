import requests, fileinput,os,csv
from time import sleep

summary="/stats/summary/summary.html"
config_params="/cgi/execAdvCom.bin?Command=85&PrintMsg=Config%20Params"
tx_monitor="/cgi/execAdvCom.bin?Command=194&PrintMsg=TxMonitor"

def check_if_alive(ip):
    try:
        r = requests.get('http://'+ip+'',timeout=3)
    except requests.exceptions.Timeout:
        print(requests.exceptions.Timeout)
        return False
    return True

def get_logs_for(filename,ip,logs_type):
    path="logs_download/"
    r = requests.get('http://'+ip+''+logs_type+'', auth=('avanti', 'avanti'))
    with open(path+filename+".html", 'wb') as fd:
        fd.write(r.content)
    r = ""
    sleep(2)

with open("device_list.csv",'r') as f:
    reader=csv.reader(f)
    for row in reader:
        device = row[0]
        ip = row[3]
        if check_if_alive(ip) != False:
            get_logs_for(device+"_summary",ip,summary)
            get_logs_for(device+"_config_params",ip,config_params)
            get_logs_for(device+"_tx_monitor",ip,tx_monitor)
        else:
            print("Connection timed out on ip: "+ip")

#print(check_if_alive("10.32.73.6"))
#print(check_if_alive("10.32.65.202"))
       
