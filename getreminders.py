import requests
import json
import time
import datetime
from datetime import datetime






def getTicketInfo(ticketNum):
    url = "!!!!!PUT YOUR URL HERE!!!!!!!!!!!" + str(ticketNum)

    querystring={"OPERATION_NAME":"GET",
                "TECHNICIAN_KEY":"!!!!!!!!!!PUT YOUR KEY HERE!!!!!!!!!", #change this to your technician key
                 "format":"json"}

    headers = {
        "Authtoken: !!!!!!!!!!PUT YOUR KEY HERE!!!!!!!!!"
        }


    response = requests.request("GET",url,params=querystring)
    newResponse = response

    response_data = response.json()
    
    ticketExists = 0
    if (response.content.decode('utf-8').find('request') > -1):#only searches JSON if ticket exists
        ticketExists = 1



    #last update time
    timetext = 'ERROR'
    if (ticketExists == 1):#only searches JSON if ticket exists
        createtimedetail = str(response_data["request"]["last_updated_time"]) 
        if( createtimedetail.find('None') > -1): ##if the ticket has never been updated, report the create time as the last update time
            timetext = response_data["request"]["created_time"]["display_value"]
        else:
            timetext = response_data["request"]["last_updated_time"]["display_value"]
    else:
        timetext = "NO_TICKET"


    #client
    client = 'ERROR'
    if(ticketExists ==1):
        client = str(response_data["request"]["requester"]["name"]) 
        
    #technician    
    technician = 'ERROR'
    if(ticketExists ==1):
        technicanTest = str(response_data["request"]["technician"])
        if(technicanTest.find('None') > -1):
            technician = "Not Assigned"
        else:    
            technician = str(response_data["request"]["technician"]["name"]) 
        
    #create time
    createtime = 'ERROR'
    if(ticketExists ==1):
        createtime = response_data["request"]["created_time"]["display_value"]     
        
    #status
    status = 'ERROR'
    if(ticketExists ==1):
        status = response_data["request"]["status"]["name"]    

    #priority
    priority = 'ERROR'
    if(ticketExists ==1):
        #createtimedetail = response_data["request"]["priority"]
        ##print(createtimedetail)
        if(response.content.decode('utf-8').find('priority') > -1): 
            try:
                priority = response_data["request"]["priority"]["name"] 
            except Exception:
                #sys.exc_clear()
                priority = 'Unassigned'
        else:
            priority = 'Unassigned'   

                  
        
    lastUpdateTime = timetext    
    return(createtime, lastUpdateTime,client,technician,status, priority)
    
def daysSinceLastUpdate(updateTime):
    current_local_time = time.localtime()

    ###print(createTime)
    ##print(updateTime)
    
    #parsedCreateTime = time.strptime(createTime, "%m/%d/%Y %I:%M %p")
    parsedUpdateTime = time.strptime(updateTime, "%m/%d/%Y %I:%M %p")
    seconds_since_update = time.mktime(current_local_time) - time.mktime(parsedUpdateTime)
    days_since_update = seconds_since_update / 60 / 60 / 24
    
    return(days_since_update)


def businessDaysSinceTime(updateTime):
    current_local_time = time.localtime()

    ###print(createTime)
    ##print(updateTime)
    
    #parsedCreateTime = time.strptime(createTime, "%m/%d/%Y %I:%M %p")
    parsedUpdateTime = time.strptime(updateTime, "%m/%d/%Y %I:%M %p")
    seconds_since_update = time.mktime(current_local_time) - time.mktime(parsedUpdateTime)

    hours = 0
    businessDays = 0
    currentDay = 'NULL'
    tempTime = time.mktime(parsedUpdateTime)
    while (tempTime < time.mktime(current_local_time)):
        date = datetime.fromtimestamp(tempTime) #date = datetime.fromtimestamp(time.localtime())
        ##print(date.strftime("%A"))
        if(date.strftime("%A") != currentDay):
            currentDay = date.strftime("%A")
            if(currentDay != 'Saturday' and currentDay != 'Sunday'):
                businessDays += 1
        tempTime+=(60*60)
        hours+=1
        
    if (hours < 24):
        businessDays = hours/100
    return(businessDays)
    
