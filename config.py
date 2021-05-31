import pymysql.cursors
import pymysql
from app import app, app2, app3
from flaskext.mysql import MySQL

mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'admin'
app.config['MYSQL_DATABASE_PASSWORD'] = '12345678'
app.config['MYSQL_DATABASE_DB'] = 'api_clientes'
app.config['MYSQL_DATABASE_HOST'] = 'djlbanco.cxycaymkd24m.us-east-1.rds.amazonaws.com'
mysql.init_app(app)

mysql2 = MySQL()
app2.config['MYSQL_DATABASE_USER'] = 'admin'
app2.config['MYSQL_DATABASE_PASSWORD'] = '12345678'
app2.config['MYSQL_DATABASE_DB'] = 'api_produtos'
app2.config['MYSQL_DATABASE_HOST'] = 'djlbanco.cxycaymkd24m.us-east-1.rds.amazonaws.com'
mysql2.init_app(app2)

mysql3 = MySQL()
app3.config['MYSQL_DATABASE_USER'] = 'admin'
app3.config['MYSQL_DATABASE_PASSWORD'] = '12345678'
app3.config['MYSQL_DATABASE_DB'] = 'api_inventario'
app3.config['MYSQL_DATABASE_HOST'] = 'djlbanco.cxycaymkd24m.us-east-1.rds.amazonaws.com'
mysql3.init_app(app3)
