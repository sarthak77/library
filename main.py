from flask import Flask, render_template, request, redirect, flash,url_for
from model import *
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer
import datetime
import random
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML


app = Flask(__name__)
app.secret_key = 'MKhJHJH798798kjhkjhkjGHh'
app.config.from_pyfile('config.cfg')

mail = Mail(app)

s = URLSafeTimedSerializer('MKhJHJH798798kjhkjhkjGHh')






@app.route("/",methods=["GET"])
def index():
	if 'username' in session:
		return render_template("home.html",logged_in=True,username=session['username'],access=access)
	else:
		return render_template("home.html",logged_in=False,username=None,access=access)	








@app.route('/login',methods=['POST','GET'])
def login():
	print "aaaaaa"
	print access
	print "aaaaaa"

	if request.method == 'GET':
		if 'username' in session:
			return render_template("result.html",message="Already logged in!!!",logged_in=True,username=session['username'],access=access)
			#return render_template("login.html",logged_in=True,username=session['username'])
		else:

			return render_template("login.html",logged_in=False,username=None,access=access)	
	
	if request.method == 'POST':
		next = request.values.get('next')
		if(authenticate(request)==False):
			return render_template("result.html",message="Login failed",logged_in=False,username=None,access=access)
			#flash("Incorrect Credentials.", "danger")
			#return render_template("login.html")
		if(authenticate(request)==True):
			print "hello"
			if not next:
				global access
				access = 1
				return render_template("result.html",message=session['username']+" is logged in successfully",logged_in=True,username=session['username'],access=access)
			else:
				return redirect(next)










@app.route('/loginstudent',methods = ['POST','GET'])
def loginstudent():
	print "aaaaaa"
	print access
	print "aaaaaa"
	if request.method == 'GET':
		if 'username' in session:
			return render_template("result.html",message="Already logged in!!!",logged_in=True,username=session['username'],access=access)
		else:
			
			return render_template("loginst.html",logged_in=False,username=None,access=access)

	if request.method == 'POST':
		if(authenticatest(request)==False):
			return render_template("result.html",message="Login Failed",logged_in=False,username=None,access=access)
		if(authenticatest(request)==True):
			global access
			access = 2
			return render_template("result.html",message=session['username']+" is logged in successfully",logged_in=True,username=session['username'],access=access)	









@app.route('/logout',methods=['GET'])
#@login_required
def logout():
	if 'username' in session:
		name = session.pop('username')
		global access
		access = 0
		return render_template("result.html",message=name+" has logged out",access=access)
	else:
		return render_template("result.html",message="Not logged in",access=access)
	









@app.route("/signup",methods=["GET","POST"])
def signup():
	if 'username' in session:
		return render_template("signup.html",logged_in=True,username=session['username'],access=access)
	else:
		return render_template("signup.html",logged_in=False,username=None,access=access)
	#return render_template("signup.html")









@app.route("/signedup",methods=["POST"])
def signedup():
	#if 'username' in session:
	#	return render_template("result.html",message=session['username']+" has to log out first :-(",logged_in=True,username=session['username'],access=access)
	#else:	
		username = request.form['username']
		password = request.form['password']
		phone = request.form.get('phone')
		email = request.form.get('email')
		selected = request.form.get('abcd')
		print selected
		if str(selected) == "email":
			token = s.dumps(email, salt='email-confirm')


			msg = Message('Confirm Email',sender='batragaurav@gmail.com',recipients=[email])

			link = url_for('confirm_email',token=token,_external=True)

			msg.body = "Your link is {}. you can also login with otp".format(link)

			mail.send(msg)
			session['field1']=username
			session['field2']=phone
			session['field3']=password
			session['field4']=email		
	
			return render_template("result.html",logged_in=True,username=session['username'],message="send for verification",access=access)
		elif str(selected) == "otp":
			print "hello"
			token = s.dumps(email, salt='email-confirm')
			msg = Message('Confirm OTP', sender='batragaurav2616@gmail.com',recipients=[email])
			link =url_for('confirm_otp',token=token,_external=True)
			otp = random.randint(1000000,9999999)
			msg.body = "your otp is {}".format(otp)

			mail.send(msg)
			session['field1']=username
			session['field2']=phone
			session['field3']=password
			session['field4']=email
			session['field5']=otp

			return render_template("homepage.html",access=access,logged_in=True,username=session['username'])
		else:
			print "ggkk"	









