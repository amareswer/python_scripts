'''
    Partner Support Automation Script v 1.0
    '''
import os, fileinput, csv, time, datetime
#set up variable
number_of_files = 0
number_of_calls = 0
calls_closed = 0
closure_time = 0
closure_percentage = 0
closure_list = []
account_termination = 0
configuration_request = 0
other = 0
request = 0
pin = 0
basic = 0
support = 0
nff = 0
visit = 0
rownum = 0 

def count_difference(date1,date2):
    ''' (str, str)->int

        Counter difference between two times. time2 is always greater than time 2
        if time2 is not longer than time1 call is not closed
        
        >>>count_difference("26-07-2013 at 16:57:00", "26-07-2013 at 20:05:00")
        0
        >>>count_difference("26-07-2013 at 16:57:00", "27-07-2013 at 20:05:00")
        1
    '''
    closure_time = 0
    date1 = datetime.datetime.strptime(date1, "%d-%m-%Y at %H:%M:%S")
    date2 = datetime.datetime.strptime(date2, "%d-%m-%Y at %H:%M:%S")
    closure_time = date2 - date1
    return closure_time.days

def closed_within_one_day(closure_list):
    '''(list)-> int

        Return the percentage of call closed within one day
        >>>closed_within_one_day([1,2,0])
        33
        >>>closed_within_one_day([1,2,0,0])
        25
    '''
    #len(closure_list)
    closed_within_one_day = 0
    for call in closure_list:
        #if lower 1 than day then calculate
        if call < 1:
            closed_within_one_day = closed_within_one_day + 1

    percentage = ( closed_within_one_day / len(closure_list) ) * 100
    return round(percentage)
    
''' Main Program ''' 


files_to_proceed = os.listdir()

#loop over files 
for file in files_to_proceed:
    # print(file )
    if not file == '_process_files.py' and os.path.isfile(file):
          #reset numbers for new file 
        with open(file,'r') as f:
            reader = csv.reader(f)
            print("Proceeding file", file)
            number_of_files = number_of_files + 1             
            # loop over rows in csv file
            for row in reader:
                #print(len(row))
                if rownum == 0:
                    rownum = 0    
                elif rownum >= 1 and len(row) > 1:
                    #print(repr(row))
                    number_of_calls = number_of_calls + 1
                    #service_call = row[0]
                    #print(service_call)
                    resolution = row[7]
                    subject = row[1]
                    subject = subject.lower()
                    #print(subject)
                    if  'cancellation' in subject or 'cancel' in subject or 'termination' in subject:
                        account_termination = account_termination + 1
                    elif 'config' in subject or 'migra' in subject or 'change' in subject or 'upgrade' in subject or 'enable voip' in subject or 'decommission' in subject or 'decommision' in subject:
                        configuration_request = configuration_request +1
                        #print(subject)
                    elif 'data' in subject or 'aup' in subject or 'data request' in subject:
                        request = request + 1
                    elif 'pin' in subject or 'sanity' in subject or 'sanity check' in subject:
                        pin = pin + 1
                    elif 'slow' in subject or 'issue' in subject or 'connection' in subject or 'oss error' in subject or 'error' in subject:
                        basic = basic + 1
                    elif 'install support' in subject or 'install' in subject:
                        support = support + 1
                    else:
                        if 'nff' in resolution or 'no fault found' in resolution:
                            nff = nff + 1
                        elif 'visit' in resolution or 'service visit' in resolution:
                            visit = visit + 1
                        else:
                            other = other + 1             
                    status = row[2]
                    #print(status)
                    if status == "Closed":
                        calls_closed = calls_closed + 1
                        created_time = row[5]
                        closed_time = row[6]
                        closure_time = count_difference(created_time, closed_time)
                        closure_list.append(closure_time)
                    #business_partner = row[3]
                    #type_call = row[4]                                        
                rownum = rownum + 1
            
            if ( len(closure_list) ) > 0:
                closure_percentage = closed_within_one_day(closure_list)
            with open(file[0:-4] +".txt",'a') as new_file:
                new_file.write("Total Calls: " + str(number_of_calls) + "\n" )
                new_file.write("Calls Closed: " + str(calls_closed) + "\n" )
                new_file.write("Percentage closed within 1 day: " + str(closure_percentage) +"%" + "\n" )
                new_file.write("Account Termination: " + str(account_termination) + "\n" )
                new_file.write("Configuration Request: " + str(configuration_request) + "\n" )
                new_file.write("Data Request: " + str(request) + "\n" )
                new_file.write("Install - Support: " + str(support) + "\n" )
                new_file.write("Install - Sanity Pin: " + str(pin) + "\n" )
                new_file.write("No Fault Found: " + str(nff) + "\n" )
                new_file.write("Other: " + str(other) + "\n" )
                new_file.write("Service Visit: " + str(visit) + "\n" )
                new_file.write("Basic Troubleshoot: " + str(basic) + "\n" )
                new_file.close()
                
            number_of_calls = 0
            calls_closed = 0
            closure_percentage = 0
            account_termination = 0
            configuration_request = 0
            request = 0
            support = 0
            pin = 0
            basic = 0
            nff = 0
            other = 0
            visit = 0
            rownum = 0
            closure_list[:] = []
            print(">>> Reseting Statistics after file ", file)
    else:
        print('')      
print("Number of files proceeded:", number_of_files)













        
        
    
