from __future__ import print_function # In python 2.7
from flask import Flask, render_template, request, redirect, make_response, Response
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate
import json
import sys
import os
from sqlalchemy.orm.attributes import flag_modified


app = Flask(__name__)
db = SQLAlchemy(app)

migrate = Migrate(app, db)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

import models


adminpassword = os.environ.get('PASSWORD',"y34h y0u kn0w m3")


try:
	if models.Flat.query.count() == 0:
		adminguesses = {}
		for label in ["south","east","west","midwest"]:
			for rank in range(1,5):
				for game in range([8,4,2,1][rank-1]):
					adminguesses[label+" "+str(rank)+" "+str(game)]=""
		for rank in range(4,7):
			for game in range([4,2,1][rank-4]):
				adminguesses["F "+str(rank)+" "+str(game)]=""
		e = models.Flat()
		f = open("flatdefault.html", "r")
		e.data = {
			"schools": ["Carmel High School"],
			"answers": adminguesses,
			"homepage": f.read(),
			"locked": False,
			"southname":"East",
			"westname":"West",
			"eastname":"South",
			"midwestname":"Midwest" ,
			"competing": {
				"southteams" : [
					"Virginia",
					"UMBC",
					"Creighton",
					"Kansas St",
					"Kentucky",
					"Davidson",
					"Arizona",
					"Buffalo",
					"Miami FL",
					"Loyola-Chi",
					"Tennessee",
					"Wright St",
					"Nevada",
					"Texas",
					"Cincinnati",
					"Georgia St"
				],
				"westteams" : [
					"Xavier",
					"NC Central or Texas So",
					"Missouri",
					"Florida St",
					"Ohio St",
					"S Dakota St",
					"Gonzaga",
					"UNC-Green",
					"Houston",
					"San Diego St",
					"Michigan",
					"Montana",
					"Texas A&M",
					"Providence",
					"N. Carolina",
					"Lipscomb"
				],
				"eastteams" : [
					"Villanova",
					"LIU-Brooklyn or Radford",
					"Va Tech",
					"Alabama",
					"W Virginia",
					"Murray St",
					"Wichita St",
					"Marshall",
					"Florida",
					"St Bona or UCLA",
					"Texas Tech",
					"SF Austin",
					"Arkansas",
					"Butler",
					"Purdue",
					"CS Fullerton"
				],
				"midwestteams" : [
					"Kansas",
					"Penn",
					"Seton Hall",
					"NC State",
					"Clemson",
					"New Mexico St",
					"Auburn",
					"Charleston",
					"TCU",
					"Arizona St or Syracuse",
					"Michigan St",
					"Bucknell",
					"Rhode Island",
					"Oklahoma",
					"Duke",
					"Iona"
				]
			}
		}
		f.close()
		db.session.add(e)
		db.session.commit()
except:
	print("error loading",file=sys.stderr)


def locked():
	return str(models.Flat.query.first().data["locked"]).lower()=="true"

def getguesses(data):
	guesses = []
	for label in ["south","east","west","midwest"]:
		for rank in range(1,4):
			for game in range([8,4,2][rank-1]):
				guesses.append(data[label+" "+str(rank)+" "+str(game)])
	for rank in range(4,7):
		for game in range([4,2,1][rank-4]):
			guesses.append(data["F "+str(rank)+" "+str(game)])
	return guesses

def undgetguesses(data):
	guesses = {}
	i = 0
	for label in ["south","east","west","midwest"]:
		for rank in range(1,4):
			for game in range([8,4,2][rank-1]):
				guesses[label+" "+str(rank)+" "+str(game)] = data[i]
				i += 1
	guesses["south 4 0"]   = data[i+0]
	guesses["west 4 0"]    = data[i+1]
	guesses["east 4 0"]    = data[i+2]
	guesses["midwest 4 0"] = data[i+3]
	for rank in range(4,7):
		for game in range([4,2,1][rank-4]):
			guesses["F "+str(rank)+" "+str(game)] = data[i]
			i += 1
	return guesses

def isvalid(inp):
	if inp=="" or inp==None: return False
	return True


@app.route('/')
def main():
	if request.cookies.get('pass') == adminpassword:
		return render_template("adminindex.html",data=models.Flat.query.first().data,emails=[g.data["email"] for g in models.Entry.query.all() if g.data["email"] != ""])
	return render_template("index.html",bodyhtml=models.Flat.query.first().data["homepage"])




@app.route('/resources')
def resources():
	return render_template("index.html",bodyhtml=models.Flat.query.first().data["resources"])




@app.route('/bracket')
def bracket():
	if request.cookies.get('pass') == adminpassword:
		return render_template("adminbracket.html",data=models.Flat.query.first().data)
	if locked(): return render_template("message.html",message="Bracket submission has been locked.")
	return render_template("bracket.html",data=models.Flat.query.first().data)




