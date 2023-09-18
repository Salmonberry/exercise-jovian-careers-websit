from flask import Flask, render_template,jsonify
from database import  get_year_target

app = Flask(__name__)

data=get_year_target()

baseurl='/api/v1'

@app.route("/")
def to_home_page():
  return render_template('home_page.html', data=data)
  
@app.route("/target/<int:target_id>",methods=["GET"])
def to_target_detail_page():
  return render_template('', id=id)

@app.route(f"{baseurl}/yeartargets",methods=["GET"])
def year_target():
  return jsonify(data)



if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True)
