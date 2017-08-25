from flask import Flask
from flask_pymongo import PyMongo, pymongo
from pymongo import MongoClient
from flask import render_template


app = Flask(__name__)
client1 = MongoClient('mongodb://localhost:27017/')
client2 = MongoClient('mongodb://localhost:27017/')
db1 = client1.worldbanks #mongoimport -d worldbanks -c code world_banks.json
collection1 = db1.worldbanks
db2 = client2.worldcountries #mongoimport -d worldcountries -c code world_countries.json
collection2 = db2.worldcountries
mongo = PyMongo(app)


class Country:
	def __init__(self, id_code, lendprojectcost, project_name,color):
		self.id_code = id_code
		self.lendprojectcost = lendprojectcost
		self.project_name = project_name
		self.color = color	
		

@app.route('/main')
def main():
	results_wrold_bank = db1.code.find()
	country = []
	for rwb in results_wrold_bank:
		result_country_code = db2.code.find_one({"properties":{"name":rwb["countryshortname"]}})
		results_proj = db1.code.find({"countryshortname":rwb["countryshortname"]})
		output_projects = ""
		output_cost = 0
		index = 0 
		for rp in results_proj:
			index += 1
			output_cost += int(rp["lendprojectcost"])
			output_projects += str(rp["project_name"]) +" : "+str(rp["lendprojectcost"])+"$"
			if index == results_proj.count():
				output_projects	+= ". "	
			else:
				output_projects += ", "
			if output_cost > 5000000000:
				color = 'HIGH'
			elif output_cost > 1000000000:
				color = 'MEDIUM'
			elif output_cost < 1000000000:
				color = 'LOW'
		try:
			country.append(Country(result_country_code["id"], output_cost, output_projects, color))
		except TypeError:
			pass
	return render_template("index.html", country = country)


@app.route('/test1')
def test1():
	results = db2.code.find_one({"properties":{"name":"Samoa"}})
	#output = ""
	#for r in results:
		#output += str(r["id"])+"<br>"	
		#print (output)
	return results["id"]


@app.route('/test2')
def test2():
	results = db1.code.find()
	output = ""
	for r in results:
		output += str(r["countryshortname"])+" == "+str(r["countryshortname"])+"<br>"
		print (output)
	return output


@app.route('/test3')
def test3():
	results = db1.code.find({"countryname":"Russian Federation"})
	output = 0
	for r in results:
		output += int(r["lendprojectcost"])
		print (output)
	return render_template("index1.html",output = output)


