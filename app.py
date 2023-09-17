from flask import Flask, render_template,jsonify
from database import  get_year_target

app = Flask(__name__)

template = 'home.html'
data=data=get_year_target()

@app.route("/")
def hello_world():
  return render_template(template, data=data)


@app.route("/api/v1/yeartargets")
def year_target():
  return jsonify(data)


if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True)
