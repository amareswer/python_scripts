import os, csv, datetime, time, socket, subprocess

server_list = "servers.csv";
dump_directory = "\\d$\\_DumpsBackups\\";
servers="";
f="";
right_now = time.time()
raportOlderThan=7;
start = time.time();
no_servers=0;
output_file="DumpBackupsFolderServerCheckResult.txt"
sock = socket.socket()
allfilesize=0
totalfiles=0


def main():
    global output_file
    global tofile
    with open(output_file,"w") as tofile:
        a= "Reporting files older than: " + str(raportOlderThan) + " days\n";
        print a
        saveResultToFile(tofile,a)
        setServerList(server_list)
        b = 'Checked ' + str(no_servers) + " servers \n"
        print b
        saveResultToFile(tofile,b)
    
        c = 'Checked in %.2f second \n' % (time.time() - start)
        print c
        saveResultToFile(tofile,c)
    
        d = "By removing these files we could save approx. %d GB \n" % (allfilesize/1000)
        print d
        saveResultToFile(tofile,d)
    
        e = 'Total number of files discovered %d \n' % (totalfiles)
        print e
        saveResultToFile(tofile,e)
    tofile.close

def findPathToDumpFolder(server):
    indirectory = "\\\\" + server[0] + "\\d$\\"
    try:
        if (os.path.exists(indirectory)):
            dd = os.listdir(indirectory)
            for d in dd:
                if (d[0:5] == "_Dump"):
                    return indirectory+d
            else:
                return False
    except:
        return False
    

def checkModificationDate(filetocheck):
    global allfilesize
    global totalfiles
    
    datemod = os.stat(filetocheck).st_mtime
    filesize = os.stat(filetocheck).st_size
     
    fileIsOld = right_now - datemod
    d = divmod(fileIsOld,86400)
    
    if d[0] >= raportOlderThan:
        try:
            allfilesize=allfilesize + filesize/1024/1024
            totalfiles = totalfiles + 1
            return filetocheck + " "' Days old: %d Size: %d mb' % (d[0],filesize/1024/1024)
        except:
            print "Could not get a file size"
    
def checkForOldFilesIn(path):
    files = os.listdir(path)
    for onefile in files:
        pathtofile = checkModificationDate(path+"\\"+onefile)
        if pathtofile!=None:
            print pathtofile
            saveResultToFile(tofile,pathtofile+"\n")
            
    
def setServerList(server_list):
    with open(server_list,'r') as f:
        global no_servers
        global sock
        servers = csv.reader(f)
        for server in servers:
            no_servers = no_servers+1;
            path = findPathToDumpFolder(server)
            if (path):
                a= "Checking Server: " + str(server[0])
                print a
                saveResultToFile(tofile,a+"\n")
                checkForOldFilesIn(path)
            else:
                a= "Server: " + str(server[0] + " cannot be accessed")
                print a
                saveResultToFile(tofile,a+"\n")
                
                        
def saveResultToFile(tofile,contents):
    tofile.write(contents)     

main()
 
        
