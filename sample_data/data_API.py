import uuid
from Nodes import *

serverURL = "http://secure-springs-85403.herokuapp.com/"  
clientURL = "http://127.0.0.1:5000/"

author1_reg={}
author1_reg["name"] 	  = "Touqir Sajed"
author1_reg["login_name"] = "touqir"
author1_reg["password"]   = "123456"

author2_reg={}
author2_reg["name"] 	  = "Shrek the third"
author2_reg["login_name"] = "shrek3rd"
author2_reg["password"]   = "123456"


author1_log={}
author1_log["name"] 	  = "Boyan3"
author1_log["login_name"] = "boyan1"
author1_log["password"]   = "1234"
author1_log['author_id'] = '0eca786bc124425da3ccd2f605e487f2'

author2_log={}
author2_log["name"] 	  = "Shrek the third"
author2_log["login_name"] = "shrek3rd"
author2_log["password"]   = "123456"
author2_log['author_id'] = str(uuid.uuid4())


author1_edit = {}
author1_edit['bio'] = 'I am cool :D'
author1_edit['github_id'] = 'shrekkii'

def createFriendRequest():
	friendRequest1 = {}
	friendRequest1["friend"]={'id': author2_log['author_id'], 'host':clientURL, 'displayName':author2_log['name'], 'url' : "http://127.0.0.1:5000/"+author2_log['author_id']}
	friendRequest1["author"]={'id': author1_log['author_id'], 'host':serverURL, 'displayName':author1_log['name']}

	return friendRequest1
