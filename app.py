from flask import Flask, render_template,jsonify
from database import  get_year_target
from database import get_year_target_by_id

app = Flask(__name__)

data=get_year_target()

baseurl='/api/v1'

@app.route("/")
def to_home_page():
  return render_template('home_page.html', data=data)
  
@app.route("/target/<int:target_id>",methods=["GET"])
def to_target_detail_page(target_id):
  data=get_year_target_by_id(id=target_id)
  return render_template('year_target_detail_page.html', data=data)
                
@app.route(f"{baseurl}/yeartargets",methods=["GET"])
def year_target():
  return jsonify(data)



if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True)