@app.route('/confirm_email/<token>')
def confirm_email(token):
	try:
		email = s.loads(token, salt='email-confirm',max_age=300)
		insert_admin(session['field1'],session['field2'],session['field3'],session['field4'])
		session.pop('field1')
		session.pop('field2')
		session.pop('field3')
		session.pop('field4')
		return render_template("result.html",message="successfully verified",logged_in=True,username=session['username'],access=access)

	except Exception as e:
		return render_template("result.html",message=e,logged_in=True,username=session['username'],access=access)	
#	return render_template("result.html",message="token works")









@app.route('/confirm_otp',methods=['POST','GET'])
def confirm_otp():
	try:
		if request.method == "POST":
			print request.form
			value = request.form.get('otp')
			print value
			print session['field5']
		#email = s.loads(token, salt='email-confirm',max_age=300)
			if(str(session['field5'])==str(value)):

				insert_admin(session['field1'],session['field2'],session['field3'],session['field4'])
				session.pop('field1')
				session.pop('field2')
				session.pop('field3')
				session.pop('field4')
				session.pop('field5')
				return render_template("result.html",message="verified",logged_in=True,username=session['username'],access=access)

			elif(str(session['field5']) != str(value)):
				return render_template("homepage.html",access=access,logged_in=True,username=session['username'])

				session.pop('field1')
				session.pop('field2')
				session.pop('field3')
				session.pop('field4')

		else:
			return render_template("result.html",logged_in=True,username=session['username'],access=access)		

	except Exception as e:
		return render_template("result.html",message=e,access=access)

#def verifyotp(otp):
#	if otp == 		








@app.route('/issuesresolution',methods=['GET'])
def resolution():
	try:
		if request.method == "GET":
			
			data = queryissues()
			print data
			fees=calcLateFees(data[0][4].encode('ascii','ignore'),datetime.datetime.today().strftime("%d-%m-%Y"))
			print fees
			print datetime.datetime.today().strftime("%d-%m-%Y")
			studentdetails = queryst(data)
			print studentdetails
			bookdetails = querybk(data)
			print bookdetails

			email = []
			for i in range(0,len(data)):
				email.append(queryemail(data[i][2]))
			print email[0][0][0].encode('ascii','ignore')
			print len(email)
			a=len(bookdetails)
			a=[bookdetails,studentdetails,a]
			flag=1

			
			#return render_template("showissues.html",logged_in=True,username=session['username'],access=access,a=a,flag=flag)	
			for i in range(0,len(email)):
				print "hello"
				env = Environment(loader=FileSystemLoader('.'))
				template = env.get_template("./templates/issueresolution.html")
				template_vars = {
				"transactionid": data[i][0],
				"bookid" : data[i][1],
				"studentid" : data[i][2],
				"studentname" : studentdetails[i][2],
				"adminid" : data[i][3],
				"dateofissue" : data[i][4],
				"latefees" : calcLateFees(data[i][4].encode('ascii','ignore'),datetime.datetime.today().strftime("%d-%m-%Y")),
				"bookname" : bookdetails[i][0],
				"bookauthor" : bookdetails[i][2]
				}
				print template_vars
				html_out = template.render(template_vars)
				HTML(string=html_out).write_pdf("issuesresolution.pdf")



			

				#token=s.dumps(list(emails[0][0])[0],salt='email-confirm')
				msg= Message('Pending dues',sender='batragaurav2616@gmail.com',recipients=[email[i][0][0].encode('ascii','ignore')])
				msg.body = "The following books are Overdue.Please return/renew them as soon as possible to avoid increasing fines"	
				with app.open_resource("issuesresolution.pdf") as file:
					msg.attach("issuesresolution.pdf","issuesresolution/pdf",file.read())
				mail.send(msg)

			return render_template("mail.html",logged_in=True,username=session['username'],access=access,studentdetails=studentdetails,bookdetails=bookdetails)	


			#msg = M
	except Exception as e:
			return render_template("showissues.html",logged_in=True,username=session['username'],access=access,a=a,flag=flag)	








