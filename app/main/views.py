from datetime import datetime
from flask import render_template,request,redirect,url_for,abort,flash
from flask_login import login_required,current_user
from . import main
from ..models import User,Post,Comment,Subscriber
from .forms import UpdateProfile,PostForm,CommentForm,UpdatePost
from .. import db,photos 
from ..requests import get_quotes


@main.route('/')
def index():
    
    post = Post.get_all_posts()
    quote = get_quotes()
    title = 'HOME - Pesonal Blog'
    return render_template('index.html',title = title,posts = post,quote = quote)


@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()

    if user is None:
        abort(404)

    return render_template('profile/profile.html',user = user)


@main.route('/user/<uname>/update',methods = ['GET','POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',uname=user.username))

    title = 'Update bio'
    return render_template('profile/update.html',form =form,title = title)


@main.route('/user/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile',uname=uname))


@main.route('/blog/post',methods = ['GET','POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data

        new_post = Post(title = title,content = content,posted = datetime.now(),user = current_user)

        new_post.save_post()
        return redirect(url_for('main.index',id = new_post.id))

    title = 'New Blog'
    return render_template('new_post.html',title = title,form = form)
      

@main.route('/blog/update/post', methods = ['GET','POST'])
@login_required
def update_post(id):
    post = Post.query.get_or_404(id)

    form = UpdatePost()

    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data

        db.session.add(post)
        db.session.commit()

        return redirect(url_for('main.index'))

    elif request.method == 'GET':
        form.title.data = post.title
        form.content = post.content

    title = 'Update post'
    return render_template('update_post.html',title = title,post = post,update_form = form)

@main.route('/blog/delete/post', methods = ['GET','POST'])
@login_required
def delete_post(id):
    post = Post.get_post_id(id)

    db.session.delete(post)
    db.session.commit()

    return redirect(url_for('index.html',id = post.id))


@main.route('/blog/post/comment/<int:id>',methods = ['GET','POST'])
@login_required
def new_comment(id):
    form = CommentForm()
    comment = Comment.get_comment(id)
    post = Post.get_post_id(id)
    if form.validate_on_submit():
        content = form.content.data

        new_comment = Comment(content = content,user = current_user,post_id = post.id)

        new_comment.save_comment()
        return redirect(url_for('main.new_comment',id = post.id))

   
    title = 'Comment'
    return render_template('new_comment.html',title = title,comment = comment,comment_form = form)
