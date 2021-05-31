# -*- coding: utf-8 -*-
"""
Created on Mon Feb 25 10:29:12 2019

@author: 蔡元堯
"""

import sqlite3
conn = sqlite3.connect('mydb.sqlite3')
print(conn)
c = conn.cursor()
"""c.execute(
        '''
        CREATE TABLE address(
        id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
        name TEXT NOT NULL,
        email TEXT NOT NULL
        )
        '''
        )"""

c.execute("INSERT INTO address VALUES(1,'justin','test@gmail.com')")
c.execute("INSERT INTO address VALUES(2,'hello','hello@gmail.com')")
c.execute("UPDATE address SET name='ppppp' WHERE id='2' ")
c.execute("SELECT id,email FROM address WHERE name='hello' AND email='hello@gmail.com' ")
print(c.fetchall())
conn.close()
