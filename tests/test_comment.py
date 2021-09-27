import unittest
from app.models import Comment,Post,User
from app import db

class CommentTestModel(unittest.TestCase):

    def setUp(self):

        self.user_James = User(username = 'James',password = 'potato', email = 'james@ms.com')
        self.new_post = Post(title = 'Skills',content = 'Improve in your body language to show confidence in your skills')
        self.new_comment = Comment(content = 'It was an interesting blog would love to hear more about it',user = self.user_James,post = self.new_post)

    def tearDown(self):
        Comment.query.delete()
        User.query.delete()
        Post.query.delete()

    def test_check_instance_variables(self):
        self.assertEquals(self.new_comment.content,'It was an interesting blog would love to hear more about it')
        self.assertEquals(self.new_comment.user,self.user_James)
        self.assertEquals(self.new_comment.post,self.new_post)

    def test_save_comment(self):
        self.new_comment.save_comment()
        self.assertTrue(len(Comment.query.all())>0)