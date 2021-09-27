import unittest
from app.models import Post,User
from app import db

class PostModelTest(unittest.TestCase):

    def setUp(self):
        self.user_Mark = User(username = 'Mark',password = 'love', email = 'mark@ds.com')
        self.new_post = Post(title = 'Skills',content = 'Know how to use your strengths and improve your weaknesses',user = self.user_Mark)


    def tearDown(self):
        Post.query.delete()
        User.query.delete()


    def test_check_instance_variables(self):
        self.assertEquals(self.new_post.title,'Skills')
        self.assertEquals(self.new_post.content,'Know how to use your strengths and improve your weaknesses')
        self.assertEquals(self.new_post.user,self.user_Mark)


    def test_save_post(self):
        self.new_post.save_post()
        self.assertTrue(len(Post.query.all())>0)