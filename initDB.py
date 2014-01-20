#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3
import settings

def initDB():
	try:
		conn = sqlite3.connect(settings.DATABASE)
		print "connection is open"
		curs = conn.cursor()
		curs.execute("CREATE TABLE IF NOT EXISTS users (id integer not null primary key autoincrement, name varchar(20) not null, password varchar(100) not null)")
		
		curs.execute("CREATE TABLE IF NOT EXISTS categories (id integer not null primary key autoincrement, title varchar not null)")
	
		curs.execute("CREATE TABLE IF NOT EXISTS c2u (id integer not null primary key autoincrement, fk_user integer not null, fk_category integer not null, FOREIGN KEY (fk_user) REFERENCES users(id), FOREIGN KEY (fk_category) REFERENCES categories(id))")
	
		curs.execute("CREATE TABLE IF NOT EXISTS payments (id integer not null primary key autoincrement, summ REAL not null, comment VARCHAR, date DATE not null, mul INTEGER not null ,fk_c2u INTEGER not null, FOREIGN KEY (fk_c2u) REFERENCES c2u(id)) ")
		print "tables were created"
		conn.commit()
	except sqlite3.Error,e:
		print e.args[0]
	finally:
		if conn:
			conn.close()
			print "connection closed"	
def fillDefault():
	try:
		conn = sqlite3.connect(settings.DATABASE)
		curs = conn.cursor()
		curs.execute("INSERT INTO categories(title) VALUES('Еда')")
		curs.execute("INSERT INTO users(name,password) VALUES('alex','123')")
		curs.execute("INSERT INTO c2u(fk_user,fk_category) VALUES(1,1)")
		conn.commit()
	except sqlite3.Error, e:
		print e.args[0]
	finally:
		if conn:
			conn.close()


def dropAllTables():
	try:
		conn = sqlite3.connect(settings.DATABASE)
		curs = conn.cursor()
		curs.execute("DROP TABLE payments")
		curs.execute("DROP TABLE c2u")
		curs.execute("DROP TABLE categories")
		curs.execute("DROP TABLE users")
		conn.commit()
		print "Tables were droped"
	except sqlite3.Error,e:
		print e
	finally:
		if conn:
			conn.close
			

def reInit():
	dropAllTables()
	initDB()
	fillDefault()
	
				
				
if __name__ == "__main__":
	#curs.execute("INSERT INTO users(name, password) values('alex','123')")
	
	reInit()
