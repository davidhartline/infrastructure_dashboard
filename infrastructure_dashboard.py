import tkinter as tk
import time
import datetime
from datetime import datetime
import load_tables

#variables
refresh_interval = 1000 * 60 * 10 #the time (in ms) between refreshes

def get_uniques_from_column(array,column):
    uniques = []
    i = 0 #
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
    return(len(uniques))       
        

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
    return(uniques)   



class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

    def createWidgets(self):
        self.now = tk.StringVar()
        self.time = tk.Label(self, bg='white',font=('Helvetica', 24))
        self.time.pack(side="top")
        self.time["textvariable"] = self.now
        global frame1
        frame1 = tk.Frame(height=2, bd=1)
        tk.Label(frame1,text='last_reminder', relief=tk.RIDGE, bg='white', width=15, fg='black', font=("Helvetica",10)).grid(row=1,column=0)

        frame1.pack()
        self.QUIT = tk.Button(self, text="QUIT", fg="red",
                                            command=root.destroy)
        self.QUIT.pack(side="bottom")
        self.onUpdate()

    def onUpdate(self):

        now2 = datetime.now()
        current_time = now2.strftime("%m/%d %I:%M %p")
        self.now.set('Infrastructure Status \n Last refreshed: ' + current_time)
        

        for widget in frame1.winfo_children():
            widget.destroy()
        

        infrastructure_table = load_tables.get_infrastructure_table()
        infrastructure_categories = get_infrastructure_categories(infrastructure_table,1) 


        row = 0
        column = 0
        i = 0
        while (i < len(infrastructure_table)):
            infrastructure_item = infrastructure_table[i][0]
            infrastructure_group  = infrastructure_table[i][1]
            status = infrastructure_table[i][2]
            cell_fg = infrastructure_table[i][5]
            cell_bg = infrastructure_table[i][6]
            category_bg_color = infrastructure_table[i][7]
            
            if (i == 0 or infrastructure_table[i][1] != infrastructure_table[i-1][1]): #if new group, start new group label
                group_label_column = column

                if(i == 0):
                    row = 0
                else:
                    row = row
                while(group_label_column%3!=0 ): #increase column count until it is divisible by 3
                    group_label_column = group_label_column + 1
               
                tk.Label(frame1,text=infrastructure_group, relief=tk.RIDGE, bg=category_bg_color, width=39, fg=cell_fg, font=("Helvetica",20)).grid(row=row,column=group_label_column,columnspan = 3)
                row = row+1
        
            tk.Label(frame1,text=infrastructure_item, relief=tk.RIDGE, bg=cell_bg, width=15, fg=cell_fg, font=("Helvetica",17)).grid(row=row,column=column)
            tk.Label(frame1,text=status, relief=tk.RIDGE, bg=cell_bg, width=15, fg=cell_fg, font=("Helvetica",17)).grid(row=row+1,column=column)
            #if(i+1 < len(infrastructure_table)and infrastructure_table[i+1][1] == infrastructure_table[i][1]):
            column = column + 1
            if(i+1 < len(infrastructure_table)and infrastructure_table[i+1][1] != infrastructure_table[i][1]): #start a new grouping if the next item is a different category
                while(column%3!=0 ): 
                    column += 1            
            
            #if we reached the end of a line on a group, hit enter and start a new line
            if (column != 0 and column%3==0 ): 
                column = column - 3
                row = row + 2
                
            #go to the next stack, if we have filled up the current stack and we are on to a new group
            if (row > 25 and i+1 < len(infrastructure_table)and infrastructure_table[i+1][1] != infrastructure_table[i][1]):
                row = 0
                column+=1
                while(column%3!=0 ): #increase column count until it is divisible by 3
                    column += 1

            i = i + 1                                   
            

        self.after(refresh_interval, self.onUpdate)


root = tk.Tk()
app = Application(master=root)
root.mainloop()