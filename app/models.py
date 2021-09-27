from . import db
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from datetime import datetime
from . import login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin,db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(255),index = True)
    email = db.Column(db.String(255),unique = True,index = True)
    bio = db.Column(db.String(255))
    profile_pic_path = db.Column(db.String())
    pass_secure = db.Column(db.String(255))
    post = db.relationship('Post',backref = 'user',lazy = 'dynamic')
    comments = db.relationship('Comment',backref = 'user',lazy = 'dynamic')
    

    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')

    @password.setter
    def password(self, password):
        self.pass_secure = generate_password_hash(password)


    def verify_password(self,password):
        return check_password_hash(self.pass_secure,password)

    def __repr__(self):
        return f'User {self.username}'


class Post(db.Model):

    __tablename__ = 'posts'

    id = db.Column(db.Integer,primary_key = True)
    title = db.Column(db.String(200))
    content = db.Column(db.String())
    posted = db.Column(db.DateTime,default = datetime.utcnow)
    user_id = db.Column(db.Integer,db.ForeignKey("users.id"))
    comment = db.relationship('Comment',backref = 'post',lazy = "dynamic")

    def save_post(self):
        db.session.add(self)
        db.session.commit()

    def delete_post(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_posts(cls,id):
        posts = Post.query.filter_by(user_id = id).order_by(Post.posted.desc()).all()
        return posts

    @classmethod
    def get_post_id(cls,id):
        post = Post.query.filter_by(id = id).first()
        return post

    @classmethod
    def get_all_posts(cls):
        return Post.query.order_by(Post.posted).all()


class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer,primary_key = True)
    content = db.Column(db.String(300))
    posted = db.Column(db.DateTime,default = datetime.utcnow)
    user_id = db.Column(db.Integer,db.ForeignKey("users.id"))
    post_id = db.Column(db.Integer,db.ForeignKey("posts.id"))

    def save_comment(self):
        db.session.add(self)
        db.session.commit()

    def delete_comment(self):
        db.session.remove(self)
        db.session.commit()

    @classmethod
    def get_comment(self,id):
        comment = Comment.query.order_by(Comment.posted.desc()).filter_by(post_id = id).all()
        return comment

    @classmethod
    def get_comment_id(self,id):
        comment = Comment.query.filter_by(id = id).first()
        return comment


class Quote:
    def __init__(self,id,author,quote):
        self.id = id
        self.author = author
        self.quote = quote


class Subscriber(db.Model):
    __tablename__ = 'subscribers'

    id = db.Column(db.Integer,primary_key = True)
    email = db.Column(db.String(255),unique = True,index = True)

    def save_subscriber(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_all_mails(cls):
        return Subscriber.query.order_by(Subscriber.id).all()