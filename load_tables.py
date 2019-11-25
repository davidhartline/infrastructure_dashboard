import csv
import getreminders





def check_status_of_infrastructure_item(infrastructure_item):
    #ticket_table = []
    displayed_status = 'nominal'
    current_status = 'nominal'
    ticket = 'N/A'
    with open('tickets.csv',newline='') as csvfile:
        reader = csv.reader(csvfile,delimiter=',',quotechar='|')
        for row in reader:
            if(infrastructure_item == row[0]):
                ticket = row[1]
                api_ticket_check_status = getreminders.getTicketInfo(ticket)[4]
                is_ticket_active = 'no'
                status_from_csv = row[2]
                if(api_ticket_check_status != 'Closed' and api_ticket_check_status != 'Resolved'):
                    is_ticket_active = 'yes'
                if (current_status == 'nominal' and is_ticket_active=='yes'):
                    current_status=status_from_csv
                elif(current_status == 'issue' and  is_ticket_active=='yes'):
                    if (status_from_csv == 'major issue' or status_from_csv == 'outage'):
                        current_status=status_from_csv
                    
                    
                #print(infrastructure_item +' api_ticket_check_status of ' + ticket + ' is ' + api_ticket_check_status)
                if (api_ticket_check_status != 'Closed' and api_ticket_check_status != 'Resolved'):
                    current_status = row[2]
                    displayed_status = row[1]
                #ticket = 'N/A'
    return(displayed_status,current_status,ticket)         

def get_infrastructure_categories(array,column):
    uniques = []
    i = 0
    while (i < len(array)):
        j = 0
        is_unique = 1
        while (j < len(uniques)):
            if (array[i][column] == uniques[j]):
                is_unique = 0
            j+=1
        if(is_unique == 1):
            uniques.append(array[i][column])
        i +=1
    return(uniques)   #dont return the header
    #return(uniques)    
 
def correct_infrastructure_item_group_color(infrastructure_table):

           
    infrastructure_group_cell_color = '#01a050'
    
    unique_categories  = get_infrastructure_categories(infrastructure_table,1)
    unique_category_colors = ['#00a04e'] * len(unique_categories)
    unique_category_statuses = ['nominal'] * len(unique_categories)
    #print(unique_category_colors)
    i = 0
    while (i < len(unique_categories)):
        j = 0
        while (j < len(infrastructure_table)):
            if (infrastructure_table[j][1] == unique_categories[i]):
                current_status =  check_status_of_infrastructure_item(infrastructure_table[j][0])[1]
                #print(infrastructure_table[j][1])
                if(current_status == 'issue' and unique_category_statuses[i] != 'major issue' and unique_category_statuses[i] != 'outage'):
                    unique_category_statuses[i] = 'issue'
                    unique_category_colors[i] = '#ffff00'                    
                elif(current_status == 'major issue'and unique_category_statuses[i] != 'outage'):
                    unique_category_statuses[i] = 'major issue'                
                    unique_category_colors[i] = '#ff9900'   
                elif(current_status == 'outage'):
                    unique_category_statuses[i] = 'outage'                
                    unique_category_colors[i] = '#ff0000'                      
                    
            j+=1
        i+=1
        
    
    #add the colors to the array that was passed here
    i = 0
    while (i < len(infrastructure_table)):
        j = 0
        while (j < len(unique_categories)):
            if (infrastructure_table[i][1] == unique_categories[j]):
                
                infrastructure_table[i][7] = unique_category_colors[j]
            j+=1
        i+=1    
    #print(infrastructure_table[7])
    print('unique_category_statuses ' + str(unique_category_statuses))
    return(infrastructure_table)    


def get_infrastructure_table():
    infrastructure_table = [["infrastructure_item","infrastructure_group","status"]]
    default_infrastructure_group_status_color = '#01a050'
    with open('infrastructure.csv',newline='') as csvfile:
        reader = csv.reader(csvfile,delimiter=',',quotechar='|')
        for row in reader:
            if (row == 0): #ignore the header row
                do_nothing = 1 #do nothing
            else:    
                values = check_status_of_infrastructure_item(row[0])
                displayed_status = values[0]
                current_status = values[1]
                ticket = values[2]

                #assign cell colors
                cell_fg = 'black'
                cell_bg = 'white'
                
                if(current_status == 'issue'):
                    cell_bg = '#ffff00'
                elif(current_status == 'nominal'):
                    cell_bg = '#bbf1d3'               
                elif(current_status == 'major issue'):
                    cell_bg = '#ff9900'   
                elif(current_status == 'outage'):
                    cell_bg = '#ff0000'                      
                                
                                
                                
                infrastructure_table.append([row[0],row[1],displayed_status,current_status,ticket,cell_fg,cell_bg,default_infrastructure_group_status_color])
    infrastructure_table = correct_infrastructure_item_group_color(infrastructure_table[2:len(infrastructure_table)])  #don't return the header & correct some colors          
                
    return(infrastructure_table) 

