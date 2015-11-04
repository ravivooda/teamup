#!/usr/bin/python
# -*- coding: utf-8 -*-

import MySQLdb as mdb
import sys

def getDB(test=False):
    try:
        con = mdb.connect('localhost','root','jugaadomysql123','JUGAADO');
        if test:
            print "Awesome you connected"
        return con
    except Exception,e:
        print "Error occurred in fetching the database"
        return None

def execute(query):
    try:
        con = getDB()
        cur = con.cursor()
        cur.execute(query)
    except mdb.Error, e:
        print "Error occurred in executing query:\n\t %s\n\tErrors:\n\t%s" % (query, e)
        sys.exit(1)
    finally:
        if con:
            con.close()

def read(query):
    try:
        con = getDB()
        cur = con.cursor(mdb.cursors.DictCursor)
        cur.execute(query)
        return cur.fetchall()
    except mdb.Error, e:
        print "Error occurred in reading query:\n\t %s\n\tErrors:\n\t%s" % (query, e)
        return None
    finally:
        if con:
            con.close()

def read_one(query):
    result = read(query)
    if result:
        return result[0]
    return None

def write(query):
    try:
        con = getDB()
        cur = con.cursor()
        #query = query + " SELECT LAST_INSERT_ID()"
        cur.execute(query)
        con.commit()
        return cur.lastrowid
    except mdb.Error, e:
        print "Error occurred in writing query:\n\t %s\n\tErrors:\n\t%s" % (query, e)
        return None
    finally:
        if con:
            con.close()


if __name__ == "__main__":
    getDB(test=True)
