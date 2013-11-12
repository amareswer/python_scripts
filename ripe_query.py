import urllib.request, urllib.error, fileinput,os,csv

ip = ""

with open("ip.csv",'r') as f:
    reader = csv.reader(f)
    for row in reader:
        ip = row[1]
        downloaded_data  = urllib.request.urlopen('https://apps.db.ripe.net/search/query.html?searchtext='+ip+'')
        for line in downloaded_data.readlines():
            line_to_check=str(line)
            if "country" in line_to_check:
                country_place = line_to_check.find("country") + 16
                print("IP:"+ip+" country: "+line_to_check[country_place:country_place+2]+"")
                ip=""
                country_place = 0
                
                
               
        