@app.route('/database')
def database():
	if request.cookies.get('pass') != adminpassword:
		return render_template("message.html",message="You may only view this document when logged in.")
	return Response(
		render_template("database.csv",responses=[g.data for g in models.Entry.query.all()]),
		mimetype="text/csv",
		headers={"Content-disposition":
		"attachment; filename=myplot.csv"})
	# resp = render_template("database.csv",responses=[g.data for g in models.Entry.query.all()])
	# resp.mimetype = 'text/csv'
	# resp.headers['Content-disposition'] = 'attachment; filename=database.csv'

	# return resp


@app.route('/simpledatabase')
def simpledatabase():
	if request.cookies.get('pass') != adminpassword:
		return render_template("message.html",message="You may only view this document when logged in.")
	return Response(
		render_template("simpledatabase.csv",responses=[g.data for g in models.Entry.query.all()]),
		mimetype="text/csv",
		headers={"Content-disposition":
		"attachment; filename=myplot.csv"})


	# resp = render_template("simpledatabase.csv",responses=[g.data for g in models.Entry.query.all()])
	# resp.mimetype = 'text/csv'
	# resp.headers['Content-disposition'] = 'attachment; filename=database.csv'

	# return resp



@app.route('/standing')
def standings():
	if request.cookies.get('pass') == adminpassword:
		return render_template("adminstandings.html",responses=[{"data":g.data,"id":g.id} for g in models.Entry.query.all()],data=models.Flat.query.first().data)
	return render_template("standings.html",responses=[{"data":g.data,"id":g.id} for g in models.Entry.query.all()],data=models.Flat.query.first().data)


@app.route('/deleteall', methods=['POST'])
def deleteall():
	if request.cookies.get('pass') != adminpassword: return render_template("message.html",message="You are not logged in.")
	models.Entry.query.delete()
	db.session.commit()
	return render_template("message.html",message="All records have been deleted.")


@app.route('/analysis')
def analysis():
	return render_template("analysis.html",competing=models.Flat.query.first().data["competing"],responses=[g.data for g in models.Entry.query.all()])


@app.route('/setlocked', methods=['POST'])
def setlocked():
	if request.cookies.get('pass') != adminpassword: return render_template("message.html",message="You are not logged in.")
	garf = models.Flat.query.first()
	garf.data["locked"] = request.form["val"]
	flag_modified(garf, 'data')
	db.session.commit()
	return render_template("message.html",message="If this page is rendered, a mistake was made.")



@app.route('/updatehomepage', methods=['POST'])
def updatehomepage():
	if request.cookies.get('pass') != adminpassword: return render_template("message.html",message="You are not logged in.")
	garf = models.Flat.query.first()
	garf.data["homepage"] = request.form["homepage"]
	flag_modified(garf, 'data')
	db.session.commit()
	return render_template("message.html",message="Homepage successfully updated!")


@app.route('/updateresources', methods=['POST'])
def updateresources():
	if request.cookies.get('pass') != adminpassword: return render_template("message.html",message="You are not logged in.")
	garf = models.Flat.query.first()
	garf.data["resources"] = request.form["resources"]
	flag_modified(garf, 'data')
	db.session.commit()
	return render_template("message.html",message="Resources page successfully updated!")



@app.route('/updateschools', methods=['POST'])
def updateschools():
	if request.cookies.get('pass') != adminpassword: return render_template("message.html",message="You are not logged in.")
	garf = models.Flat.query.first()
	garf.data["schools"] = [g.strip() for g in request.form["schools"].split(",") if g.strip() != ""]
	flag_modified(garf, 'data')
	db.session.commit()
	return render_template("message.html",message="Schools successfully updated!")
@app.route('/updateteams', methods=['POST'])
def updateteams():
	if request.cookies.get('pass') != adminpassword: return render_template("message.html",message="You are not logged in.")
	flat = models.Flat.query.first()
	oldteams = flat.data["competing"]
	newteams = {
		"southteams":  [request.form["south "+str(x)] for x in range(16)],
		"westteams":   [request.form["west "+str(x)] for x in range(16)],
		"eastteams":   [request.form["east "+str(x)] for x in range(16)],
		"midwestteams":[request.form["midwest "+str(x)] for x in range(16)]
	}

	for k,v in flat.data["answers"].items():
		for dk in newteams.keys():
			for j,gv in enumerate(oldteams[dk]):
				if v==gv:
					flat.data["answers"][k] = newteams[dk][j]
	

	guesses = getguesses(flat.data["answers"])

	for r in models.Entry.query.all():
		for k,v in enumerate(r.data["answers"]):
			for dk in newteams.keys():
				for j,gv in enumerate(oldteams[dk]):
					if v==gv:
						r.data["answers"][k] = newteams[dk][j]
		score = 0
		for g in xrange(len(guesses)):
			if guesses[g] == r.data["answers"][g] and guesses[g] != "":
				score = score + 1
		r.data["score"] = score

		flag_modified(r, 'data')


	flat.data["competing"] = newteams

	flat.data["southname"]   = request.form["southname"]
	flat.data["westname"]    = request.form["westname"]
	flat.data["eastname"]    = request.form["eastname"]
	flat.data["midwestname"] = request.form["midwestname"]


	flag_modified(flat, 'data')
	db.session.commit()
	return render_template("message.html",message="Teams successfully updated!")



