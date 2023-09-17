from sqlalchemy import create_engine
from sqlalchemy import text

DB_HOST = 'gcp.connect.psdb.cloud'
DB_USERNAME = '20bpbzz0ia8j0rv81a2f'
DB_PASSWORD = 'pscale_pw_oMYjQnbjWORykEpmTk4B4FB4sJzBNYQuStWa9KTJ8ka'
DB_NAME = 'my_blog'

db_connection_string = f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}?charset=utf8mb4"

engine = create_engine(db_connection_string,
                       connect_args={"ssl": {
                         "ssl_ca": "/etc/ssl/cert.pem"
                       }})

def get_year_target():
  result_dicts = []
  
  with engine.connect() as conn:
    result = conn.execute(text("select * from yerar_targets"))

  for row in result.all():
    result_dicts.append(row._asdict())

  return result_dicts

