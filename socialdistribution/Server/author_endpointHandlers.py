from model import *

"""
THINGS TO DO:

* Make sure the servers db contains an entry of our server.


"""


def isFriend(param):
	"""
	This will be called in response to :
	GET http://service/friends/<authorid1>/<authorid2>  Checks whether the author1 is friends with author 2. 

	Refer to line : 156-169		

	param["author1"] = authorid1
	param["author2"] = authorid2
	"""

	author_id1 = param["author1"]
	author_id2 = param["author2"]
	query_param={}
	query_param['author_ids'] = [author_id1, author_id2]
	results=Author_Relationships.query(query_param)
	if len(results) > 0 :
		assert(len(results) == 1), "Duplicate author_relationships entry found!"
		if results[0].relationship_type == 3 :
			return True

	query_param['author_ids'] = [author_id2, author_id1] # Search with reverse query
	results=Author_Relationships.query(query_param)
	if len(results) > 0 :
		assert(len(results) == 1), "Duplicate author_relationships entry found!"
		if results[0].relationship_type == 3 :
			return True

	return False



def getFriendList(param):


	"""
	This will be called in response to :
	GET http://service/friends/<authorid>  returns friendlist of author with authorid 

	Refer to line : 144-154		

	param["author"] = author_id
	param["local_server_Obj"] = local server obj

	TODO: add code for handling in Author_Relationships.query() when server and author id are given instead of objects
	"""

	author_id = param["author"]
	server_index = param["local_server_Obj"].server_index

    query_param={}
    query_param["server_author_id1"] = [server_index, author_id] 
	results1=[row.author2_id for row in Author_Relationships.query(query_param)] # Can modify this if the friend's server address is needed
  
    query_param["server_author_id2"] = [server_index, author_id] 
	results2=[row.author1_id for row in Author_Relationships.query(query_param)] # Can modify this if the friend's server address is needed
	results = results1 + results2

	return results


def areFriends_LIST(param):
	"""
	This will be called in response to :
	POST http://service/friends/<authorid>  POSTS a JSON containing lists of authorids and returns with a list containing those IDs 
	who are friend with authorid author

	Refer to line : 171-196

	param["query_author"] = authorid in query
	param["authors"] = [author_id1, author_id2 ,...., author_idn]
	"""

	author_id_List = param["authors"]
	my_author_id = param["query_author"]
	my_friends=[]

	for other_author_id in author_id_List :

		query_param = {}
		query_param["author1"] = my_author_id
		query_param["author2"] = other_author_id
		if isFriend(query_param) is True:
			my_friends.append(other_author_id)

	return my_friends


def processFriendRequest(param):

	"""
	This will be called in response to :
	POST http://service/friendrequest  POSTS a JSON containing author info and the to be friended author's info and this sends a friendrequest
	
	refer to line 227-244

	param["from_author"] = author id who send the request
	param["to_author"] = the author to whom the request is sent to
	param["from_serverIP"] = server IP hosting the from_author
	param["to_server_obj"] = obj of our local server 
	"""

	if len(db.session.query(Authors).filter(Authors.author_id == param["to_author"]).all()) == 0:
		return False

	local_server_Obj = param["to_server_obj"]
	from_serverIP = param["from_serverIP"]
    from_server_index=db.session.query(Servers).filter(Servers.IP == from_serverIP).all()[0].server_index
    to_server_index = local_server_Obj.server_index
    datum={}
    __App_state['no_friend_Requests'] += 1
    
    datum = {
    		'friendrequests_id' : __App_state['no_friend_Requests'], 
    		'fromAuthor_id' : param['from_author'], 
    		'fromAuthorServer_id' : from_server_index,
    		'toAuthor_id' : param["to_author"],
    		'toAuthorServer_id' : to_server_index,
    		'isChecked' : False
    		}

	new_friendRequest = Friend_Requests(datum)
	try :
		db.session.add(new_friendRequest)
		db.session.commit()
	except Exception as e:
		print "Error occured while saving new friend request: ", e
		return False

	return True


def unFriend(param):

	"""
	CLIENT-SERVER API
	This will be called in response to :
	POST http://service/unfriend  POSTS a JSON containing author info and to be unfriended author's info and this unfriends.
	
	This is an API that is not in the assigned specifications but we created this for unfriending.

	param["author1"] = author1 id 
	param["author2"] = author2 id
	param["server_1_IP"] = server1 IP  
	param["server_2_IP"] = server2 IP 

	"""

	author1_id = param["author1"]
	author2_id = param["author2"]
	server1_IP = param["server_1_IP"] 
	server2_IP = param["server_2_IP"]
	server1_index = db.session.query(Servers).filter(Servers.IP == server1_IP).all()[0].server_index
	server2_index = db.session.query(Servers).filter(Servers.IP == server2_IP).all()[0].server_index


	query_param={}
	query_param["server_author_id1"]=[server1_index, author1_id]
    query_param["server_author_id2"]=[server2_index, author2_id]	
    results1 = Author_Relationships.query(query_param)

	query_param={}
    query_param["server_author_id1"]=[server2_index, author2_id] #In reversed order	
	query_param["server_author_id2"]=[server1_index, author1_id]
    results2 = Author_Relationships.query(query_param)

   	results = results1 + results2
   	assert(len(results) == 1), "there should 1 row for each relationships"
   	
   	try:
	   	db.session.delete(results[0])
	   	db.session.commit()
   	except Exception as e:
   		print("Error while unfriending! :", e)
   		return False

	return True


