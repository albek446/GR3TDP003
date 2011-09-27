#!/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, render_template, abort
from datalager import data

app = Flask(__name__)
data.init()

def get_sidebar_projects():
  toRet = []

  err, asdf = data.retrieve_projects(sort_order="desc")
  for i in range(len(asdf)):
    toRet.append({"id": int(asdf[i]["project_no"]), "title": str(asdf[i]["project_name"])})
    if i > 10:
      break

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

@app.route("/search")
def search():
  return render_template("banan.html")

@app.route("/project/<int:id>")
def getProj(id):
  return render_template("project.html", project=data.lookup_project(id)[1])

if __name__ == "__main__":
  app.run(debug = True, port=8080, host='0.0.0.0')
 
