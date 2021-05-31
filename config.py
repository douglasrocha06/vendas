import pymysql.cursors
import pymysql
from app import app3
from flaskext.mysql import MySQL

mysql3 = MySQL()
app3.config['MYSQL_DATABASE_USER'] = 'admin'
app3.config['MYSQL_DATABASE_PASSWORD'] = '12345678'
app3.config['MYSQL_DATABASE_DB'] = 'api_inventario'
app3.config['MYSQL_DATABASE_HOST'] = 'djlbanco.cxycaymkd24m.us-east-1.rds.amazonaws.com'
mysql3.init_app(app3)
