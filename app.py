from flask import Flask, render_template, jsonify, abort, request
from database import get_year_target_list
from database import get_year_target_by_id
from database import get_year_target_by_title

app = Flask(__name__)

data = get_year_target_list()

baseurl = '/api/v1'


@app.route("/")
def to_home_page():
  return render_template('home_page.html', data=data)


@app.route("/target/<int:target_id>", methods=["GET"])
def to_target_detail_page(target_id):
  data = get_year_target_by_id(id=target_id)

  if not data: abort(404)

  return render_template('year_target_detail_page.html', data=data)


@app.route("/target/target_search_page", methods=["GET"])
def to_target_search_page():
  return render_template('target_search_page.html')


@app.route(f"{baseurl}/year_target_list", methods=["GET"])
def year_target_list():
  return jsonify(data)


@app.route(f"{baseurl}/year_target/<int:target_id>", methods=["GET"])
def year_target(target_id):
  data = get_year_target_by_id(id=target_id)
  return jsonify(data)


@app.route(f"{baseurl}/target/target_search", methods=["GET"])
def get_target_by_name():
  target_title = request.args.get('target_title')

  if target_title is not None and target_title.strip() != "":
    data = get_year_target_by_title(title=target_title)
  
    # return render_template('target_search_page.html', data=data)
    return jsonify(data)

  else:
    return "Input string is empty"


@app.errorhandler(404)
def not_found_error(error):
  return "404 Not Found - Page not found", 404


if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True)
