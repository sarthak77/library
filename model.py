import sqlite3 as sql
from flask import session
from passlib.hash import sha256_crypt
import random
import datetime

def insert_admin(username,phone,password,email):
	with sql.connect("database.db") as con:
		password = sha256_crypt.encrypt(password)
		cur = con.cursor()
		cur.execute("INSERT INTO admins (username,phone,password,email) VALUES (?,?,?,?)", (username,phone,password,email) )
		con.commit()

def insert_books(name,author,category):
	with sql.connect("database.db") as con:
		cur = con.cursor()
		cur.execute("INSERT INTO books (name,author,category) VALUES (?,?,?)", (name,author,category) )
		con.commit()

def getAll():
	try:
		with sql.connect("database.db") as con:
			con.row_factory = sql.Row
			cur = con.cursor()
			cur.execute("select * from books")
			rows = cur.fetchall()
			for row in rows:
				print "row=" + row["name"]
			return (rows)
	except:
		print "NO ENTRY FOUND"
		return ([])

def authenticate(request):
	con = sql.connect("database.db")
	username = request.form['username']
	password = request.form['password']
	sqlQuery = "select password from admins where username = '%s'"%username
	cursor = con.cursor()
	cursor.execute(sqlQuery)
	row = cursor.fetchall()
	status = False
	if row:
		for i in range(0,len(row)):
			status = sha256_crypt.verify(password,row[i][0])
			if status == True:
				break
		if status:
			msg = username + "has logged in successfully"
			session['username'] = username
	else:
		msg = username + "login failed"

	return status

def authenticatest(request):
	con = sql.connect("database.db")
	username = request.form['username']
	password = request.form['password']
	sqlQuery = "select password from students where name = '%s'"%username
	print sqlQuery
	cur = con.cursor()
	cur.execute(sqlQuery)
	row = cur.fetchall()
	print len(row)
	status = False
	if row:
		for i in range(0,len(row)):
			status = sha256_crypt.verify(password,row[i][0])
			print status
			print i
			if status == True:
				print "hello"
				break
		print status		
		if status:
			msg = username + "had logged in successfully"
			session['username'] = username
	else:
		msg = username + "login failed"	

	return status		

def querybook(params):
	clause = []
	if params.get("name") is not None and params.get("name") is not '':
		clause.append("name LIKE '%{}%'".format(params.get("name")))
	if params.get("author") is not None and params.get("author") is not '':
		clause.append("author LIKE '%{}%'".format(params.get("author")))
	if params.get("category") is not None and params.get("category") is not '':
		clause.append("category LIKE '%{}%'".format(params.get("category")))	
	
	for items in clause:
		print items
	if clause:
		query = "SELECT * FROM books WHERE {}".format(" AND ".join(clause))
	else:
		query = "SELECT * FROM books"

	try:
		con = sql.connect("database.db")
		cursor = con.cursor()
		cursor.execute(query, params)
		book_list = cursor.fetchall()
		print len(book_list)
		return book_list
	except Exception as e:
		print e
		return None	

def unique(carnum):
	try:
		con = sql.connect("database.db")
		cursor = con.cursor()
		cursor.execute("SELECT count(*) from students where cardnum=?",(carnum, ))
		num = cursor.fetchone()
		#for items in num:
		print num[0]
		if num[0] == 0:
			return True
		else:
			return False	
	except Exception as e:
		print e
		return None

def insertStudent(form_apply):

	try:
		con =sql.connect("database.db")
		cursor = con.cursor()
		print form_apply["password"]
		form_apply["password"]=sha256_crypt.encrypt(form_apply["password"])
		cursor.execute("INSERT INTO students(cardnum,name,dob,doj,address,phone,borrowlimit,password,email) VALUES (:cardnum,:name,:dob,:doj,:address,:phone,:borrowlimit,:password,:email)",form_apply)
		con.commit()
		return True
	except Exception as e:
		print e
		return False


def duplicate(form_apply):
	try :
		con = sql.connect("database.db")
		cursor = con.cursor()
		clause=[]
		clause.append("name='{}'".format(form_apply.get("name")))
		clause.append("dob='{}'".format(form_apply.get("dob")))
		clause.append("address='{}'".format(form_apply.get("address")))
		clause.append("phone='{}'".format(form_apply.get("phone")))
		clause.append("borrowlimit='{}'".format(form_apply.get("borrowlimit")))
		query="SELECT * FROM students WHERE {}".format(" AND ".join(clause))

		print query
		cursor.execute(query,form_apply)
		list_s = cursor.fetchall()
		for items in list_s:
			return True
			print items
		return False	 
	except Exception as e:
		print e
		return False

