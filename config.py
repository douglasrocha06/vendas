import pymysql.cursors
import pymysql
from app import app, app2, app3
from flaskext.mysql import MySQL

mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'admin'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'api_clientes'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

mysql2 = MySQL()
app2.config['MYSQL_DATABASE_USER'] = 'root'
app2.config['MYSQL_DATABASE_PASSWORD'] = ''
app2.config['MYSQL_DATABASE_DB'] = 'api_produtos'
app2.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql2.init_app(app2)

mysql3 = MySQL()
app3.config['MYSQL_DATABASE_USER'] = 'root'
app3.config['MYSQL_DATABASE_PASSWORD'] = ''
app3.config['MYSQL_DATABASE_DB'] = 'api_inventario'
app3.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql3.init_app(app3)