@app.route('/viewrecord')
def viewrecord():
	person = models.Entry.query.filter_by(id=request.args.get('record', '')).first()
	if person==None:
		print("No matching record was found",file=sys.stderr)
	return render_template("viewbracket.html",data=models.Flat.query.first().data,person=person.data,recguess=undgetguesses(person.data["answers"]))


@app.route('/modifyrecord', methods=['POST'])
def updaterecord():
	if request.cookies.get('pass') != adminpassword: return render_template("message.html",message="You are not logged in.")
	gh = models.Entry.query.filter_by(id=request.form["record"]).first()
	if gh==None:
		print("No matching record was found",file=sys.stderr)
	gh.data[request.form["key"]]=request.form[request.form["key"]]
	flag_modified(gh, 'data')
	db.session.commit()
	return render_template("message.html",message="If this page is rendered, a mistake was made.")

@app.route('/deleterecord', methods=['POST'])
def deleterecord():
	if request.cookies.get('pass') != adminpassword: return render_template("message.html",message="You are not logged in.")
	gh = models.Entry.query.filter_by(id=request.form["record"]).first()
	if gh==None:
		print("No matching record was found",file=sys.stderr)
	db.session.delete(gh)
	db.session.commit()
	return render_template("message.html",message="If this page is rendered, a mistake was made.")



@app.route('/admin')
def admin():
	return render_template("login.html")



@app.route('/login', methods=['POST'])
def login():
	if request.form["password"] != adminpassword: return render_template("message.html",message="You guessed the password wrong!")
	resp = make_response(render_template("message.html",message="Logged in!"))
	resp.set_cookie('pass',request.form["password"])
	return resp


@app.route('/logout', methods=['POST'])
def logout():
	if request.cookies.get('pass') != adminpassword: return render_template("message.html",message="You were already logged out!")
	resp = make_response(render_template("message.html",message="Logged out!"))
	resp.set_cookie('pass','',expires=0)
	return resp



@app.route('/handle_data', methods=['POST'])
def handle_data():
	if locked(): return render_template("message.html",message="You may not submit brackets anymore.")
	if not isvalid(request.form.get("firstname",None)): return render_template("message.html",message="You left a required field blank.")
	if not isvalid(request.form.get("lastname",None)):  return render_template("message.html",message="You left a required field blank.")
	if not isvalid(request.form.get("age",None)):       return render_template("message.html",message="You left a required field blank.")
	if not isvalid(request.form.get("persontype",None)):    return render_template("message.html",message="You left a required field blank.")
	if not isvalid(request.form.get("knowledge",None)): return render_template("message.html",message="You left a required field blank.")
	answers = getguesses(request.form)

	e = models.Entry()

	e.data = {
		"first":request.form["firstname"],
		"last":request.form["lastname"],
		"age":request.form["age"],
		"persontype":int(request.form["persontype"]),
		"school": request.form["otherschool"] if request.form["school"] == "other" else request.form["school"],
		"knowledge":int(request.form["knowledge"]),
		"email":request.form["email"],
		"score":0,
		"answers":answers
	}

	db.session.add(e)
	db.session.commit()

	return render_template("message.html",message="Your bracket has been submitted.")


@app.route('/update_standings', methods=['POST'])
def update_standings():
	if request.cookies.get('pass') != adminpassword: return render_template("message.html",message="Invalid; you are not logged in.")
	garf = models.Flat.query.first()
	garf.data["answers"] = request.form.to_dict()#needs flag_modified???
	flag_modified(garf, 'data')


	guesses = getguesses(request.form)
	worth = (([1]*8)+([2]*4)+([4]*2))*4 + [6,6,6,6,8,8,10]

	for r in models.Entry.query.all():
		score = 0
		for g in xrange(len(guesses)):
			if guesses[g] == r.data["answers"][g] and guesses[g] != "":
				score = score + worth[g]
		r.data["score"] = score

		flag_modified(r, 'data')

	db.session.commit()
	return render_template("message.html",message="The standings and graphs have been updated.")

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0', port=8080)


#school preset? analysis stuff? formatting?