@app.route('/showall', methods=["GET"])
def showall():
	rows = getAll()
	#return render_template('showall.html',rows=rows,message="LIST OF BOOKS")
	if 'username' in session:
		return render_template("showall.html",logged_in=True,username=session['username'],rows=rows,message="LIST OF BOOKS",access=access)
	else:
		return render_template("showall.html",logged_in=False,username=None,rows=rows,message="LIST OF BOOKS",access=access)









@app.route('/contact')
def contact():
	#return render_template('contact.html')
	if 'username' in session:
		return render_template("contact.html",logged_in=True,username=session['username'],access=access)
	else:
		return render_template("contact.html",logged_in=False,username=None,access=access)








@app.route('/addbooks')
def addbooks():
	if 'username' in session and access == 1:
		return render_template("addbooks.html",logged_in=True,username=session['username'],access=access)
	elif 'username' in session and access == 2:
		return render_template("result.html",message="Only ADMINS can add books",logged_in=True,username=session['username'],access=access)
	else:
		return render_template("result.html",message="Only ADMINS can add books",logged_in=False,username=None,access=access)
		#return render_template("addbooks.html",logged_in=False,username=None)
	#return render_template('addbooks.html')








@app.route('/added',methods=["POST"])
def added():

	name = request.form['name']
	author = request.form['author']
	category = request.form.get('category')

	#if not session.get("logged_in"):
	insert_books(name,author,category)
	if 'username' in session and access == 1:
		return render_template("added.html",logged_in=True,username=session['username'],access=access)
	elif 'username' in session and access == 2:
		return render_template("added.html",logged_in=True,username=session['username'],access=access)
	else:
		return render_template("added.html",logged_in=False,username=None,access=access)
	#return render_template("added.html",name=name)









@app.route('/searchbook', methods=["POST"])
def searchBook():
	if request.method == "POST":
		book = {
		"name": request.form.get('name'),
		"author": request.form.get('author'),
		"category": request.form.get('category')
		}
		books = querybook(book)
		x=len(books)
		if 'username' in session:
			return render_template("searchbook.html",logged_in=True,username=session['username'],payload={"books":books},x=x,access=access)
		else:
			return render_template("searchbook.html",logged_in=False,username=None,payload={"books":books},x=x,access=access)	

		






@app.route("/apply", methods=["POST", "GET"])
def studentApply():
	if request.method == "GET":
		if 'username' in session:
			return render_template("apply.html",logged_in=True,username=session['username'],access=access)
		else:
			return render_template("apply.html",logged_in=False,username=None,access=access)	
	if request.method == "POST":
		pass

		student_form = {
		"name" : request.form.get('name'),
		"dob" : request.form.get('dob'),
		"address" : request.form.get('address'),
		"phone" : request.form.get('phone'),
		"password" : request.form.get('password'),
		"email" : request.form.get('email')
		}
		print student_form['password']
		student_status = insertstudent_reg(student_form)
		if student_status == False:
			flash("error in data entered","danger")
			return redirect("/apply")
		else:
			flash("Application sent for approval")
			#return redirect("/")
			if 'username' in session:
				return render_template("result.html",message="Application sent for approval",logged_in=True,username=session['username'],access=access)
			else:
				return render_template("result.html",message="Application sent for approval",logged_in=False,username=None,access=access)	







@app.route("/applications")
def studentapplications():
	if 'username' in session and access == 1:
		applications = querystudentreg()
		count=0
		for items in applications:
			print len(items)/6
			count+=len(items)/6
		print count
		return render_template("applications.html",payload={"applications":applications},logged_in=True,username=session['username'],count=count,access=access)							
	elif 'username' in session and access == 2:
		print "hello"
		return render_template("result.html",message="ADMIN ACCESS ALLOWED",logged_in=True,username=session['username'],access=access)
	else:
		return render_template("result.html",message="ADMIN ACCESS ALLOWED",logged_in=False,username=None,access=access)






