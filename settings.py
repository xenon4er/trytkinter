import os

DATABASE = os.path.abspath(__file__).replace(os.path.basename(__file__),'') + "accountig.db"

if __name__=="__main__":
	print DATABASE