def existence_book(bookid):
	try:
		con= sql.connect("database.db")
		cursor = con.cursor()
		cursor.execute("SELECT COUNT(*) FROM books WHERE id=?",(bookid,))
		flag = cursor.fetchone()
		return flag[0] == 1
	except Exception as e:
		print(e)
		return None

def existence_student(studentid):
	try:
		con = sql.connect("database.db")
		cursor = con.cursor()
		cursor.execute("SELECT COUNT(*) FROM students WHERE id=?",(studentid,))
		flag = cursor.fetchone()
		return flag[0] == 1
	except Exception as e:
		print(e)
		return None

def getbookstatus(bookid):
	try:
		con = sql.connect("database.db")
		cursor = con.cursor()
		cursor.execute("SELECT COUNT(*) FROM issue WHERE bookid=?",(bookid, ))
		flag = cursor.fetchone()
		return flag[0] == 0
	except Exception as e:
		print e
		return None	

def existence_borrowlimit(studentid):
	try:
		con = sql.connect("database.db")
		cursor = con.cursor()
		cursor.execute("SELECT COUNT(*) FROM issue WHERE studentid=?",(studentid, ))
		borrows = cursor.fetchone()[0]
		cursor.execute("SELECT borrowlimit FROM students WHERE id=?",(studentid, ))
		borrowlimit = cursor.fetchone()[0]
		return borrows < borrowlimit
	except Exception as e:
		print(e)
		return None	

def insertIssue(issue):
	try:
		con = sql.connect("database.db")
		cursor = con.cursor()
		cursor.execute("INSERT INTO issue(bookID,studentid,adminid,issueDate)VALUES(:bookID,:studentid,:adminid,:issueDate)",issue)
		con.commit()
		return True
	except Exception as e:
		print e
		return False		

def queryissues():
	try:
		con = sql.connect("database.db")
		cursor = con.cursor()
		cursor.execute("SELECT * FROM issue")
		row = cursor.fetchall()
		return row
	except Exception as e:
		print e	
def queryemail(studentid):
	try:
		con = sql.connect("database.db")
		cursor = con.cursor()
		cursor.execute("SELECT email FROM students where id="+str(studentid))
		row = cursor.fetchall()
		return row
	except Exception as e:
		print e

def querystudent(params):
	clause = []
	count =0
	if params.get("id") is not None and params.get("id") is not '':
		clause.append("id='{}'".format(params.get("id")))
		count = count+1
		if clause[0] == "id=''":
			clause.pop(0)
			count=count-1
	if params.get("name") is not None and params.get("name") is not '':
		clause.append("name LIKE '%{}%'".format(params.get("name")))
		count = count+1
	if params.get("cardnum") is not None and params.get("name") is not '':
		clause.append("cardnum='{}'".format(params.get("cardnum")))
		count = count+1
		if clause[count-1]=="cardnum=''":
			clause.pop(count-1)
			count = count-1

	
	if clause:
		query = "SELECT * FROM students WHERE {}".format(" AND ".join(clause))
	else:
		query = "SELECT * FROM students"				
	print query	
	try:
		con = sql.connect("database.db")
		cursor = con.cursor()
		cursor.execute(query,params)
		student_list = cursor.fetchall()
		#for items in student_list:
		print student_list
		xxx=len(student_list)
		return [student_list,xxx]
	except Exception as e:
		print e
		return None	

def queryissuebybook(bookid,student=False):
	try:
		if student:
			con = sql.connect("database.db")
			cursor = con.cursor()
			cursor.execute(''' 
				SELECT transid,bookid,studentid,adminid,issueDate,name
				FROM issue,students
				WHERE studentid = student.id AND bookid =?''',(bookid, ))
		else:
			con = sql.connect("database.db")
			cursor = con.cursor()
			cursor.execute("SELECT * FROM issue WHERE bookid=?",(bookid, ))
		issue = cursor.fetchone()
		return issue
	except Exception as e:
		print e
		return None

