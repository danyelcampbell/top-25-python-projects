import sqlite3
import datetime
import time
import connection
import requests
import json
import webbrowser
import tkinter as tk
from tkinter import Tk, ttk, Button, Text, LabelFrame
from tkinter import *
from tkinter.ttk import Progressbar


def populateView():
    #get data from Github using API
    url = 'https://api.github.com/search/repositories?per_page=25&q=language:python'
    response = requests.get(url).content
    dataset = json.loads(response)
    print('data fetched successfully')

    #deletes the tree, important during data refresh
    tree.delete(*tree.get_children())
    connection.Database()

    for row in dataset['items']:
        #checks to see if description column has any empty records
        if (row['description'] is not None):
            description = row['description'].encode('ascii','ignore')
            description_clean = description.decode('utf-8')
        else:
            description_clean = row['description']

        #cleans created and pushed dates, getting rid of T and Z from raw data
        created_date = datetime.datetime.strptime(row['created_at'], '%Y-%m-%dT%H:%M:%SZ')
        pushed_date = datetime.datetime.strptime(row['pushed_at'], '%Y-%m-%dT%H:%M:%SZ')

        #inserts data into tkinter treeview
        tree.insert('',tk.END, values=(row['id'], row['name'], row['html_url'], created_date, pushed_date, description_clean, row['stargazers_count']))

    connection.cursor.execute("SELECT * FROM statistics")
    connection.cursor.close()
    connection.db.close()

#create tk winder
window = tk.Tk()
window.title("Top 25 Most Starred Python Projects On Github")
window.geometry('800x600+0+0')

#==================================FRAME==============================================

Top = Frame(window, width=700, height=50, bd=8)
Top.pack(side=TOP)
Button_Group=Frame(window, width=700, height=50)
Button_Group.pack(side=TOP)
Buttons = Frame(Button_Group, width=200, height=50)
Buttons.pack(side=LEFT)
Body = Frame(window, width=700, height=300, bd=8)
Body.pack(side=BOTTOM)

#==================================LABEL WIDGET=======================================

txt_title = Label(Top, width=300, font=('times', 24), text = "Top 25 Most Starred Python Projects On Github")
txt_title.pack()

#==================================BUTTONS WIDGET=====================================

#function to change button text upon click
def update_btn_text():
    btn_text.set("Refresh Data")

#what will happen when button is clicked
def button_commands(evt=None):
    populateView()
    update_btn_text()

#tkinter string variable for button
btn_text = StringVar()

btn_display = Button(Buttons, width=15, textvariable=btn_text, command=button_commands)

#initial button text
btn_text.set("Fetch Data")
btn_display.pack(side=LEFT) #shows the button in window

#==================================LIST WIDGET========================================

#makes each row in treeview clickable, will open url to repository in new window or tab
def selectURL(event):
    curItem = tree.focus()
    contents = tree.item(curItem)
    URL = contents['values'][2]
    webbrowser.open('{}'.format(URL))

scrollbary = Scrollbar(Body, orient=VERTICAL)
scrollbarx = Scrollbar(Body, orient=HORIZONTAL)
tree = ttk.Treeview(Body, columns=("RepositoryID", "Name", "URL", "Created", "Pushed", "Description", "Stars"), selectmode="extended", height=300, yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)
scrollbary.config(command=tree.yview)
scrollbary.pack(side=RIGHT, fill=Y)
scrollbarx.config(command=tree.xview)
scrollbarx.pack(side=BOTTOM, fill=X)
tree.bind("<Double-1>", selectURL)
tree.heading('RepositoryID', text="Repository ID", anchor=W)
tree.heading('Name', text="Name", anchor=W)
tree.heading('URL', text="URL", anchor=W)
tree.heading('Created', text="Created Date", anchor=W)
tree.heading('Pushed', text="Last Pushed Date", anchor=W)
tree.heading('Description', text="Description", anchor=W)
tree.heading('Stars', text="Number Of Stars", anchor=W)
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
