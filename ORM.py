#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3
import datetime
import settings

def hashPass(pwd):
	return pwd
def fillPaymentsList(dl):
	pl=[]
	for data in dl:
		pl.append({'id':data[0],'summ':data[1],'comment':data[2],'date':data[3],'mul':data[4],'fk_c2u':data[5],'category_title':data[6]})				
	return pl
	
class Users:
	id = None
	name = None
	password = None
	
	
	def newUser(self,name,password):
		try:
			conn = sqlite3.connect(settings.DATABASE)
			curs = conn.cursor()
			
			curs.execute("SELECT id, name FROM users WHERE name=?",(name,))
			if curs.fetchone():
				raise Exception("bad username")
			pw = hashPass(password)
			np = (name, pw)
			curs.execute("INSERT INTO users(name,password) VALUES(?,?)" , np)
			self.id = curs.lastrowid
			self.name = name
			self.password = pw
			conn.commit()
			
		except sqlite3.Error as e:
			print (e)
		except Exception as e:
			print (e)
		finally:
			if conn:
				conn.close()
	
	def getUser(self,name, password):
		try:
			conn = sqlite3.connect(settings.DATABASE)
			curs = conn.cursor()
		
			np = (name, hashPass(password))
			curs.execute("SELECT id, name, password FROM users WHERE name=? AND password=?" , np)
			tmpU = curs.fetchone()
			if tmpU:
				self.id = int(tmpU[0])
				self.name = tmpU[1]
				self.password = tmpU[2]
			else:
				raise Exception("bad username or password")
		except sqlite3.Error as e:
			print (e)
		finally:
			if conn:
				conn.close()
	
			
	
class Payments:
	paymetsList = None

	
	def newPayment(self,dataList, categoryId, userId):
		#dataList: list of dict. example [{'summ':122, 'comment':"adad",'date':"2013-10-10", 'mul':1},]
		try:
			conn = sqlite3.connect(settings.DATABASE)
			curs = conn.cursor()
			
			curs.execute("SELECT id FROM c2u WHERE fk_user=? AND fk_category=?", (userId, categoryId))
			fk_c2u = curs.fetchone()
			if fk_c2u:
				fk_c2u = int(fk_c2u[0])
			else:
				raise Exception("Category not found")
			
			pl = []
			for data in dataList:
				#data consist of {summ:, comment:, date:, mul:}
				dataTuple = tuple([data['summ'], data['comment'], data['date'], data['mul'], fk_c2u])
				curs.execute("INSERT INTO payments(summ, comment, date, mul, fk_c2u) VALUES(?,?,?,?,?)",dataTuple)
				conn.commit()
				pl.append({'id':curs.lastrowid,'summ':dataTuple[0],'comment':dataTuple[1],'date':dataTuple[2],'mul':dataTuple[3],'fk_c2u':dataTuple[4]})
			self.paymetsList = pl	
		except sqlite3.Error as e:
			print(e)
		finally:
			if conn:
				conn.close()
	
	
	def getPaymentsAll(self,userId):		
		try:
			conn = sqlite3.connect(settings.DATABASE)
			curs = conn.cursor()
			curs.execute("SELECT p.id, p.summ, comment, date, mul,fk_c2u,c.title from payments p, categories c where fk_c2u in (select id from c2u where fk_user = ? and c.id = fk_category)",(userId,))
			dataList = curs.fetchall()
			self.paymetsList = fillPaymentsList(dataList)
		except sqlite3.Error as e:
			print(e)
		finally:
			if conn:
				conn.close()

	def getPayments(self,userId,dateRange):		
		try:
			conn = sqlite3.connect(settings.DATABASE)
			curs = conn.cursor()
			curs.execute("SELECT p.id, p.summ, comment, date, mul,fk_c2u,c.title from payments p, categories c where (fk_c2u in (select id from c2u where fk_user = ? and c.id = fk_category)) and (date between  ? and ? ) and (1=1) order by date desc",(userId,dateRange,datetime.date.today()))
			dataList = curs.fetchall()
			self.paymetsList = fillPaymentsList(dataList)
		except sqlite3.Error as e:
			print(e)
		finally:
			if conn:
				conn.close()


class Categories:
	categoriesList = None
	
	def newCategory(self, title,userId):
		if userId and title:
			try:
				conn = sqlite3.connect(settings.DATABASE) 
				curs = conn.cursor()
				t = title.decode('utf-8').upper()
				curs.execute("SELECT id, title FROM categories WHERE title=? ",(t,))
				cat = curs.fetchone()
				if cat:
					self.id = int(cat[0])
					self.title = cat[1]
					curs.execute("SELECT id FROM c2u WHERE fk_category=? and fk_user=?",(self.id,userId))
					if curs.fetchone():
						raise Exception("This group already exists")
					else:
						curs.execute("INSERT INTO c2u(fk_user,fk_category) VALUES(?,?)",(userId,self.id))
						conn.commit()
					
				else:
					curs.execute("INSERT INTO categories(title) VALUES(?)",(title.decode('utf-8').upper(),))
					conn.commit()
					self.id = curs.lastrowid
					self.title = title.decode('utf-8').capitalize()
					curs.execute("INSERT INTO c2u(fk_user,fk_category) VALUES(?,?)",(userId,self.id))
					conn.commit()
			except sqlite3.Error as e:
				print(e)
			finally:
				if conn:
					conn.close()
		else:
			print ("Bad title or not user")
		
	def getCategoriesAll(self, userId):
		try:
			conn = sqlite3.connect(settings.DATABASE)
			curs = conn.cursor()
			
			curs.execute("SELECT id, title FROM categories WHERE id IN (SELECT fk_category FROM c2u WHERE fk_user=?)",(userId,))
			cl = []
			dataList = curs.fetchall()
			for data in dataList:
				cl.append({'id':data[0],'title':data[1]})
			self.categoriesList = cl
		except sqlite3.Error as e:
			print(e)
		finally:
			if conn:
				conn.close()

	def getCategory(self, title, userId):
		try:
			conn = sqlite3.connect(settings.DATABASE)
			curs = conn.cursor()
			
			curs.execute("SELECT id, title FROM categories WHERE title=? AND id IN (SELECT fk_category FROM c2u WHERE fk_user=?)",(title.decode('utf-8').upper(), userId))
			dataList = curs.fetchone()
			if not dataList:
				raise Exception("category not found")
			
			self.categoriesList = [{'id':dataList[0],'title':dataList[1]}]
			
		except sqlite3.Error as e:
			print(e)
		finally:
			if conn:
				conn.close()
		
if __name__ == "__main__":
	u = Users()
	u.getUser("alex", "123")
	
	p = Payments()
	#p.newPayment(dataList=[{'summ':107,'comment':"fddf",'date':datetime.date.today(),'mul':2}],categoryId=2,userId=u.id)
	p.getPaymentsWithCategory(u.id)
	#ls = [l for l in p.paymetsList if l['id']==1]
	for row in p.paymetsList: 
		print (len(row))
	
	#p.getPaymentsList(u.id)
	#c = Categories()
	#c.getCategory("bbbb",u.id)
	#print c.categoriesList
	#c.newCategory(title="3",userId=u.id)
	#c.getCategotiesAll(u.id)
	#for row in c.categoryList:
	#	print row
