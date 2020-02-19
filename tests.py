#!flask/bin/python
import os
import unittest

from config import basedir
from app import app, db, bcrypt
from app.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required

class TestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()


    def test_user_database_add(self):
        # database is empty
        self.assertEqual(User.query.all(), [])
        hashed_password = bcrypt.generate_password_hash('asdf').decode('utf-8')
        user = User(username='karel', email='karel@gmail.com', password=hashed_password)
        db.session.add(user)
        db.session.commit()
        # database is not empty
        assert User.query.filter_by(username='karel') != None


    def test_post_database_add(self):
        # database is empty
        self.assertEqual(Post.query.all(), [])
        post = Post(title='First title', content="this blog", user_id=1)
        db.session.add(post)
        db.session.commit()
        # database is not empty
        assert Post.query.filter_by(user_id=1) != None


    def test_follow_and_unfollow(self):
        # add two users to User database
        hashed_password = bcrypt.generate_password_hash('asdf').decode('utf-8')
        t = User(username='tomas', email='tomas@email.cz', password=hashed_password)
        n = User(username='nikol', email='nikol@email.cz', password=hashed_password)
        db.session.add_all([t, n])
        db.session.commit()
        self.assertEqual(t.followed.all(), [])
        self.assertEqual(t.followers.all(), [])

        # Tomas follows Nikol
        t.follow(n)
        db.session.commit()
        self.assertTrue(t.is_following(n))
        self.assertEqual(t.followed.count(), 1)
        self.assertEqual(t.followed.first().username, 'nikol')
        self.assertEqual(n.followers.count(), 1)
        self.assertEqual(n.followers.first().username, 'tomas')

        # Nikol follows Tomas
        n.follow(t)
        db.session.commit()
        self.assertTrue(n.is_following(t))
        self.assertEqual(n.followed.count(), 1)
        self.assertEqual(n.followed.first().username, 'tomas')
        self.assertEqual(t.followers.count(), 1)
        self.assertEqual(t.followers.first().username, 'nikol')

        # Tomas unfollows Nikol
        t.unfollow(n)
        db.session.commit()
        self.assertFalse(t.is_following(n))
        self.assertEqual(t.followed.count(), 0)
        self.assertEqual(n.followers.count(), 0)


    def test_followed_user(self):
        # create four users
        hashed_password = bcrypt.generate_password_hash('asdf').decode('utf-8')
        t = User(username='tomas', email='tomas@email.uk', password=hashed_password)
        n = User(username='nikol', email='nikol@email.uk', password=hashed_password)
        r = User(username='rosta', email='rosta@email.uk', password=hashed_password)
        p = User(username='petra', email='petra@email.uk', password=hashed_password)
        db.session.add_all([t, n, r, p])

        # create four posts
        p1 = Post(title='first post', content='content of this post', user_id=1)
        p2 = Post(title='second post', content='content of this post', user_id=2)
        p3 = Post(title='third post', content='content of this post', user_id=2)
        p4 = Post(title='fourth post', content='content of this post', user_id=3)
        db.session.add_all([p1, p2, p3, p4])
        db.session.commit()

        # setup the followers
        t.follow(n)  # tomas follows nikol
        t.follow(r)  # tomas follows petra
        n.follow(t)  # nikol follows rosta
        r.follow(p)  # rosta follows petra
        db.session.commit()

        # check the followed posts of each user
        f1 = t.followed_posts().all()
        f2 = n.followed_posts().all()
        f3 = r.followed_posts().all()
        f4 = p.followed_posts().all()
        self.assertEqual(f1, [p4, p3, p2, p1])
        self.assertEqual(f2, [p3, p2, p1])
        self.assertEqual(f3, [p4])
        self.assertEqual(f4, [])

    




if __name__ == '__main__':
    unittest.main()