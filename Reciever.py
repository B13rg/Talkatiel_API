from flask import Flask, request
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps
from flask.ext.jsonpify import jsonify
import time

db = create_engine('sqlite:///chinook.db')
app = Flask(__name__)
cache = Cache(app,config={'CACHE_TYPE': 'simple'})
api = API(app)
app_port='5002'

"""
TODO Some sort of authentication
TODO Return tree of comments json
"""

class Posts(Resource):
	"""Get the top 50 posts.  If a number is passed in, it will get 50 posts from that index onward."""
	@app.route('/Posts/<string:req_type>', methods='GET')
	@app.route('/Posts/<string:req_type>/<int:post_index>', methods='GET')
	def get(req_type, post_index=None):
		if(post_index==None):
			post_index=0
		if(req_type=="Hot"):
			return get_hot(post_index)
		else if(req_type=="New"):
			return get_new(post_index)
		else if(req_type=="Top"):
			return get_top(post_index)

	"""Hot posts are caches for 2 minutes"""
	@cache.cached(timeout=120, key_prefix='hot_posts')	#caches for 120 seconds, or 2 minutes.
	def get_hot(post_index):
		conn = db.connect()
		query = conn.execute("SELECT postID, title, content, upvotes, downvotes FROM posts "
									"ORDER BY LOG10(ABS(upvotes-downvotes) + 1) * SIGN(upvotes - downvotes)"
									"+ (UNIX_TIMESTAMP(created) / 300000) DESC LIMIT {0},50".format(post_index))
		result = {'data': [dict(zip(tuple (query.keys()), i)) for i in query.cursor]}	
		return jsonify(result)

	#don't cache new because we always want the newest of the new.
	def get_new(post_index):
		conn = db.connect()
		query = conn.execute("SELECT postID, title, content, upvotes, downvotes FROM posts "
									"ORDER BY UNIX_TIMESTAMP(created) DESC LIMIT {0},50".format(post_index))
		result = {'data': [dict(zip(tuple (query.keys()), i)) for i in query.cursor]}	
		return jsonify(result)

	"""Top posts are caches for 2 minutes"""
	@cache.cached(timeout=120, key_prefix='top_posts')
	def get_top(post_index):
		conn = db.connect()
		query = conn.execute("SELECT postID, title, content, upvotes, downvotes FROM posts "
									"WHERE UNIX_TIMESTAMP(created) >= (CURDATE() - INTERVAL 3 DAY) "
									"ORDER BY (upvotes-downvotes) DESC LIMIT {0},50".format(post_index))
		result = {'data': [dict(zip(tuple (query.keys()), i)) for i in query.cursor]}	
		return jsonify(result)

	"""TODO Currently only does top level comments"""
	@app.route('/Posts/<int:postID>', method='GET')
	def get_comments(postID):
		conn = db.connect()
		query = conn.execute("SELECT postID, title, content, upvotes, downvotes FROM posts "
									"WHERE parentPost = {0} "
									"ORDER BY (upvotes-downvotes) DESC".format(postID))
		result = {'data': [dict(zip(tuple (query.keys()), i)) for i in query.cursor]}	
		return jsonify(result)

	"""Votes on a post given the postiID and voteType"""
	@app.route('/Posts/<int:postID>/<int:vote_Type>', method='POST')
	def vote_post(postID, vote_Type):
		conn = db.connect()
		if(vote_Type):
			conn.execute("UPDATE posts SET upvotes = upvotes+1 WHERE postID="+ str(postID))
		else:
			conn.execute("UPDATE posts SET downvotes = downvotes+1 WHERE postID="+ str(postID))
		return {'status':'success'}

	"""Adds the given postID to the reports table"""
	@app.route('/Posts/Report/<int:postID>' method='POST')
	def report_post(postID):
		conn = db.connect()
		print(request.json)
		userID = request.json['userID']
		reason = request.json['reason']
		conn.execute("INSERT INTO reports VALUES(null,{0},{1},'{2}')".format(postID, userID, reason))
		return {'status':'success'}

	"""Deletes a post with the give postID"""
	@app.route('/Posts/Delete/<int:postID>', method="GET")
	def delete_post(postID):
		conn = db.connect()
		conn.execute("DELETE FROM posts WHERE postID={0}".format(postID))
		return {'status':'success'}
	
	""" Add a post to the database """
	@app.route('/Posts', method='POST')
	def post(self):
		conn = db.connect()
		print(request.json)
		title = request.json['title']
		content = request.json['content']
		userID = request.json['userID']
		query = conn.execute("INSERT INTO posts VALUES(null,{0},{1},NOW(),0,0,TRUE,null,{2})".format(title,content,userID))
		return {'status':'success'}

	"""Adds a comment to the given post"""
	@app.route('/Posts/<int:postID>' method='POST')
	def comment(postID):
		conn = db.connect()
		print(request.json)
		#no title for comments
		content = request.json['content']
		userID = request.json['userID']
		query = conn.execute("INSERT INTO posts VALUES(null,'',{0},NOW(),0,0,TRUE,{1},{2})".format(content,postID,userID))
		return {'status':'success'}

class Users(Resource):
	@app.route('/Users/<int:userID>' method='GET')
	def get(userID):
		conn = db.connect()
		query = conn.execute("SELECT * FROM users WHERE user_id=%d " %float(userID))
		result = {'data': [dict(zip(tuple (query.keys()) , i)) for i in query.cursor]}
		return jsonify(result)

	@app.route('/Users/' method='POST')
	def post(self):
		conn = db.connect()
		print(request.json)
		userID = request.json['userID']
		phone = request.json['phone']
		deviceID = request.json['deviceID']
		admin = request.json['admin']
		try:
			query = conn.execute("INSERT INTO users VALUES({0},{1},{2},0,TRUE,{3})".format(userID,phone,deviceID,admin))
			conn.commit()
			return {'status':'success'}
		except MYSQLdb.IntegrityError:
			return {'status':'failure'}


if __name__ == '__main__':
	app.run(port=app_port)