def beFriend(param):

	"""
	CLIENT-SERVER API
	This will be called in response to :
	POST http://service/accept_friendship  POSTS a JSON containing author info and to be friended(accepting a request) author's info and this unfriends.
	
	This is an API that is not in the assigned specifications but we created this for unfriending.

	param["author1"] = author1 id 
	param["author2"] = author2 id
	param["server_1_IP"] = server1 IP  
	param["server_2_IP"] = server2 IP 

	"""

	author1_id = param["author1"]
	author2_id = param["author2"]
	server1_IP = param["server_1_IP"] 
	server2_IP = param["server_2_IP"]
	server1_index = db.session.query(Servers).filter(Servers.IP == server1_IP).all()[0].server_index
	server2_index = db.session.query(Servers).filter(Servers.IP == server2_IP).all()[0].server_index

	datum={}
    __App_state['no_author_relationships'] += 1

	datum["AuthorRelationship_id"] = __App_state['no_author_relationships']
	datum["authorServer1_id"] = server1_index
	datum["authorServer2_id"] = server2_index
	datum["author1_id"] = author1_id
	datum["author2_id"] = author2_id
	datum["relationship_type"] = 3 # Mutual friendship

	new_relationship = Author_Relationships(datum)
	
	try:

		db.session.add(AR)
		db.session.commit(AR)

	except Exception as e:
		print("Error while saving a relationship row! : ", e)
		return False

	return True



def getAuthor(param):

	"""
	This will be called in response to :
	GET http://service/author/<AUTHORID>  Retrieves profile information about AUTHORID author. 

	Refer to line 248-273

	param["author"] = author_id
	param["local_server_Obj"] = local server obj
	"""

	query_results = {}
	author_id = param["author"]
    results=db.session.query(Authors).filter(Authors.author_id == author_id).all()
    if len(results) == 0:
    	return query_results
	
	else:
		author = results[0]
		query_results["id"] = author.author_id
		query_results["displayName"] = author.name
		query_results["bio"] = author.bio
		query_results["friends"] = getFriendList(param)

		return query_results




def userLogin(param):

	"""
	This will be called in response to :
	POST http://service/login/  Used for login.

	example POST body:
	{
		login_name : "touqir",
		password : "123456"
	} 


	param["login_name"] = Name used for login
	param["password"] = password for authentication

	return values:
	0 if success
	1 if no match found
	2 if input data(login_name and password) is larger than specified in Authors schema
	"""

	login_name = param["login_name"]
	password = param["password"]

	if len(password) > 30:
		return 2

	if len(login_name) > 60:
		return 2

    results=db.session.query(Authors).filter(Authors.author_id == author_id).all()

    if len(results[0]) == 0:
    	return 1
	
	else :
		author = results[0]
		if author.password == password:
			return serializeAuthors(author)[0]
		else:
			return 1



def serializeAuthors(authors):

	results = []
	for author in authors:
		datum = {}
		datum["author_id"]  = author.id
		datum["name"] 	    = author.name
		datum["login_name"] = author.login_name
		datum["password"]   = author.password
		# datum["address"]    = "edmonton, alberta, Canada"
		datum["birthdate"]  = author.birthdate
		datum["bio"]        = author.bio
		datum["github_id"]  = author.github_id
		datum["numberOf_friends"] = author.numberOf_friends  
		datum["numberOf_followers"] = author.numberOf_followers  
		datum["numberOf_followees"] = author.numberOf_followees  
		datum["numberOf_friendRequests"] = author.numberOf_friendRequests
		results.append(datum)

	return results  




def userRegistration(param):

	"""
	This will be called in response to :
	POST http://service/register/  Used for login.

	example POST body:
	{
		login_name : "touqir",
		name : "Touqir Sajed",
		password : "123456",
		birthdate : "12-01-1919",
		bio : "Life is cool!",
		github_id : "CoolProgrammer"
	} 


	param["login_name"] = Name used for login
	param["password"] = password for authentication

	return values:
	0 if success
	2 if input data size or format doesnt match the ones specified in Authors schema
	1 if failure for other reasons
	3 if duplicate login_name

	Note:
	* for the post body, birthdate is actually a string object of the format "dd-mm-yyyy"
	"""

	login_name = param["login_name"]
	if len(db.session.query(Authors).filter(Authors.login_name == login_name).all()) != 0 :
		return 3

	name = param["name"]
	password = param["password"]
	birthdate_str = param["birthdate"]
	bio = param["bio"]
	github_id = param["github_id"]

	if len(login_name) > 60 :
		return 2 

	if len(name) > 60 :
		return 2 

	if len(password) > 30 :
		return 2 

	if len(bio) > 200 :
		return 2

	if len(github_id) > 200 :
		return 2

	try:
		birthdate = datetime.datetime.strptime(birthdate_str, '%d-%m-%Y')
	except Exception as e:
		print "Failed to convert birthdate to datetime object! : ", e
		return 2

	datum = {}
	datum["author_id"]  = # NEED TO CHECK THIS OUT!
	datum["name"] 	    = name
	datum["login_name"] = login_name
	datum["password"]   = password
	# datum["address"]    = "edmonton, alberta, Canada"
	datum["birthdate"]  = birthdate
	datum["bio"]        = bio
	datum["github_id"]  = github_id

	new_author = Authors(datum)

	try:
		db.session.add(new_author)
		db.session.commit()

	except Exception as e:
		print "Failed to save new registered user! : ", e
		return 1


	return 0



def userlogout(param):

	"""
	Not sure if this necessary
	"""

	pass