@app.route("/reject/<int:regID>")
def rejectapplications(regID):
	if 'username' in session and access == 1:
		flag = deletestudentreg(regID)
		if flag is False:
			flash("error in rejecting. ","danger")
		return redirect("/applications")
	else:
		return render_template("result.html",message="ADMIN ACCESS ALLOWED",logged_in=False,username=None,access=access)			








@app.route("/accept/<int:regID>")
def acceptapplication(regID):
	if 'username' in session and access == 1:
		req_student = querysinglestudentreg(regID)
		if req_student is not None:
			student = {
			"cardnum" : generate(),
			"doj" : datetime.datetime.today().strftime("%d-%m-%Y"),
			"borrowlimit" : 2,
			"name" : req_student[1],
			"dob" : req_student[2],
			"address" : req_student[3],
			"phone" : req_student[4],
			"password" : req_student[5],
			"email" : req_student[6]
			}
			print student["password"]
			flag = insertStudent(student)
			deletestudentreg(regID)
			if flag is False:
				return render_template("result.html",message="IS UNABLE TO LOGIN",logged_in=False,username=None,access=access)
			return render_template("reg.html",message="SUCCESSFULLY REGISTERED",logged_in=False,username=None,access=access)
	else:
		return render_template("result.html",message="ADMIN ACCESS ALLOWED",logged_in=False,username=None,access=access)			








@app.route("/issuereturn", methods=["GET"])
def issuereturn():
	if 'username' in session:
		#print session['username'].id
		return render_template("issuereturn.html",logged_in=True,username=session['username'],access=access)
	else:
		return render_template("result.html",logged_in=False,username=None,message="NOT LOGGED IN",access=access)








@app.route("/issue",methods=["POST"])
def issuebook():
	if request.method == "POST":
		issueRequest = {
		"bookID" : request.form.get('bookID'),
		"studentid":request.form.get('studentid'),
		"adminid":request.form.get('adminid'),
		"issueDate" : datetime.datetime.today().strftime("%d-%m-%Y")
		}
		print issueRequest["adminid"]
		book_exists = existence_book(issueRequest.get("bookID"))
		print book_exists
		student_exists = existence_student(issueRequest.get("studentid"))
		print student_exists
		
		if book_exists is True:
			if student_exists is True:
				book_status = getbookstatus(issueRequest.get("bookID"))
				print book_status
				borrowlimit_check = existence_borrowlimit(issueRequest.get("studentid"))
				print borrowlimit_check
				if book_status is True:
					if borrowlimit_check is True:
						insert_status = insertIssue(issueRequest)
						print insert_status
						if insert_status is False:
							print "error is issueing. "
							return render_template("result.html",message="Error in issueing",logged_in=True,username=session['username'],access=access)
					else:
						print "Cannot borrow more"
						return render_template("result.html",message="Cannot borrow more",logged_in=True,username=session['username'],access=access)
				else:
					print "Book is issued"
					return render_template("result.html",message="Book is issued",logged_in=True,username=session['username'],access=access)
			else:

				print "student doesnot exists"
				return render_template("result.html",message="Student does not exist",logged_in=True,username=session['username'],access=access)
		else: 
			print "book does not exist"
			return render_template("result.html",message="Book does not exist",logged_in=True,username=session['username'],access=access)
		return render_template("result.html",message="Successfull",logged_in=True,username=session['username'],access=access)









