from flask import Flask, render_template, jsonify, abort, request, send_from_directory
from database import get_year_target_list, get_year_target_by_title, get_year_detail_target_by_id, add_year_target_to_db, update_year_target_in_db, delete_year_target_by_id, modify_year_detail_target_in_db
from werkzeug.utils import secure_filename
import os
from flask_cors import CORS

app = Flask(__name__)

baseurl = '/api/v1'

# 设置允许跨域访问的源列表
allowed_origins = [
  "https://my-blog-api-service.onrender.com",
  "https://exercise-jovian-careers-websit.salmonpj.repl.co",
  "https://exercise-jovian-careers-websit--salmonpj.repl.co/api/v1"
]
CORS(app)
# 启用CORS，允许所有来源的请求访问
# CORS(app,
#      resources={
#        f"{baseurl}/uploads/*": {
#          "origins": allowed_origins,
#          "methods": ["GET", "POST"]
#        },
#        f"{baseurl}/year_target_detail_list": {
#          "origins": allowed_origins,
#          "methods": ["GET", "POST"]
#        }
#      })

data = get_year_target_list()

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# 创建文件夹（如果不存在）
if not os.path.exists(UPLOAD_FOLDER):
  os.makedirs(UPLOAD_FOLDER)


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


#upload文件列表页
@app.route('/uploads', methods=["GET"])
def to_upload_list_page():
  # 创建一个空数组用于存储文件信息的字典
  file_info_list = []
  file_list = os.listdir(UPLOAD_FOLDER)

  for file in file_list:
    file_obj={}
    # 获取文件的完整路径
    file_path=os.path.join(UPLOAD_FOLDER,file) 
    file_obj['file_name']=file
    if os.path.isfile(file_path):
      file_size=os.path.getsize(file_path)
      
      # 将字节数转换为更友好的格式（例如，KB、MB、GB等）
      if file_size < 1024:
          size_str = f"{file_size} bytes"
      elif 1024 <= file_size < 1048576:
          size_str = f"{file_size / 1024:.2f} KB"
      elif 1048576 <= file_size < 1073741824:
          size_str = f"{file_size / 1048576:.2f} MB"
      else:
          size_str = f"{file_size / 1073741824:.2f} GB"
          
      file_obj['file_size']=size_str
      
    file_info_list.append(file_obj)
      
      
    
  return render_template('upload_list_page.html',data=file_info_list)




# API

@app.route(f"{baseurl}/uploads", methods=['PUT'])
def rename_file():

    try:
        # 获取 JSON 数据
        data = request.json

        # 从 JSON 数据中获取旧文件名和新文件名
        old_file_name = data.get('origin_name')
        new_file_name = data.get('rename')

        # 拼接旧文件路径和新文件路径
        old_file_path = os.path.join('uploads', old_file_name)
        new_file_path = os.path.join('uploads', new_file_name)
          
        # 检查旧文件是否存在
        if not os.path.exists(old_file_path):
            return jsonify({'error': 'Old file not found','origin_name':old_file_path}), 404

        # 执行文件重命名操作
        os.rename(old_file_path, new_file_path)

        return jsonify({'message': 'File renamed successfully'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route(f"{baseurl}/uploads/<string:file_name>", methods=["DELETE"])
def delete_file_by_name(file_name):
    try:
        # 构建要删除的文件的完整路径
        file_path = os.path.join(UPLOAD_FOLDER, file_name)

        # 检查文件是否存在
        if os.path.exists(file_path):
            # 如果文件存在，执行删除操作
            os.remove(file_path)
            return jsonify({'message': 'Delete success','file':file_path}), 200
        else:
            # 如果文件不存在，返回错误响应
            return jsonify({'error': 'File not found','file':file_path}), 404

    except Exception as e:
        # 处理异常情况
        return jsonify({'error': str(e)}), 500

@app.route(f"{baseurl}/year_target_detail_list/<int:target_id>",
           methods=["PUT"])
def update_year_target_detail(target_id):
  target = get_year_detail_target_by_id(target_id)

  if (target is not None):
    target['title'] = request.json['title']
    target['description'] = request.json['description']
    target['image_url'] = request.json['image_url']
    target['key_point_list'] = request.json['key_point_list']
    target['summary'] = request.json['summary']

    update_year_target_in_db(target, target_id)
    return jsonify({'message': 'update success', 'year_target': target})

  return jsonify({'error': 'update faile', 'target': target})


@app.route(f"{baseurl}/year_target_detail_list/<int:target_id>",methods=["DELETE"])
def delete_year_detail_target_by_id(target_id):
  target = get_year_detail_target_by_id(target_id)

  if (target is not None):
    delete_year_target_by_id(target_id)
    return jsonify({'message': 'delete success', 'target': target})

  return jsonify({'error': 'delete faile', 'target': target})


@app.route(f"{baseurl}/year_target_detail_list/<int:target_id>",
           methods=["PATCH"])
def modify_year_detail_target_by_id(target_id):
  target = get_year_detail_target_by_id(target_id)

  if (target is not None):
    data = request.get_json()
    # if 'title' in data:
    #   target['title']=data['title']
    # if 'image_url' in data:
    #   target['image_url']=data['image_url']
    # if 'description' in data:
    #   target['description']=data['description']
    # if 'summary' in data:
    #   target['summary']=data['summary']
    # if 'key_point_list' in data:
    #   target['key_point_list']=data['key_point_list']
    # for key, value in data.items():
    #         if key in target:
    #             target[key] = value

    modify_year_detail_target_in_db(data, target_id)

    return jsonify({'message': 'modify success', 'year_target': target})

  return jsonify({'error': 'modify faile', 'target': target}), 404


@app.errorhandler(404)
def not_found_error(error):
  return "404 Not Found - Page not found", 404


if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True)
