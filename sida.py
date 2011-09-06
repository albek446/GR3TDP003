from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello():
  return "Hello world"

app.route("/sida")
def sida():
  return "Working title goes here"

if __name__ == "__main__":
  app.run()
