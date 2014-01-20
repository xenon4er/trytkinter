#!/usr/bin/python
# -*- coding: utf-8 -*-

import ORM



def login():
	print "login"




def run():
	exit = 0
	comands = ">>exit - exit \n>>login" 
				
	while not exit:
		print comands
		cmd = raw_input('input cmd: ')
		
		if cmd == 'exit':
			exit = 1
		elif cmd == 'login':
			login()

if __name__=="__main__":
	run()