def insertissuehistory(issuehistory):
	try:
		for keys in issuehistory:
			print issuehistory[keys]
		con = sql.connect("database.db")
		cursor = con.cursor()
		cursor.execute('''
			INSERT INTO issue_history(transid,bookid,studentid,issuedbyid,issueDate,returnDate,lateFees)
			VALUES(:transid,:bookid,:studentid,:issuedbyid,:issueDate,:returnDate,:lateFees)
			''',issuehistory)
		con.commit()
		return True
	except Exception as e:
		print "hello"
		print e
		return None

def deleteissue(issueid):
	try:
		con = sql.connect("database.db")
		cursor=con.cursor()
		cursor.execute("DELETE FROM issue WHERE transid=?",(issueid, ))
		con.commit()
		return True
	except Exception as e:

		print e
		return None


def insertstudent_reg(student):
	try:
		con = sql.connect("database.db")
		cursor = con.cursor()
		cursor.execute("INSERT INTO student_reg(name, dob, address, phone,password,email) VALUES(:name, :dob, :address, :phone,:password,:email)",student)
		con.commit()
		return True
	except Exception as e:
		print e
		return False

def querystudentreg():
	try:
		con = sql.connect("database.db")
		cursor = con.cursor()
		cursor.execute("SELECT * FROM student_reg")
		regs = cursor.fetchall()
		for items in regs:
			print items
		return regs
	except Exception as e:
		print e			
		return None

def querysinglestudentreg(regID):
	try:
		con = sql.connect("database.db")
		cursor = con.cursor()
		cursor.execute("SELECT * FROM student_reg WHERE regID=:regID",(regID, ))
		reg = cursor.fetchone()
		return reg
	except Exception as e:
		print e			
		return None

def deletestudentreg(regID):
	try:
		con = sql.connect("database.db")
		cursor = con.cursor()
		cursor.execute("DELETE FROM student_reg WHERE regID=:regID",(regID, ))
		con.commit()
		return True
	except Exception as e:
		print e			
		return False
					
					
def generate():
	carNum = random.randint(1000,9999)
	if unique(carNum):
		return carNum
	else: 
		generate()	
	#return carNum

def calcLateFees(issueDate, returnDate):
	lateFees = 0
	date1 = datetime.datetime.strptime(issueDate, "%d-%m-%Y")
	date2 = datetime.datetime.strptime(returnDate, "%d-%m-%Y")
	print date1
	days_issued = (date2-date1).days
	print days_issued
	if days_issued > 7:
		lateFees = (days_issued-7)*LATE_FINE
	return lateFees


def getinfo(name):
	try:
		con = sql.connect("database.db")
		cursor = con.cursor()
		cursor.execute("SELECT * FROM students WHERE name=:name",(name, ))
		info = cursor.fetchone()
		return info
	except Exception as e:
		print e			
		return None

def findbooks(name):
	try:
		con = sql.connect("database.db")
		cursor = con.cursor()
		cursor.execute("SELECT id FROM students WHERE name=:name",(name,))
		x = cursor.fetchone()
		y =  x[0]
		cursor.execute("SELECT * FROM issue WHERE studentid=?",(y,))
		book = cursor.fetchall()
		print book
		print book[0]


		return book
	except Exception as e:
		print e			
		return None



def viewadmins1():
	try:
		con = sql.connect("database.db")
		cursor = con.cursor()
		cursor.execute("SELECT * FROM admins")
		x = cursor.fetchall()
		print x
		print len(x)
		y=len(x)
		return [x,y]
	except Exception as e:
		print e			
		return None
		
def queryst(data):
	try:
		con = sql.connect("database.db")
		row = []
		cursor = con.cursor()
		for i in range(0,len(data)):
			cursor.execute("SELECT * FROM students where id ="+str(data[i][2])+";")
			row.append(cursor.fetchone())
			

		return row
	except Exception as e:
		print e				
		
def querybk(data):
	try:
		con = sql.connect("database.db")
		row = []
		cursor = con.cursor()
		for i in range(0,len(data)):
			cursor.execute("SELECT * FROM books where id ="+str(data[i][1])+";")
			row.append(cursor.fetchone())

		return row
	except Exception as e:
		print e

def showissued():
	try:
		con=sql.connect("database.db")
		row = []
		cursor = con.cursor()
		cursor.execute("SELECT * from issue")
		row = cursor.fetchall()
		return row
	except Exception as e:
		print e
		

