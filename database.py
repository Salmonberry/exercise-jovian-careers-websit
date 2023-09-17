from sqlalchemy import create_engine
from sqlalchemy import text

db_connection_string = "mysql+pymysql://srcg9yuiaj4h19ebtjdk:pscale_pw_Y8nvMNMFoiEBdoIpCHGK578u1KhTzpqQ6WqvPScaEZA@gcp.connect.psdb.cloud/my_blog?charset=utf8mb4"

engine = create_engine(db_connection_string,
                       connect_args={"ssl": {
                         "ssl_ca": "/etc/ssl/cert.pem"
                       }})


def get_year_target():
  with engine.connect() as conn:
    result = conn.execute(text("select * from yerar_targets"))

  result_dicts=[]
  
  for row in result.all():
     result_dicts.append(row._asdict()) 
  
  return result

  