@app.route("/return",methods=["POST"])
def returnBook():
	if 'username' in session:
		if request.method == "POST":
			return_book = {
			"bookid" : request.form.get("bookID"),
			#"returnedtoID" : request.form.get("adminid")
			}

			issue = queryissuebybook(return_book.get("bookid"))
			if issue is not None:
				return_book["transid"]=issue[0]
				return_book["studentid"]=issue[2]
				return_book["issuedbyid"]=issue[3]
				return_book["issueDate"]=issue[4]
				return_book["returnDate"]=datetime.datetime.today().strftime("%d-%m-%Y")
				return_book["lateFees"] = calcLateFees(return_book["issueDate"],return_book["returnDate"])
				print return_book["lateFees"]
				flag = insertissuehistory(return_book)
				if flag is False:
					return render_template("result.html",message="Error in returning",logged_in=True,username=session['username'],access=access)
				else:
					deleteissue(return_book["transid"])
					if return_book["lateFees"] > 0:
						return render_template("result.html",message="you have to pay rs {} as fine".format(return_book["lateFees"]),logged_in=True,username=session['username'],access=access)	
					else:
						return render_template("result.html",message="Book returned successfully",logged_in=True,username=session['username'],access=access)	
			else:
				return render_template("result.html",message="Book is not issued yet",logged_in=True,username=session['username'],access=access)			
		return redirect("/issuereturn")

	else:
		return render_template("result.html",message="log in first",logged_in=True,username=session['username'],access=access)					










@app.route("/searchstudent", methods=["POST","GET"])
def searchstudent():
	if 'username' in session and access == 1:
		if request.method == "GET":
			return render_template("searchstudent.html", payload={"type":"student"},logged_in=True,username=session['username'],access=access)
		if request.method == "POST":
			student = {
			"id" : request.form.get('id'),
			"name" : request.form.get('name'),
			"cardnum": request.form.get('cardnum')
			}
			for items in student:
				print student[items]
			students = querystudent(student)
			return render_template("searchstudent.html", payload={"students": students},access=access,logged_in=True,username=session['username'])
	elif 'username' in session and access == 2:
		return render_template("result.html", message="ADMIN ACCESS ALLOWED",logged_in=True,username=session['username'],access=access)
	else:
		return render_template("result.html", message="ADMIN ACCESS ALLOWED",logged_in=False,username=None,access=access)		









@app.route('/allbooks')
def allbooks():
	rows = getAll()
	if 'username' in session:
		return render_template("allbooks.html",logged_in=True,username=session['username'],rows=rows,message="LIST OF BOOKS",access=access)
	else:
		return render_template("allbooks.html",logged_in=False,username=None,rows=rows,message="LIST OF BOOKS",access=access)




@app.route('/allbooks1')
def allbooks1():
	rows = getAll()
	if 'username' in session:
		return render_template("allbooks1.html",logged_in=True,username=session['username'],rows=rows,message="LIST OF BOOKS",access=access)
	else:
		return render_template("allbooks1.html",logged_in=False,username=None,rows=rows,message="LIST OF BOOKS",access=access)




@app.route('/allbooks2')
def allbooks2():
	rows = getAll()
	if 'username' in session:
		return render_template("allbooks2.html",logged_in=True,username=session['username'],rows=rows,message="LIST OF BOOKS",access=access)
	else:
		return render_template("allbooks2.html",logged_in=False,username=None,rows=rows,message="LIST OF BOOKS",access=access)




@app.route('/allbooks3')
def allbooks3():
	rows = getAll()
	if 'username' in session:
		return render_template("allbooks3.html",logged_in=True,username=session['username'],rows=rows,message="LIST OF BOOKS",access=access)
	else:
		return render_template("allbooks3.html",logged_in=False,username=None,rows=rows,message="LIST OF BOOKS",access=access)




@app.route('/allbooks4')
def allbooks4():
	rows = getAll()
	if 'username' in session:
		return render_template("allbooks4.html",logged_in=True,username=session['username'],rows=rows,message="LIST OF BOOKS",access=access)
	else:
		return render_template("allbooks4.html",logged_in=False,username=None,rows=rows,message="LIST OF BOOKS",access=access)




