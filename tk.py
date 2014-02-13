# -*- coding: utf-8 -*-
from ORM import Users, Payments, Categories
from tkinter import  simpledialog, messagebox, Label, Frame, Toplevel, Entry, LEFT, RIGHT, BOTH, TOP, BOTTOM, Button, \
    GROOVE, YES, Menu, Scrollbar, VERTICAL, SUNKEN, W, X, Y, Tk

from ttk import Combobox, Treeview
#import tkMageBox
#import tkSimpleDialog
import datetime

user = Users()
payments = Payments()
categories = Categories()

class authWindow(simpledialog.Dialog):
	def body(self,parent):
		self.title("SignIn")
		self.geometry("250x115+400+300")


		Label(parent, text='Enter your name and login').grid(row=0, columnspan=2)
		Label(parent, text='Username: ').grid(row=1)
		self.username = Entry(parent)
		self.username.grid(row=1,column=1)		

		Label(parent, text='Password: ').grid(row=2)
		self.pwd = Entry(parent,show="*")
		self.pwd.grid(row=2,column=1)		
	
	def apply(self):
		global user
		try:
			user.getUser(name=self.username.get(),password=self.pwd.get())
			self.parent.status.set("%s",user.name)
		except Exception as e:
			messagebox.showerror(title='Error', message=e)

class Statistics(Toplevel):	
	def __init__(self,parent):
		Toplevel.__init__(self,parent)
		self.title("Статистика")	
		self.transient(parent)
		self.parent = parent

	#fields for parameters of search-----------------------------------------------------------------------------------
		paramframe = Frame(self,relief=GROOVE,width=200,bd=1)
		paramframe.pack(side=LEFT,fill=BOTH)

		Label(paramframe, text="Что вывести",width=20,height=2).grid(row=0,column=0,columnspan=2)
		what = Combobox(paramframe,state='readonly',values = [u"Расходы",u"Доходы",u"Всё"],height=5)
		what.set(u"Расходы")
		what.grid(row=1,column=0,columnspan=2)
		self.what = what		
		
		Label(paramframe, text="За период",height=2).grid(row=2,column=0,columnspan=2)
		when = Combobox(paramframe,state='readonly',values=[u"Сегодня",u"3 дня",u"5 дней",u"Неделю",u"3 недели",u"Месяц",u"Всё время"],height=5)
		when.set(u"Сегодня")
		when.grid(row=3,column=0,columnspan=2)
		self.when = when
		
		Label(paramframe,text="Упорядочить по",height=2).grid(row=4,column=0,columnspan=2)
		orderby = Combobox(paramframe,state='readonly',values=[u"Дата",u"Cумма",u"Категория"],height=3)
		orderby.set(u"Дата")
		orderby.grid(row=5,column=0,columnspan=2)
		
		self.orderby = orderby		

		Button(paramframe,text="Вывести",command=(lambda: self.getStatistics())).grid(row=6,column=0,columnspan=2)		

		Label(paramframe,text="Итого: ",height=20).grid(row=7,column=0)
		self.summarylbl = Label(paramframe,text='0.0',height=20)
		self.summarylbl.grid(row=7,column=1)


	#end ------------------------------------------------------------------------------------------------------------------
		
	#table -------------------------------------------------------------------------------------------------------------
		
		self.viewframe = Frame(self,relief=GROOVE,width=200,bd=1)
		self.viewframe.pack(side=RIGHT,fill=BOTH,expand=YES)

	#end ------------------------------------------------------------------------------------------------------------------

		self.geometry("%dx%d+%d+%d" % (1000,500,225,125))
		self.wait_window(self)
	
	def getStatistics(self):
		when = self.when.current()
		dateRange = ''
		
		if when == 0:
		#today
			dateRange = datetime.date.today()
		elif when == 1:
		#3 days
			dateRange = datetime.date.today() - datetime.timedelta(days=3)
		elif when == 2:
		#5 days
			dateRange = datetime.date.today() - datetime.timedelta(days=5)
		elif when == 3:
		#1 week
			dateRange = datetime.date.today() - datetime.timedelta(weeks=1)
		elif when == 4:
		#3 weeks
			dateRange = datetime.date.today() - datetime.timedelta(weeks=3)
		elif when == 5:
		#1 month
			dateRange = datetime.date.today() - datetime.timedelta(weeks=4)
		elif when == 6:
		#all 
			dateRange = '2012-01-01'
		
		orderby = self.orderby.current()
		if orderby == 0:
		#date
			orderby = 4
		elif orderby == 1:
		#summ
			orderby = 2
		elif orderby == 2:
		#c.title
			orderby = 6
			
		global payments
		payments.getPayments(1,str(dateRange))
		
		if hasattr(self, 'tree'):
			self.tree.destroy()
			
		self.tree = Treeview(self.viewframe,selectmode="extended",columns=('summ', 'comment', 'date','mul','category_title'))
		self.tree.heading('#0',text='№')
		self.tree.column('#0',width=15,anchor='center')
		
		
		self.tree.column('summ', width=60, anchor='center')
		self.tree.column('comment', anchor='center')
		self.tree.column('date', width=60, anchor='center')
		self.tree.column('mul', width=7, anchor='center')
		self.tree.column('category_title',  anchor='center')
		
		self.tree.heading('summ', text='Сумма')
		self.tree.heading('comment', text='Комметарий')
		self.tree.heading('date', text='Дата')
		self.tree.heading('mul', text='Количество')
		self.tree.heading('category_title', text='Категория')
		
		i=1
		summary = 0.0
		for row in payments.paymetsList:
			self.tree.insert('', i,str(i), text=str(i))
			self.tree.set(str(i),'summ',row['summ'])
			self.tree.set(str(i),'comment',row['comment'])
			self.tree.set(str(i),'date',row['date'])
			self.tree.set(str(i),'mul',row['mul'])
			self.tree.set(str(i),'category_title',row['category_title'])
			i+=1
			summary+=row['summ']*row['mul']
		
		self.summarylbl.config(text=str(summary))
		self.tree.pack(side=TOP, fill=BOTH, expand=YES)
		
		s = Scrollbar(self.tree, orient=VERTICAL, command=self.tree.yview)
		self.tree.configure(yscrollcommand=s.set)
		s.pack(side=RIGHT,fill=Y)
		
		
