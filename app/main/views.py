from . import main
from flask import render_template,url_for,flash,redirect,abort,request
from ..models import User,Blog,Comment
from .forms import UpdateProfile,BlogForm,CommentForm
from flask_login import login_required,current_user
from datetime import datetime
from .. import db,photos

@main.route('/')
def home():
    title= 'Home - Pitch APP '
    return render_template('index.html',title=title)

@main.route('/about')
def about():
    title= 'About - Blog APP '
    return render_template('about.html',title=title)


@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()
    blogs_count = Blog.count_blogs(uname)
    user_joined = user.date_joined.strftime('%b %d, %Y')

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user,blogs = blogs_count,date = user_joined)


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

    return render_template('profile/update.html',form = form)


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



@main.route('/blog/new', methods = ['GET','POST'])
@login_required
def new_blog():
    blog_form = BlogForm()
    if blog_form.validate_on_submit():
        title = blog_form.title.data
        blog = blog_form.text.data
        category = blog_form.category.data

        # Updated blog instance
        new_blog = Blog(blog_title=title,blog_content=blog,category=category,user=current_user,likes=0,dislikes=0)

        # Save blog method
        new_blog.save_blog()
        return redirect(url_for('.home'))

    title = 'New blog'
    return render_template('new_blog.html',title = title,blog_form=blog_form )


@main.route('/blogs/fashion_blogs')
@login_required
def fashion_blogs():

    blogs = Blog.get_blogs('fashion')

    return render_template("fashion_blogs.html", blogs = blogs)

@main.route('/blogs/lifestyle_blogs')
@login_required
def lifestyle_blogs():

    blogs = Blog.get_blogs('lifestyle')

    return render_template("lifestyle_blogs.html", blogs = blogs)

@main.route('/blogs/travel_blogs')
@login_required
def travel_blogs():

    blogs = Blog.get_blogs('travel')

    return render_template("travel_blogs.html", blogs = blogs)



@main.route('/blogs/music_blogs')
@login_required
def music_blogs():

    blogs = Blog.get_blogs('music')

    return render_template("music_blogs.html", blogs = blogs)


@main.route('/blogs/fitness_blogs')
@login_required
def fitness_blogs():

    blogs = Blog.get_blogs('fitness')

    return render_template("fitness_blogs.html", blogs = blogs)


@main.route('/blog/<int:id>', methods = ['GET','POST'])
def blog(id):
    blog = Blog.get_blog(id)
    posted_date = blog.posted.strftime('%b %d, %Y')

    if request.args.get("like"):
        blog.likes = blog.likes + 1

        db.session.add(blog)
        db.session.commit()

        return redirect("/blog/{blog_id}".format(blog_id=blog.id))

    elif request.args.get("dislike"):
        blog.dislikes = blog.dislikes + 1

        db.session.add(blog)
        db.session.commit()

        return redirect("/blog/{blog_id}".format(blog_id=blog.id))

    comment_form = CommentForm()
    if comment_form.validate_on_submit():
        comment = comment_form.text.data

        new_comment = Comment(comment = comment,user = current_user,blog_id = blog)

        new_comment.save_comment()


    comments = Comment.get_comments(blog)

    return render_template("blog.html", blog = blog, comment_form = comment_form, comments = comments, date = posted_date)

@main.route('/user/<uname>/blogs')
def user_blogs(uname):
    user = User.query.filter_by(username=uname).first()
    blogs = Blog.query.filter_by(user_id = user.id).all()
    blogs_count = Blog.count_blogs(uname)
    user_joined = user.date_joined.strftime('%b %d, %Y')

    return render_template("profile/blogs.html", user=user,blogs=blogs,blogs_count=blogs_count,date = user_joined)