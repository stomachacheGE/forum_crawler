# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import sqlite3
import os

current_path = os.getcwd()
database_path = current_path + '/database_krebs.db'

#print(database_path)

with sqlite3.connect(database_path) as conn:
    cursor = conn.cursor()
    cursor.execute('SELECT SQLITE_VERSION()')
    version = cursor.fetchone()
    print('Initialized database: %s' % database_path)
    print('SQLite version: %s'% version)
    