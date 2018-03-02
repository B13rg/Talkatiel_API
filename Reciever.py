from flask import Flask, request
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps
from flask.ext.jsonpify import jsonify

db = create_engine('sqlite:///chinook.db')
app = Flask(__name__)
api = API(app)
app_port='5002'

class Posts(Resource):
	"""Get the top 50 posts.  If a number is passed in, it will get 50 posts from that index onward."""
	def get(self, post_index=None):
		conn = db.connect()
		if post_num is None:
			#get top x posts
			query = conn.execute("/*SQL statement LIMIT 50*/")
		else:
			#get posts starting from index
			query = conn.execute("/* SQL statment */")
		result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
		return jsonify(result)
	
	""" Add a post to the database """
	def post(self):
		conn = db.connect()
		print(request.json)
		#column_name = request.json['column_name']
		query = conn.execute("INSERT INTO table_name values(null,'{0}')".format(column_name))
		return {'status':'success'}

class Users(Resource):
	def get(self, user_id):
		conn = db.connect()
		query = conn.execute("SELECT * FROM users WHERE user_id=%d " %float(employee_id))
		result = {'data': [dict(zip(tuple (query.keys()) , i)) for i in query.cursor]}
		return jsonify(result)

	def post(self):
		conn = db.connect()
		print(request.json)
		#same as post above.


		query = conn.execute("INSERT INTO table_name values()".format())
		return {'status':'success'}





api.add_resource(Posts, '/Posts')	#route 1, probably most used
api.add_resource(Posts, '/Posts/<post_index>')
api.add_resource(Users, '/Users')
api.add_resource(Users, '/Users/<user_id>')


if __name__ == '__main__':
	app.run(port=app_port)