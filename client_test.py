import init_location
import requests
from sample_data.data_API import *
import unittest
import json
import re
from Nodes import *

URL = "http://secure-springs-85403.herokuapp.com/"  
firstTime = True
"""
CS stands for Client-Server
"""

COOKIE_NAMES = ["cookie_cmput404_author_id","cookie_cmput404_session_id","cookie_cmput404_github_id"] 

class Test_CS_API(unittest.TestCase):
    
    s=requests.Session()

    def createAuthHeaders():

        auth_str = b"%s:%s"%("servertoserver", "654321")
        userAndPass = b64encode(auth_str).decode("ascii")
        headers = { 'Authorization' : 'Basic %s' %  userAndPass }
        return headers

    def setUp(self):
        global firstTime
        self.serverURL = URL
        # if firstTime:
        #     self.s = requests.Session()
        #     firstTime = False


    def test(self):
    	self.authors_1()
    	self.posts_1()

    def authors_1(self):
	    self.sample_Login(author1_log)
        self.isFriends = False
        self.friend = author2_log['author_id'] 
	    data = {}
	    data['query'] = 'friends'
	    data['authors'] = [author1_log['author_id'], author2_log['author_id']]
        
        self.sample_ifFriends(author1_log, author2_log, data)
        resp = self.sample_getFriendList(author1_log)
        self.matchFriendList(resp)
        fetched_author=self.sample_FetchAuthor(author1_log)
        self.match_author1(fetched_author, author1_log) 
       
        FR1 = createFriendRequest()
        self.sample_friendrequest(FR1)
        self.sample_AcceptFriendRequests(FR1)

        self.isFriends = True
        self.sample_ifFriends(author1_log, author2_log, data)        
        resp = self.sample_getFriendList(author1_log)
        self.matchFriendList(resp)
        fetched_author=self.sample_FetchAuthor(author1_log)
        self.match_author1(fetched_author, author1_log) 


	def posts_1(self):
		pass

    def login_(self):
        author1_log["author_id"] = self.sample_Registration(author1_reg)
        self.sample_Logout()
        self.authorize(author1_log['author_id'])
        self.sample_Login(author1_log)
        self.sample_Logout()
        self.sample_Login(author1_log)
        self.sample_EditProfile()
        self.sample_Logout()
        self.sample_FetchAuthor()
        self.sample_FetchAuthorByName()


    def authorize(self, ID):
        url = URL + "/secretAuthorization/" + ID
        requests.get(url)

    def parseCookie(self, cookies):
        new={}

        for name in COOKIE_NAMES:
            if name in cookies.keys():
                new[name]=cookies.get(name)
            else:
                new[name]=None

        self.cookies = new

    def prepCookie(self, prepped):
        new = {}
        for name in self.s.cookies.keys():
            if name in COOKIE_NAMES:
                new[name] = self.s.cookies.get(name)
                # s=s+self.s.cookies.get(name)+'; '

        prepped.prepare_cookies(new)
        return prepped

    def cookie_assert(self, cookies, author=None, opt=None):
        print cookies.keys()
        self.parseCookie(cookies)
        assert(self.cookies[COOKIE_NAMES[0]] != None), "there must be some author_id"
        assert(self.cookies[COOKIE_NAMES[1]] != None), "there must be some session_id"
        if opt == "github_id_present":
            assert(self.cookies[COOKIE_NAMES[2]] != None), "there must be some github_id"
        if author != None:
            assert(self.cookies[COOKIE_NAMES[0]] == author['author_id']), "author_ids must match"

    def sample_Login(self, author):

        url = self.serverURL + "/login"
        headers = {'Content-type': 'application/json'}
        req1 = requests.Request('POST', url, data=json.dumps(author), headers=headers)
        prepp1 = req1.prepare()
        # prepp1 = self.prepCookie(prepp1)
        resp = self.s.send(prepp1)
        # print(resp.text)
        body = json.loads(resp.text)
        print body["status"]
        assert(body["status"] == "SUCCESS"), "Should be a success!"
        assert(body["name"] != None), "A display name should be there"
        self.cookie_assert(resp.cookies, author=author)


    def sample_Registration(self, author):

        url = self.serverURL + "/register"
        headers = {'Content-type': 'application/json'}
        req1 = requests.Request('POST', url, data=json.dumps(author), headers=headers)
        # req1 = self.prepCookie(req1)
        prepp1 = req1.prepare()
        resp = self.s.send(prepp1)
        body = json.loads(resp.text)
        assert(body["status"] == "NOT_AUTHORIZED")
        assert(body["name"] != None), "A display name should be there"
        # self.cookie_assert(resp.cookies)
        return body['author_id']



    def sample_Logout(self):

        url = self.serverURL + "/logout"
        req1 = requests.Request('GET', url)
        prepp1 = req1.prepare()
        prepp1 = self.prepCookie(prepp1)
        resp = self.s.send(prepp1)
        body = json.loads(resp.text)
        assert(body["status"] == "SUCCESS"), "Should be a success!"


    def sample_EditProfile(self):

        url = self.serverURL + "/editProfile"
        headers = {'Content-type': 'application/json'}
        req1 = requests.Request('POST', url, data=json.dumps(author1_edit), headers=headers)
        prepp1 = req1.prepare()
        prepp1 = self.prepCookie(prepp1)
        resp = self.s.send(prepp1)
        body = json.loads(resp.text)
        # print body["status"]
        assert(body["status"] == "SUCCESS"), "Should be a success!"


    def sample_FetchAuthor(self, author):

        # headers = {'Foreign_host': 'false'}        
        # url = self.serverURL + "/author/"+ author["author_id"]
        headers = self.createAuthHeaders()
        prefix, suffix = getAPI(URL, 'GET/author/A')
        url = prefix + author['author_id'] + suffix
        req1 = requests.get(url, headers = headers)
        # prepp1 = req1.prepare()
        # prepp1 = self.prepCookie(prepp1)
        # resp = self.s.send(prepp1)
        assert(req1.status_code == 200)
        body = json.loads(req1.text)
        return body
        # print "author_id: ", author1_log["author_id"]
        # assert(body["status"] == "SUCCESS"), "Should be a success!"
        # self.match_author1(body, author)


    def sample_FetchAuthorByName(self):
        
        names=author1_reg['name'].split()
        first = ""
        last = ""
        if len(names) == 1:
            first=names[0]
        if len(names) == 2:
            first=names[0]
            last=names[1]

        if len(names) > 2:
            first=names[0]
            last = "".join(names[1:])

        url = self.serverURL + "authorByName/?first=%s&last=%s"%(first,last)
        req1 = requests.Request('GET', url)
        prepp1 = req1.prepare()
        # prepp1 = self.prepCookie(prepp1)
        resp = self.s.send(prepp1)
        body = json.loads(resp.text)
        print body["status"]
        # print "author_id: ", author1_log["author_id"]
        assert(body["status"] == "SUCCESS"), "Should be a success!"
        assert("authors" in body.keys())
        print body
        self.match_author1(body['authors'][0])


    def match_author1(self, body, author):

        assert(body['id'] == author['author_id'])
        assert(body['host'] == URL)
        assert(body['displayName'] == author['name'])
        assert(body['url'] == (URL+'author/'+author['author_id']))
        exists = False 
        for friend in body['friends']:
            if friend['id'] == self.friend:
                exists = True

        if self.isFriends:
            assert(exists == True)
        else:
            assert(exists == False)



    def friend_(self):
        # self.sample_Registration(author1_reg)
        # author1_log["author_id"] = self.cookies[COOKIE_NAMES[0]]
        self.sample_Login(author1_log)
        author1_log["author_id"] = self.cookies[COOKIE_NAMES[0]]
        self.sample_Logout()
        author2_log["author_id"] = self.sample_Registration(author2_reg)
        self.authorize(author2_log["author_id"])
        FR1 = createFriendRequest()
        self.sample_Login(author1_log)
        self.sample_friendrequest(author1_log, author2_log, FR1)
        self.sample_Logout()
        self.sample_Login(author2_log)
        received_FR = self.sample_getFriendRequests(author1_log)
        self.sample_AcceptFriendRequests(FR1)
        POST_body = {}
        POST_body['query'] = 'friends'
        POST_body['author'] = author2_log['author_id']
        POST_body['authors'] = [author1_log['author_id']]
        self.sample_ifFriends(author2_log, author1_log, POST_body)

        FL_body = self.sample_getFriendList(author2_log)
        self.matchFriendList(FL_body, [author1_log['author_id']])

        self.sample_Unfriend(author1_log['author_id'])
        FL_body = self.sample_getFriendList(author2_log)
        self.matchFriendList(FL_body, [])
        self.sample_Logout()



    def sample_friendrequest(self, body):

        headers = self.createAuthHeaders()
    	prefix, suffix = getAPI(URL, 'POST/friendrequest')
        url = prefix + suffix
        headers['Content-type'] = 'application/json'
        req1 = requests.post(url, data=json.dumps(body), headers=headers)
        # prepp1 = req1.prepare()
        # prepp1 = self.prepCookie(prepp1)
        # resp = self.s.send(prepp1)
        assert(req1.status_code == 200)
        body = json.loads(req1.text)
        # print body["status"]
        # assert(body["status"] == "SUCCESS"), "Should be a success!"


    def sample_getFriendRequests(self, from_author):

        url = self.serverURL + "getFriendRequests"
        req1 = requests.Request('GET', url)
        prepp1 = req1.prepare()
        prepp1 = self.prepCookie(prepp1)
        resp = self.s.send(prepp1)
        body = json.loads(resp.text)
        # print body
        assert(len(body['friendRequestList']) == 1)
        FR = body['friendRequestList'][0]
        assert(FR['fromAuthor_id'] == from_author['author_id'])
        return FR


    def sample_AcceptFriendRequests(self, FR):

        url = self.serverURL + "acceptFriendRequest"
        headers = {'Content-type': 'application/json'}
        data = {}
        data['author'] = FR['friend']['id']
        data['server_address'] = FR['friend']['host']
        req1 = requests.Request('POST', url, data=json.dumps(data), headers=headers)
        prepp1 = req1.prepare()
        prepp1 = self.prepCookie(prepp1)
        resp = self.s.send(prepp1)
        body = json.loads(resp.text)
        # assert()
        # assert(body["status"] == "SUCCESS")


    def sample_getFriendList(self, logged_author):

    	"""
		Will return friendlist of logged_author 
    	"""
    	prefix, suffix = getAPI(URL, 'GET/friends/A')
        url = prefix + logged_author['author_id'] + suffix
        req1 = requests.get(url)
        # prepp1 = req1.prepare()
        # prepp1 = self.prepCookie(prepp1)
        # resp = self.s.send(prepp1)
        assert(req1.status_code == 200)
        body = json.loads(req1.text)
        return body

    def sample_ifFriends(self, author1, author2, POST_request):
    	prefix, suffix = getAPI(URL, 'GET/friends/A1/A2')
        url = prefix + str(author1['author_id']) + "/" + str(author2['author_id']) + suffix
        req1 = requests.get(url)
        # prepp1 = req1.prepare()
        # prepp1 = self.prepCookie(prepp1)
        # resp = self.s.send(prepp1)
        assert(req1.status_code == 200)
        body_duo = json.loads(req1.text)

    	prefix, suffix = getAPI(URL, 'POST/friends/A')
        url = prefix + author1['author_id'] + suffix
        headers = {'Content-type': 'application/json'}
        req1 = requests.post(url, data=json.dumps(POST_request), headers=headers)
        # prepp1 = req1.prepare()
        # prepp1 = self.prepCookie(prepp1)
        # resp = self.s.send(prepp1)
        assert(req1.status_code == 200)
        body_multiple = json.loads(req1.text)

        self.matchIfFriends(body_duo, body_multiple, author1['author_id'], [author2['author_id']])


    def matchIfFriends(self, response_duo, response_multiple, logged_author):

        assert(response_duo['query'] == 'friends')
        # print response_duo['authors']
        assert(set(response_duo['authors']) == set([logged_author]+TrueFriends))
        if self.isFriends == True:
        	assert(response_duo['friends'] == True)
    	else:
	    	assert(response_duo['friends'] == False)

        assert(response_multiple['query'] == 'friends')
        assert(response_multiple['author'] == logged_author)
        print response_multiple["authors"]
        if self.isFriends == True:
        	assert(self.friend in response_multiple['authors'])
    	else:
        	assert(self.friend not in response_multiple['authors'])


    def matchFriendList(self, response):

        assert(response['query'] == 'friends')
        if self.isFriends == True:
        	assert(self.friend in response['authors'])
    	else:
	    	assert(self.friend not in response['authors'])



    def sample_Unfriend(self, toUnfriend_id):

        url = self.serverURL + "unFriend"
        headers = {'Content-type': 'application/json'}
        data = {}
        data['author'] = toUnfriend_id
        data['server_address'] = self.serverURL
        req1 = requests.Request('POST', url, data=json.dumps(data), headers=headers)
        prepp1 = req1.prepare()
        prepp1 = self.prepCookie(prepp1)
        resp = self.s.send(prepp1)
        body = json.loads(resp.text)
        assert(body['status'] == 'SUCCESS')




    def sample_getPosts(self):
    	prefix, suffix = getAPI(URL, 'GET/posts')
    	url = prefix + suffix
    	req1 = requests.get(url)
        body = json.loads(req1.text)
        return body

    def check_getPosts(self, body):
        posts = body['posts']
        allPublic = True
        for post in posts:
            if post['visibility'] != "PUBLIC":
                allPublic = False

        assert(allPublic == True)

    def sample_getAuthorPosts(self, author_id):
    	prefix, suffix = getAPI(URL, 'GET/author/A/posts')
    	url = prefix + author_id + suffix
    	req1 = requests.get(url)
    	body = json.loads(req1.text)
    	return body

    def check_getAuthorPosts(self, body, author_id):
        posts = body['posts']
        allAuthorPost = True
        for post in posts:
            if post['author']['id'] != author_id:
                allAuthorPost = False

        assert(allAuthorPost == True)

	def sample_getPost_ID(self, post_id):
		prefix, suffix = getAPI(URL, 'GET/posts/P')
    	url = prefix + post_id + suffix
    	req1 = requests.get(url)
        body = json.loads(req1.text)
        return body

    def check_getPost_ID(self, thePost, post_body, exists):
        posts = post_body['posts']
        post_id = thePost['id']
        content = thePost['content']
        if exists == True:
            assert(len(post) == 1)
        else:
            assert(len(post) == 0)

        for post in posts:
            assert(post["id"] == post_id)
            assert(post['content'] == content )


    def sample_getComments(self, post_id):
    	prefix, suffix = getAPI(URL, 'GET/posts/P/comments')
    	url = prefix + post_id + suffix
    	req1 = requests.get(url)
        body = json.loads(req1.text)
        return body

    def check_getComments(self, body, comments)
        get_comments = body['comment']
        assert(len(get_comments) == len(comments))
        ids1 = [comment['guid'] for comment in get_comments]
        contents1 = [comment['comment'] for comment in get_comments]
        ids2 = [comment['guid'] for comment in comments]
        contents2 = [comment['comment'] for comment in comments]

        assert(set(ids1) == set(ids2))
        assert(set(comments1) == set(comments2))


    def sample_makeComments(self, data, post_id):
    	prefix, suffix = getAPI(URL, 'POST/posts/P/comments')
    	url = prefix + post_id + suffix
    	req1 = requests.post(url, data=data)
        body = json.loads(req1.text)
        return body



if __name__ == '__main__':
    unittest.main()