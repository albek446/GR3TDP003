from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello():
  return "Hello world"

@app.route("/sida")
def sida():
  return "Working title goes here"
  
@app.route("/project/<int:id>")
def getProj(id):
  return "Projekt med id#" + str(id) + " goes here!"

if __name__ == "__main__":
  app.run(debug = True)
