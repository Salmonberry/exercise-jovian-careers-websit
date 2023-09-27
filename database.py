from sqlalchemy import create_engine
from sqlalchemy import text
import os
import json

my_secret = os.environ['DB_CONNECTION_STR']
db_connection_string = my_secret

engine = create_engine(db_connection_string,
                       connect_args={"ssl": {
                         "ssl_ca": "/etc/ssl/cert.pem"
                       }})

def get_year_target_list():
  result_dicts = []
  
  with engine.connect() as conn:
    result = conn.execute(text("select * from year_target_list"))

  for row in result.all():
    result_dicts.append(row._asdict())

  return result_dicts

def get_year_detail_target_by_id(id):
  # result_dicts = []
  with engine.connect() as conn:
    result = conn.execute(
       text("SELECT * FROM year_target_detail_list WHERE id = :target_id"),
      {"target_id": id}
    )

  #获取查询结果的第一行
  row=result.fetchone()

  # print(row)

  target=None
    
  if row: 
    target= row._asdict()

    # mysql 直接返回的array为 array string json 需要转为python对象
    key_points_string= target.get("key_point_list")
    # print(key_points_string) 
    # print("type(key_points_string)",type(key_points_string))
    # 将string list json转为python的list 对象
    data=json.loads(key_points_string)
    # print(data)
    # print("type(data)",type(data))
    target["key_point_list"]=data
  
  return target

def get_year_target_by_title(title):
  # result_dicts = []
  with engine.connect() as conn:
    result = conn.execute(
       text("SELECT * FROM year_target_detail_list WHERE title = :target_title"),
      {"target_title": title}
    )

  #获取查询结果的第一行
  row=result.fetchone()

  # print(row)

  target=None
    
  if row: 
    target= row._asdict()

    # mysql 直接返回的array为 array string json 需要转为python对象
    key_points_string= target.get("key_point_list")
    # print(key_points_string) 
    # print("type(key_points_string)",type(key_points_string))
    # 将string list json转为python的list 对象
    data=json.loads(key_points_string)
    # print(data)
    # print("type(data)",type(data))
    target["key_point_list"]=data
  
  return target


def add_year_target_to_db(data):
  with engine.connect() as conn:
    query=text("INSERT INTO year_target_detail_list (title, image_url, description, summary, key_point_list) VALUES (:title, :image_url, :description, :summary, :key_point_list)")
    
    conn.execute(query, 
                 title=data['title'],
                 image_url=data['image_url'],
                 description=data['description'],
                 summary=data['summary'],
                 key_point_list=data['key_point_list'])

