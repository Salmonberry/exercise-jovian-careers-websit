from flask import Flask, render_template, jsonify, abort, request, send_from_directory
from database import get_year_target_list,get_year_target_by_title,get_year_detail_target_by_id,add_year_target_to_db
from werkzeug.utils import secure_filename
import os
from flask_cors import CORS

app = Flask(__name__)

baseurl = '/api/v1'

# 设置允许跨域访问的源列表
allowed_origins = [
    "https://my-blog-api-service.onrender.com",
    "https://exercise-jovian-careers-websit.salmonpj.repl.co"
]
# CORS(app)
# 启用CORS，允许所有来源的请求访问
CORS(app, resources={
  f"{baseurl}/uploads/*": {"origins": allowed_origins,"methods": ["GET", "POST"]},
  f"{baseurl}/year_target_detail_list": {"origins": allowed_origins,"methods": ["GET", "POST"]}
})


data = get_year_target_list()

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route("/")
def to_home_page():
  return render_template('index.html', data=data)


@app.route("/target/<int:target_id>", methods=["GET"])
def to_target_detail_page(target_id):
  data = get_year_detail_target_by_id(id=target_id)

  if not data: abort(404)

  return render_template('year_target_detail_page.html', data=data)


@app.route("/target/target_search_page", methods=["GET"])
def to_target_search_page():
  return render_template('target_search_page.html')


@app.route("/target/target_add_page", methods=["GET"])
def to_add_target_page():
  return render_template('target_add_page.html')


@app.route(f"{baseurl}/year_target_list", methods=["GET"])
def year_target_list():
  return jsonify(data)


@app.route(f"{baseurl}/year_target_detail_list/<int:target_id>",
           methods=["GET"])
def year_target(target_id):
  data = get_year_detail_target_by_id(id=target_id)
  return jsonify(data)


@app.route(f"{baseurl}/year_target_detail_list", methods=["GET"])
def get_target_by_name():
  target_title = request.args.get('target_title')

  if target_title is not None and target_title.strip() != "":
    data = get_year_target_by_title(title=target_title)

    # return render_template('target_search_page.html', data=data)
    return jsonify(data)

  else:
    return "Input string is empty"


@app.route(f"{baseurl}/year_target_detail_list", methods=["POST"])
def add_target_by_name():
  data = request.get_json()
  add_year_target_to_db(data)
  return jsonify(data)
  # if data is not None:
  #   title=


@app.route(f"{baseurl}/uploads", methods=["POST"])
def uploaded_image():
  try:
    upload_file = request.files['image']
    if upload_file.filename != '':
      import datetime
      timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
      filename = timestamp + '_' + secure_filename(upload_file.filename)
      upload_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

      print(upload_file)
      base_url = request.url_root
      image_url = base_url + 'uploads/' + filename

      return jsonify({
        'message': 'Image uploaded successfully ',
        'image_url': image_url
      })
    else:
      return jsonify({'message': 'No file selected'})
  except Exception as e:
    return jsonify({'message': 'Error: ' + str(e)})


# 添加一个路由用于访问上传的图片
@app.route('/uploads/<filename>')
def send_uploaded_file(filename):
  return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.errorhandler(404)
def not_found_error(error):
  return "404 Not Found - Page not found", 404


if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True)
