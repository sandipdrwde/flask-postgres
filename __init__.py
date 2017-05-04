from flask import Flask, request, flash, url_for, redirect, render_template, make_response
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:sandip08@localhost:5432/test'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "random string"

db = SQLAlchemy(app)

class students(db.Model):
	id = db.Column('student_id', db.Integer, primary_key = True)
	name = db.Column(db.String(100))
	city = db.Column(db.String(50))
	addr = db.Column(db.String(200)) 
	pin = db.Column(db.String(10))

	def __init__(self, name, city, addr,pin):
		self.name = name
		self.city = city
		self.addr = addr
		self.pin = pin

@app.route('/')
def show_all():
	return render_template('show_all.html', students = students.query.all())

@app.route('/new', methods = ['GET', 'POST'])
def new():

	if request.method == 'POST':

		if not request.form['name'] or not request.form['city'] or not request.form['addr']:
			flash('Please enter all the fields', 'error')
		else:
			student = students(request.form['name'],
								request.form['city'],
								request.form['addr'],
								request.form['pin'])

			db.session.add(student)
			db.session.commit()
			flash('Record was successfully added')
			return redirect(url_for('show_all'))
	return render_template('new.html')



from flask import Flask, render_template
#from forms import ContactForm

@app.route('/contact', methods=['GET', 'POST'])
def contact():
	form = ContactForm()
	#return render_template('contact.html', form=form)

	if request.method == 'POST':
		if form.validate() == False:
			flash('All fields are required.')
			return render_template('contact.html', form=form)

		else:
			return render_template('success.html')

	elif request.method == 'GET':
		return render_template('contact.html', form=form)



from flask_wtf import Form
from wtforms import TextField, RadioField, SelectField, IntegerField,TextAreaField,SubmitField
from wtforms import validators, ValidationError

class ContactForm(Form):
	#name = TextField("Name Of Student")
	#name = TextField("Name Of Student",[validators.Required("Please enter your name.")])

	name = TextField("Name Of Student",[validators.Required("Please enter your name.")])
	Gender = RadioField('Gender', choices=[('M','Male'),('F','Female')])
	Address = TextAreaField("Address")
	email = TextField("Email",[validators.Required("Please enter your email address."), validators.Email("Please enter your email address.")])
	Age = IntegerField("age")
	language = SelectField('Languages', choices=[('cpp', 'C++'), ('py', 'Python')])
	submit = SubmitField("Send")



@app.route('/index')
def index():
	return render_template('index.html')


@app.route('/setcookie', methods=['POST', 'GET'])
def setcookie():
	if request.method=='POST':
		user= request.form['nm']
		resp = make_response(render_template('readcookie.html'))
		resp.set_cookie('userID', user)
		return resp


@app.route('/getcookie')
def getcookie():
	name = request.cookies.get('userID')
	return '<h1>welcome '+name+'</h1>'



@app.route('/student')
def student():
	return render_template('student.html')

@app.route('/result',methods=['POST', 'GET'])
def result():
	if request.method=='POST':
		result=request.form

		print result
		return render_template("result.html",result=result)

if __name__ == '__main__':
	db.create_all()
	app.run(debug = True)



