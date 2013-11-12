import os, fileinput, csv, time, datetime
signal = ""
rate = ""
file_ignored=0
path ="logs/"

config_params = []
info = []

def summary(f):
    """file -> list
    Return True if rate and signal found
    """
    info=[]
    signal = ""
    rate = ""
    line_number = 0
    current_sid=f[0:8]
    info.append(current_sid)
    for line in fileinput.input(path+f):
        line_number = line_number + 1
        if line_number == 9:
           signal = line[30:32]
           info.append(signal)
        if line_number == 17:
           rate = line[18:27]
           if "512" in rate:
               rate= rate.strip()
           info.append(rate)
    return info

def check_gps_cords(f):
    signal = ""
    config_params=[]
    current_sid=f[0:8]
    line_number = 0
    config_params.append(current_sid)
    for line in fileinput.input(path+f):
        line_number = line_number + 1
        if  21 >= line_number >= 16:
           # print(line_number)
            #print(line[41:46])
            config_params.append(line[41:46])
    return config_params

# START ANALYSING

files = os.listdir(path)

for f in files:
    #print(f)
    size = (os.stat(path+f))
    #print(size.st_size)
    if 2800 > size.st_size > 1000:
        if "Summary" in f:
           info_list = (summary(f))
           if len(info_list) > 2:
               with open("output.csv", "a", newline='') as output:
                   writer = csv.writer(output)
                   writer.writerow([info_list[0],info_list[1],info_list[2]])

        if "Config_Params" in f:
            gsp_cords=check_gps_cords(f)
            if len(gsp_cords) > 4:
                with open("config_params.csv", "a", newline='') as output:
                    writer = csv.writer(output)
                    writer.writerow([gsp_cords[0],gsp_cords[1],gsp_cords[2],gsp_cords[3],gsp_cords[4],gsp_cords[5], gsp_cords[6]])
    else:
        file_ignored = file_ignored + 1

print("Files Ignored: ",file_ignored)

          






