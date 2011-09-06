from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def hello():
  return "Hello world"

@app.route("/sida")
def sida():
  return render_template("layout.html")
  
@app.route("/project/<int:id>")
def getProj(id):
  return "Projekt med id #" + str(id) + " goes here!"

if __name__ == "__main__":
  app.run(debug = True)
