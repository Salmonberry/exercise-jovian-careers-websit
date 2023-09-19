from sqlalchemy import create_engine
from sqlalchemy import text
import os

my_secret = os.environ['DB_CONNECTION_STR']
db_connection_string = my_secret

engine = create_engine(db_connection_string,
                       connect_args={"ssl": {
                         "ssl_ca": "/etc/ssl/cert.pem"
                       }})

def get_year_target():
  result_dicts = []
  
  with engine.connect() as conn:
    result = conn.execute(text("select * from year_target_list"))

  for row in result.all():
    result_dicts.append(row._asdict())

  return result_dicts

def get_year_target_by_id(id):
  result_dicts = []
  with engine.connect() as conn:
    result = conn.execute(
       text("SELECT * FROM year_target_detail")
    )
    
  for row in result.all():
    result_dicts.append(row._asdict())

  obj=result_dicts[id-1]
  print(obj)
    
  
  return obj

