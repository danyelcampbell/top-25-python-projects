import sqlite3
import datetime
import connection
import json
import requests
from tkinter import Tk, ttk, Button, Text, LabelFrame
from tkinter import *
import tkinter as tk

#get data from Github using API
url = 'https://api.github.com/search/repositories?q=stars:>=80000+language:python$sort=stars&order=desc'
response = requests.get(url).content
dataset = json.loads(response)

#create list to append the data
dataframe = list()

def populateView():
    tree.delete(*tree.get_children())
    connection.Database()
    for row in dataset['items']:
        description = row['description'].encode('ascii','ignore')
        description_clean = description.decode('utf-8')
        created_date = datetime.datetime.strptime(row['created_at'], '%Y-%m-%dT%H:%M:%SZ')
        pushed_date = datetime.datetime.strptime(row['pushed_at'], '%Y-%m-%dT%H:%M:%SZ')
        data = (int(row['id']), str(row['name']), str(row['url']), created_date, pushed_date, description_clean, int(row['stargazers_count']))
        tree.insert('',tk.END, values=(row['id'], row['name'], row['url'], created_date, pushed_date, description_clean, row['stargazers_count']))
    connection.cursor.execute("SELECT * FROM 'statistics' ORDER BY 'stargazers_count' DESC")
    connection.cursor.close()
    connection.db.close()

#create tk winder
window = tk.Tk()
window.title("Top 25 Most Starred Python Projects On Github")
window.geometry('800x600+0+0')

#==================================FRAME==============================================
Top = Frame(window, width=700, height=50, bd=8, relief="raise")
Top.pack(side=TOP)
Button_Group=Frame(window, width=700, height=50)
Button_Group.pack(side=TOP)
Buttons = Frame(Button_Group, width=200, height=50)
Buttons.pack(side=LEFT)
Buttons1 = Frame(Button_Group, width=500, height=50)
Buttons1.pack(side=RIGHT)
Body = Frame(window, width=700, height=300, bd=8)
Body.pack(side=BOTTOM)


#==================================LABEL WIDGET=======================================
txt_title = Label(Top, width=300, font=('times', 24), text = "Top 25 Most Starred Python Projects On Github")
txt_title.pack()

#==================================BUTTONS WIDGET=====================================


# btn_display = Button(Buttons, width=15, text="Insert Data", command=insert_data)
# btn_display.pack(side=RIGHT)

btn_display2 = Button(Buttons, width=15, text="Refresh Data", command=populateView)
btn_display2.pack(side=LEFT)

#==================================LIST WIDGET========================================
scrollbary = Scrollbar(Body, orient=VERTICAL)
scrollbarx = Scrollbar(Body, orient=HORIZONTAL)
tree = ttk.Treeview(Body, columns=("RepositoryID", "Name", "URL", "Created", "Pushed", "Description", "Stars"), selectmode="extended", height=300, yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)
scrollbary.config(command=tree.yview)
scrollbary.pack(side=RIGHT, fill=Y)
scrollbarx.config(command=tree.xview)
scrollbarx.pack(side=BOTTOM, fill=X)
tree.heading('RepositoryID', text="Repository ID", anchor=W)
tree.heading('Name', text="Name", anchor=W)
tree.heading('URL', text="URL", anchor=W)
tree.heading('Created', text="Created", anchor=W)
tree.heading('Pushed', text="Pushed", anchor=W)
tree.heading('Description', text="Description", anchor=W)
tree.heading('Stars', text="Stars", anchor=W)
tree.column('#0', stretch=NO, minwidth=0, width=0)
tree.column('#1', stretch=NO, minwidth=0, width=200)
tree.column('#2', stretch=NO, minwidth=0, width=200)
tree.column('#3', stretch=NO, minwidth=0, width=200)
tree.column('#4', stretch=NO, minwidth=0, width=200)
tree.column('#5', stretch=NO, minwidth=0, width=200)
tree.column('#6', stretch=NO, minwidth=0, width=200)
tree.pack()


if __name__ == '__main__':
    window.mainloop()
