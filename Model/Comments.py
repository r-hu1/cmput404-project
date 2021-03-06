from db import db
from Posts import *
import uuid

class Comments(db.Model):
    
    __tablename__ = 'comments'
    
    comment_id = db.Column(db.String(100), primary_key=True)

    author_id = db.Column(db.String(100))

    author_name = db.Column(db.String(60))

    author_host = db.Column(db.String(500))

    author_url = db.Column(db.String(600))

    author_github = db.Column(db.String(60))
    
    post_id = db.Column(db.String(100), db.ForeignKey('posts.post_id'))
    
    comment_text = db.Column(db.String(800))

    content_type = db.Column(db.String(33))
    
    creation_time = db.Column(db.DateTime)
    
    #    UniqueConstraint('post_id', name = 'uix_1')
    
    def __new__(cls, datum = None):
        
        """
            Input: See comments in __init__
            
            Description:
            Checks whether comment_id is inside datum dictionary.
            If not found, then it returns None
            """
        
        if datum == None:
            return super(Comments, cls).__new__(cls)
        
        if ('post_id') not in datum.keys():
            return None
        
        else:
            return super(Comments,cls).__new__(cls)
    
    def __init__(self,datum=None):
        
        """
            Input:
            datum is a dictionary with keys as column names and values as their corresponding values.
            eg,
            
            Description:
            This constructor sets the values of fields based on datum dictionary. If any field
            is missing from datum, its default value will be inserted.
            
            TODO:
            
            """
                
       	self.post_id = datum["post_id"]

        self.comment_text = datum["comment_text"]

        self.author_id = datum["author_id"]
        self.author_host = datum["author_host"]
        self.author_name = datum["author_name"]
        self.author_url = datum["author_url"]
        self.author_github = datum["author_github"]

        self.comment_id = datum["comment_id"]

        self.creation_time = datum["creation_time"]


    def __repr__(self):
        return '<User %r>' % (self.comment_text)

# db.create_all()
