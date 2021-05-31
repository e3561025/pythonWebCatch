# -*- coding: utf-8 -*-
"""
Created on Mon Feb 25 11:25:06 2019

@author: 蔡元堯
"""
import sqlite3
import random
conn=sqlite3.connect('mydb.sqlite3')
print(conn)
c=conn.cursor()
'''c.execute("""
          CREATE TABLE score(
          id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
          name TEXT NOT NULL,
          math TEXT NOT NULL,
          chinese TEXT NOT NULL
          )
          """)'''
number=int(input('input the number:'))
#name=['aa','bb','cc','dd']
#math=[50,70,60,99]
#chinese=[50,60,44,33]

for i in range(0,number):
    name=input("name:")
    #a=str(111)
    #print(a)
    string=("INSERT INTO score VALUES("+str(i+1)+",'"+name+"','"+str(random.randint(0,100))+"','"+str(random.randint(0,100))+"')")
    print(string)
    #c.execute("INSERT INTO address VALUES(2,'hello','hello@gmail.com')")

    c.execute(string)
print('success')
c.execute('SELECT * FROM score ')
for i in c.fetchall():
    print(i)
conn.close()