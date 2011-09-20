#!/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, render_template, abort

app = Flask(__name__)

def get_sidebar_projects():
	toRet = []

	for i in range(10):
		toRet.append({"id": i, "title": "Projekt #" + str(i)})

	return toRet

app.jinja_env.globals.update(get_sidebar_projects=get_sidebar_projects)

@app.route("/")
def hello():
  abort(418)

@app.route("/sida")
def sida():
  return render_template("layout.html")
  
@app.route("/sida/banan")
def banan():
  return render_template("banan.html")

@app.route("/project/<int:id>")
def getProj(id):
  return "Projekt med id#" + str(id) + " goes here!"

if __name__ == "__main__":
  app.run(debug = True, port=8080, host='0.0.0.0')
 