class StatusBar(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.label = Label(self, bd=1, relief=SUNKEN, anchor=W)
        self.label.pack(fill=X)

    def set(self, format, *args):
        self.label.config(text=format % args)
        self.label.update_idletasks()

    def clear(self):
        self.label.config(text="")
        self.label.update_idletasks()

		


class LeftMenu(Frame):
	def __init__(self,parent):
		Frame.__init__(self,parent,relief=GROOVE,height=10,width=125,bd=1)
		
		self.fbtn = Button(self,text="ss")
		self.fbtn.pack(side=TOP,fill=X)
		
		self.fbtn1 = Button(self,text="ss2")
		self.fbtn1.pack(side=TOP,fill=X)
		#self.label = Label(self,bd=1,relief=GROOVE, anchor=W)
		#self.label.pack(fill=BOTH)
		
		self.pack_propagate(0)

class MyGUI(Frame):

	def __init__(self, parent=None):
		Frame.__init__(self,parent)
		self.parent = parent
		self.parent.title("Accounting")
		
		self.status = StatusBar(parent)
		self.status.set("%s","...")
		self.status.pack(side=BOTTOM, fill=BOTH)
		
		self.leftmenu = LeftMenu(parent)
		self.leftmenu.pack(side=LEFT, fill=BOTH)
			
		self.paymentframe = Frame(self,relief=GROOVE, bd=1)
		Label(self.paymentframe,text="Упорядочить по",height=2).grid(row=0,column=0,columnspan=2)
		self.paymentframe.pack(side=TOP,fill=BOTH,expand=YES)

		
		self.menubar = Menu(self)
		menu = Menu(self.menubar, tearoff=0)
		self.menubar.add_cascade(label="File", menu=menu)
		menu.add_command(label="LogIn", command=(lambda: authWindow(self)))
		menu.add_separator()
		menu.add_command(label="MessBox",command=(lambda: self.addPayment()))
		menu.add_separator()
		menu.add_command(label="Close", command=self.quit)

		menu = Menu(self.menubar, tearoff=0)
		self.menubar.add_cascade(label="Other", menu=menu)
		menu.add_command(label="Статистика", command=(lambda: Statistics(self)))
		menu.add_command(label="Copy")
		menu.add_command(label="Paste")
		
		try:
			self.master.config(menu=self.menubar)
		except AttributeError:
		    # master is a toplevel window (Python 1.4/Tkinter 1.63)
		    self.master.tk.call(master, "config", "-menu", self.menubar)		
		
		
		self.pack()
	
	def addPayment(self):
		pass
		
	def reply(self,text):
		messagebox.showinfo(title='popup', message=user.name)

if __name__=='__main__':
	root = Tk()
	root.geometry("800x400+225+250")
	window = MyGUI(root)
	root.mainloop()

