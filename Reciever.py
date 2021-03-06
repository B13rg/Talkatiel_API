from flask import Flask, request
from flask_restful import Resource, Api
from flask_cache import Cache
from sqlalchemy import create_engine
from json import dumps
from flask_jsonpify import jsonify
from flask_cors import CORS, cross_origin

db = create_engine('sqlite:///database.db')
app = Flask(__name__)
cache = Cache(app,config={'CACHE_TYPE': 'simple'})
CORS(app)
api = Api(app)
app_port='5002'

"""Get the top 50 posts.  If a number is passed in, it will get 50 posts from that index onward."""
@app.route('/Posts/<string:req_type>/<int:post_index>', methods=['GET'])
def get_posts(req_type, post_index):
	if(post_index==None):
		post_index=0
	if(req_type=="Hot"):
		return get_hot(post_index)
	elif(req_type=="New"):
		return get_new(post_index)
	elif(req_type=="Top"):
		return get_top(post_index)

@app.route('/Posts/<string:req_type>', methods=['GET'])
def simple_get(req_type):
	if(req_type=="Hot"):
		return get_hot(0)
	elif(req_type=="New"):
		return get_new(0)
	elif(req_type=="Top"):
		return get_top(0)

"""Hot posts are caches for 2 minutes"""
@cache.cached(timeout=120, key_prefix='hot_posts')	#caches for 120 seconds, or 2 minutes.
def get_hot(post_index):
	conn = db.connect()
	query = conn.execute("""SELECT postID, title, content, upvotes, downvotes FROM posts
								ORDER BY ((ABS(upvotes-downvotes) + 1)%10) * (upvotes - downvotes)
								+ (DATETIME(postDate) / 300000) DESC LIMIT {0},50""".format(post_index))
	return dumps([dict(r) for r in query])

#don't cache new because we always want the newest of the new.
def get_new(post_index):
	conn = db.connect()
	query = conn.execute("""SELECT postID, title, content, upvotes, downvotes FROM posts
								ORDER BY DATETIME(postDate) DESC LIMIT {0},50""".format(post_index))
	return dumps([dict(r) for r in query])

"""Top posts are caches for 2 minutes"""
@cache.cached(timeout=120, key_prefix='top_posts')
def get_top(post_index):
	conn = db.connect()
	query = conn.execute("SELECT postID, title, content, upvotes, downvotes FROM posts "
								"WHERE postDate BETWEEN datetime('now', '-3 days') AND datetime('now', 'localtime') "
								"ORDER BY (upvotes-downvotes) DESC LIMIT {0},50".format(post_index))
	return dumps([dict(r) for r in query])

@app.route('/Posts/<int:postID>', methods=['GET'])
def get_comments(postID):
	conn = db.connect()
	query = conn.execute("WITH mytest as "
								"(SELECT p2.postID, p2.title, p2.content, p2.upvotes, p2.downvotes "
								"FROM posts p2 where p2.parentPost={0} "
								"UNION ALL "
								"SELECT p.postID, p.title, p.content, p.upvotes, p.downvotes "
								"FROM posts p "
								"INNER JOIN MyTest M on "
								"M.postID=p.parentPost) "
								"SELECT * from mytest ORDER BY (upvotes-downvotes) DESC".format(postID))
	return dumps([dict(r) for r in query])

"""Votes on a post given the postiID and voteType"""
@app.route('/Posts/<int:postID>/<int:vote_Type>', methods=['POST'])
def vote_post(postID, vote_Type):
	conn = db.connect()
	if(vote_Type):
		conn.execute("UPDATE posts SET upvotes = upvotes+1 WHERE postID="+ str(postID))
	else:
		conn.execute("UPDATE posts SET downvotes = downvotes+1 WHERE postID="+ str(postID))
	return jsonify({'status':'success'})

"""Adds the given postID to the reports table"""
@app.route('/Posts/Report/<int:postID>', methods=['POST'])
def report_post(postID):
	conn = db.connect()
	data=request.get_json(force=True)
	userID = data['userID']
	reason = data['reason']
	conn.execute("INSERT INTO reports (reportID, postID, userID, reason) VALUES(NULL,{0},{1},'{2}')".format(postID, userID, reason))
	return jsonify({'status':'success'})

"""Deletes a post with the give postID"""
@app.route('/Posts/Delete/<int:postID>', methods=["GET"])
def delete_post(postID):
	conn = db.connect()
	conn.execute("DELETE FROM posts WHERE postID={0}".format(postID))
	return jsonify({'status':'success'})

""" Add a post to the database """
@app.route('/Posts', methods=['POST'])
def post():
	conn = db.connect()
	data=request.get_json(force=True)
	title = data['title']
	content = data['content']
	userID = data['userID']
	query = conn.execute("INSERT INTO posts (postID, title, content, upvotes, downvotes, visible, parentPost, userID) "
								"VALUES(NULL,'{0}','{1}',0,0,1,NULL,{2})".format(title,content,userID))
	return jsonify({'status':'success'})

"""Adds a comment to the given post"""
@app.route('/Posts/<int:postID>', methods=['POST'])
def comment(postID):
	conn = db.connect()
	#no title for comments
	data=request.get_json(force=True)
	content = data['content']
	postID = data['postID']
	userID = data['userID']
	query = conn.execute("INSERT INTO posts (postID, title, content, upvotes, downvotes, visible, parentPost, userID) "
								"VALUES(NULL,'','{0}',0,0,1,{1},{2})".format(content,postID,userID))
	return jsonify({'status':'success'})


@app.route('/Users/<int:userID>', methods=['GET'])
def get_User(userID):
	conn = db.connect()
	query = conn.execute("SELECT * FROM users WHERE user_id=%d " %float(userID))
	return dumps([dict(r) for r in query])

@app.route('/Users', methods=['POST'])
def post_user():
	conn = db.connect()
	data=request.get_json(force=True)
	userID = data['userID']
	phone = data['phone']
	deviceID = data['deviceID']
	admin = int(data['admin'])
	query = conn.execute("INSERT INTO users (ID, phonenumber, deviceID, points, active, admin) "
								"VALUES({0},'{1}',{2},0,1,{3})".format(userID,phone,deviceID,admin))
	return jsonify({'status':'success'})


if __name__ == '__main__':
	app.run(port=app_port)