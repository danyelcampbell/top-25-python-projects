import sqlite3

def Database():
    global db, cursor
    #exception handling to know whether or not the query executed successfully or not
    try:
        #connected to the statistics database for the table creation
        db = sqlite3.connect('db_statistics.db')
        cursor = db.cursor()
        #created table and used the datatypes that are used in sql
        cursor.execute('''create table if not exists 'statistics' (repositoryID int, name varchar(50), url varchar(100), createdDate datetime, pushedDate datetime, description varchar(500), stars int)''')
    except Exception as E:
        print('Error: ', E)
    else:
        print('table created')
