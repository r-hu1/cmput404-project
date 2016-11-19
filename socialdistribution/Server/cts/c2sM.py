from flask import Flask, jsonify
from flask_restful import Resource, Api, abort, reqparse
from model import *
from pch import *
import random, os

app = Flask(__name__)
api = Api(app)

handler = RestHandlers()

def getCookie(Operation_str):
    
    COOKIE ={}
    # print request.cookies.keys()
    for name in COOKIE_NAMES:
        if name in request.cookies.keys():
            
            if name == COOKIE_NAMES[0]:
                COOKIE['author_id'] = request.cookies[name]
            elif name == COOKIE_NAMES[1]:
                COOKIE['session_id'] = request.cookies[name]
            elif name == COOKIE_NAMES[2]:
                COOKIE['github_id'] = request.cookies[name]
'''            elif name == COOKIE_NAMES[3]:
                COOKIE['post_id'] = request.cookies[name]
            elif name == COOKIE_NAMES[4]:
                COOKIE['comment_id'] = request.cookies[name]
            elif name == COOKIE_NAMES[5]:
                COOKIE['image_id'] = request.cookies[name]
 '''

    if COOKIE == {}:
        print "WARNING! Cookie not found during %s!"%(Operation_str)
        return "status : CLIENT_FAILURE", 200

    return COOKIE


class Post(Resource):
	def get(self, post_id):
        
        
        output = getCookie("get_post")
        if type(output) == flask.wrappers.Response: #In case if cookie is not found a status code =200 response is send back.
            return output
        
        cookie = output
        if "session_id" in cookie.keys[]:
            sessionID = cookie["session_ids"]:
            if sessionID in APP_state["session_ids"]:
    
    
                data = handler.getPost(post_id)
                rt =	{
                                    "post_id"	: data[0].post_id,
                                    "title" :	data[0].title,
                                    "text"	:	data[0].text,	
                                    "creation_time" : data[0].post.creation_time
                            }
                return jsonify(rt)


	def delete(self, post_id):

        output = getCookie("delete_post")
        if type(output) == flask.wrappers.Response: #In case if cookie is not found a status code =200 response is send back.
            return output
            
        cookie = output
        if "session_id" in cookie.keys[]:
            sessionID = cookie["session_ids"]:
            if sessionID in APP_state["session_ids"]:
                
                if handler.delete_post(post_id):
                    return '', 201



class All_Post(Resource):
	def get(self):
		rtl = [] 
		data = handler.getAllPosts()
		for entry in data:
			rtl.append({
									"post_id" :	entry[0].post_id,
									"title" :	entry[0].title,
									"text"	:	entry[0].text,
									"creation_time" : entry[0].creation_time,
									"author_id"	: entry[0].author_id
								})	

		return jsonify(rtl)	



	def post(self):
        
        
        
        output = getCookie("edit_post")
        if type(output) == flask.wrappers.Response: #In case if cookie is not found a status code =200 response is send back.
            return output
        
        cookie = output
        if "session_id" in cookie.keys[]:
            sessionID = cookie["session_ids"]:
            if sessionID in APP_state["session_ids"]:
                
                data = request.form
                return handler.make_post(data), 201	


# gets all post made by AUTHOR_ID for current author to view.
class AuthorToAuthorPost(Resource):

    def get(self, AUTHOR_ID):
        
        output = getCookie("view_author_id_post")
        if type(output) == flask.wrappers.Response: #In case if cookie is not found a status code =200 response is send back.
            return output

        cookie = output
        if "session_id" in cookie.keys[]:
            sessionID = cookie["session_ids"]:
            if sessionID in APP_state["session_ids"]:


            data = handler.getVisiblePostsByAuthor(AUTHOR_ID)
            
            if selected_post == []:
                return "status : NO_MATCH", 200
            else:
                for entry in data:
                    rtl.append({
                               "post_id" :	entry[0].post_id,
                               "title" :	entry[0].title,
                               "text"	:	entry[0].text,
                               "creation_time" : entry[0].creation_time,
                               "author_id"	: entry[0].author_id
                               })	
                               
                return jsonify(rtl)



class Comment(Resource):
	def post(self):
    
        output = getCookie("edit_post")
            if type(output) == flask.wrappers.Response: #In case if cookie is not found a status code =200 response is send back.
                return output

        cookie = output
        if "session_id" in cookie.keys[]:
            sessionID = cookie["session_ids"]:
            if sessionID in APP_state["session_ids"]:
        
        
                data = request.form
                return handler.make_comment(data), 201

class Edit_Post(Resource):
    
    def post(self, post_id):
        
        output = getCookie("edit_post")
        if type(output) == flask.wrappers.Response: #In case if cookie is not found a status code =200 response is send back.
            return output
    
        cookie = output
        if "session_id" in cookie.keys[]:
            sessionID = cookie["session_ids"]:
            if sessionID in APP_state["session_ids"]:
                userID = APP_state["session_ids"][sessionID]
                data = request.form
                result = handler.updateProfile(data)
                if result == True:
                    return "status : SUCCESS", 200
                elif result == "NO_MATCH":
                    return "status : NO_MATCH", 200
                elif result == "DB_FAILURE":
                    return "status : DB_FAILURE", 200
        
            else:
                print "WARNING! Session id not inside server!"
                return "status : INVALID_SESSION_ID", 200

        else :
            
            print 'WARNING! "session_id" field is not found inside cookie!'
            return "status : CLIENT_FAILURE", 200






api.add_resource(Post, '/<string:post_id>')
api.add_resource(Comment, '/api/comment')
api.add_resource(All_Post, '/service/posts')

if __name__ == '__main__':
	for i in range(1, 55):
		currentTime = datetime.now()
		post = {}
		post["author_id"] = i
		post["title"] = "test" + str(i)
		post["text"]="TEXT" + str(i)
		post["view_permission"]=random.randint(1, 5)
		post["post_type"]=1
		post["numberOf_comments"]=0
		post["numberOf_URL"]=0
		post["numberOf_images"]=0
		post["images"] = []
		post["images"].append(os.urandom(100000))
		handler.make_post(post)

	app.run(debug=True)