@app.route('/allbooks5')
def allbooks5():
	rows = getAll()
	if 'username' in session:
		return render_template("allbooks5.html",logged_in=True,username=session['username'],rows=rows,message="LIST OF BOOKS",access=access)
	else:
		return render_template("allbooks5.html",logged_in=False,username=None,rows=rows,message="LIST OF BOOKS",access=access)




@app.route('/allbooks6')
def allbooks6():
	rows = getAll()
	if 'username' in session:
		return render_template("allbooks6.html",logged_in=True,username=session['username'],rows=rows,message="LIST OF BOOKS",access=access)
	else:
		return render_template("allbooks6.html",logged_in=False,username=None,rows=rows,message="LIST OF BOOKS",access=access)




@app.route('/allbooks7')
def allbooks7():
	rows = getAll()
	if 'username' in session:
		return render_template("allbooks7.html",logged_in=True,username=session['username'],rows=rows,message="LIST OF BOOKS",access=access)
	else:
		return render_template("allbooks7.html",logged_in=False,username=None,rows=rows,message="LIST OF BOOKS",access=access)




@app.route('/allbooks8')
def allbooks8():
	rows = getAll()
	if 'username' in session:
		return render_template("allbooks8.html",logged_in=True,username=session['username'],rows=rows,message="LIST OF BOOKS",access=access)
	else:
		return render_template("allbooks8.html",logged_in=False,username=None,rows=rows,message="LIST OF BOOKS",access=access)




@app.route('/allbooks9')
def allbooks9():
	rows = getAll()
	if 'username' in session:
		return render_template("allbooks9.html",logged_in=True,username=session['username'],rows=rows,message="LIST OF BOOKS",access=access)
	else:
		return render_template("allbooks9.html",logged_in=False,username=None,rows=rows,message="LIST OF BOOKS",access=access)




@app.route('/allbooks10')
def allbooks10():
	rows = getAll()
	if 'username' in session:
		return render_template("allbooks10.html",logged_in=True,username=session['username'],rows=rows,message="LIST OF BOOKS",access=access)
	else:
		return render_template("allbooks10.html",logged_in=False,username=None,rows=rows,message="LIST OF BOOKS",access=access)








@app.route('/adminrights')
def adminrights():
	#return render_template('contact.html')
	print access
	if 'username' in session and access == 1:
		return render_template("adminrights.html",logged_in=True,username=session['username'],access=access)
	elif 'username' in session and access == 2:
		return render_template("result.html",message="log in first",logged_in=True,username=session['username'],access=access)
	else:
		return render_template("result.html",message="log in first",logged_in=False,username=None,access=access)	









@app.route('/studentinfo')
def studentinfo():
	if 'username' in session and access == 2:
		print session['username']
		info=getinfo(session['username'])
		books=findbooks(session['username'])
		x=0
		if books != None:
			x=1
			return render_template("studentinfo.html",logged_in=True,books=books,info=info,username=session['username'],access=access,x=x)
		else:
			return render_template("studentinfo.html",logged_in=True,books=[],info=info,username=session['username'],access=access,x=x)	
	elif 'username' in session and access == 1:
		return render_template("result.html",message='LOGIN as student FIRST',logged_in=True,username=session['username'],access=access)
	else:
		return render_template("result.html",message='LOGIN FIRST',logged_in=False,username=None,access=access)










@app.route('/viewadmins')
def viewadmins():
	if 'username' in session and access == 1:
		x=viewadmins1()
		return render_template("viewadmins.html",logged_in=True,username=session['username'],x=x,access=access)
	
	elif 'username' in session and access == 2:
		return render_template("result.html",message="log in first",logged_in=True,username=session['username'],access=access)
	else:
		return render_template("result.html",message="log in first",logged_in=False,username=None,access=access)	








@app.route('/showissues')
def showissue():
	data = showissued()
	print data
	bookdetails = querybk(data)
	print bookdetails
	studentdetails = queryst(data)
	print studentdetails
	a=len(bookdetails)
	a=[bookdetails,studentdetails,a]
	flag=0
	return render_template("showissues.html",a=a,flag=flag,logged_in=True,username=session['username'],access=access)	





access = 0
app.run(debug=True)	

