"""
Flask Blog Application
-----------------------

A feature-rich blogging platform implemented using Flask. This application includes the following functionalities:

- User Authentication:
  - Secure user registration and login with hashed passwords.
  - User session management with Flask-Login.
- Blog Post Management:
  - Create, edit, and delete blog posts (admin only).
  - View all blog posts on the homepage.
- Comments System:
  - Authenticated users can add and delete comments.
  - Decorators enforce access restrictions for deleting comments.
- Profile Avatars:
  - Gravatar integration for user profile images.
- Rich Text Editing:
  - CKEditor for creating and editing blog posts.
- Responsive UI:
  - Bootstrap for user-friendly and mobile-responsive design.

Main Components:
- **Database Models**:
  - `User`: Stores user information, including login credentials.
  - `BlogPost`: Represents individual blog posts with relationships to comments.
  - `Comment`: Manages user comments on blog posts.

- **Routes**:
  - `/`: Homepage displaying all posts.
  - `/register` and `/login`: User registration and login.
  - `/post/<int:post_id>`: Displays a single blog post and associated comments.
  - `/new-post`: Admin-only route for creating new posts.
  - `/edit-post/<int:post_id>`: Admin-only route for editing posts.
  - `/delete/<int:post_id>`: Admin-only route for deleting posts.
  - `/delete/comment/<int:comment_id>/<int:post_id>`: User-only route for deleting own comments.
  - `/about` and `/contact`: Static informational pages.

- **Extensions**:
  - Flask-Bootstrap: Simplifies integration with Bootstrap CSS framework.
  - Flask-CKEditor: Adds WYSIWYG editor functionality.
  - Flask-Gravatar: Automatically generates avatars for users.
  - Flask-SQLAlchemy: ORM for managing the database schema and queries.

Usage:
- Run the application locally using `flask run`.
- The admin is the first registered user and has exclusive rights to manage posts.
- Authentication protects routes that modify content or user data.

Dependencies:
- Flask, Flask-Bootstrap, Flask-CKEditor, Flask-Login, Flask-SQLAlchemy, Flask-Gravatar
- SQLAlchemy for ORM

This application demonstrates modularity, extensibility, and adherence to best practices in Flask development.
"""

from datetime import date
from flask import Flask, abort, render_template, redirect, url_for, flash, request
from flask_bootstrap import Bootstrap5
from flask_ckeditor import CKEditor
from flask_gravatar import Gravatar
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user, login_required
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text
from functools import wraps
from flask_gravatar import Gravatar
from sqlalchemy.testing.suite.test_reflection import users
from werkzeug.security import generate_password_hash, check_password_hash
# Import your forms from the forms.py
from forms import CreatePostForm, RegisterForm, LoginForm, CommentForm

# Initialize Flask app and configure extensions
app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
ckeditor = CKEditor(app)
Bootstrap5(app)

#=== To avoid  version warning and serve locally
app.config['CKEDITOR_SERVE_LOCAL'] = True
app.config['CKEDITOR_PKG_TYPE'] = 'standard'
app.config['CKEDITOR_CONFIG']={'versionCheck':False}
#==================================================

# Configure Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)


# Configure SQLAlchemy
class Base(DeclarativeBase):
    pass
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)

# For adding profile images to the comment section
gravatar = Gravatar(app,
                    size=100,
                    rating='g',
                    default='retro',
                    force_default=False,
                    force_lower=False,
                    use_ssl=False,
                    base_url=None)


# CONFIGURE TABLES
class BlogPost(db.Model):
    __tablename__ = "blog_posts"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    subtitle: Mapped[str] = mapped_column(String(250), nullable=False)
    date: Mapped[str] = mapped_column(String(250), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    author: Mapped[str] = mapped_column(String(250), nullable=False)
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)
    author_id: Mapped[int] = db.Column(db.Integer,db.ForeignKey("users.id"))

    #********** Parent Relationship ****************
    comments = relationship("Comment",back_populates="parent_post")


# Create a User table for all your registered users.
class User(UserMixin,db.Model):
    __tablename__ = "users"
    id:Mapped[int] = mapped_column(Integer,primary_key=True)
    email:Mapped[str] = mapped_column(String(250),unique=True)
    password:Mapped[str] = mapped_column(String(250),nullable=False)
    name:Mapped[str] = mapped_column(String(100))

    # Relationship to comments
    comments = relationship("Comment", back_populates="comment_author")

# Create Comment table to store user's comment on the Blog post.
class Comment(db.Model):
    __tablename__ = "comments"
    id:Mapped[int] = mapped_column(Integer, primary_key= True)
    text:Mapped[str] = mapped_column(Text,nullable = False)

    #**********Child Relationship ***************************
    author_id:Mapped[int] = mapped_column(Integer,db.ForeignKey("users.id"))
    comment_author = relationship("User",back_populates="comments")

    post_id:Mapped[int] = mapped_column(Integer,db.ForeignKey("blog_posts.id"))
    parent_post = relationship("BlogPost",back_populates="comments")



# Create database tables
with app.app_context():
    db.create_all()


@login_manager.user_loader
def load_user(user_id):
    """Retrieve user by ID."""
    return  db.session.get(User,user_id)

#  Use Werkzeug to hash the user's password when creating a new user.
@app.route('/register',methods = ["GET","POST"])
def register():
    """Register a new user."""
    form = RegisterForm()
    if  form.validate_on_submit():

        email = form.email.data
        password = form.Password.data
        name = form.name.data

        # Check if User already exists
        existing_user = User.query.filter_by(email = email).first()
        if existing_user:
            flash(" User already exit, Please Log in!")
        else:
            # Create New User
            hashed_password = generate_password_hash(password)
            new_user = User(
                email = email,
                password = hashed_password,
                name = name
            )
            db.session.add(new_user)
            db.session.commit()
            # Login and authenticate user after adding details to database
            flash("You have been registered ,Please Log in!!")
            login_user(new_user)
        return  redirect(url_for("login"))

    return render_template("register.html",form = form,current_user = current_user)


#  Retrieve a user from the database based on their email.
@app.route('/login',methods = ["GET","POST"])
def login():
    """Log in an existing user."""
    form = LoginForm()
    if request.method == "POST":
        email = form.email.data
        password = form.password.data
        user = db.session.execute(db.select(User).where(User.email==email)).scalar()
        if user:
            if check_password_hash(user.password,password):
                login_user(user)
                return redirect(url_for("get_all_posts"))
            else:
                flash("Invalid Password!! Please Try again!!")
                print("Invalid Password !!")
                return redirect(url_for("login"))
        elif not user:
            flash("User not found.Please register")
            return render_template("register.html",not_registered = True)
    return render_template("login.html",form = form,current_user= current_user)


@app.route('/logout')
@login_required
def logout():
    """Log out the current user."""
    logout_user()
    return redirect(url_for('get_all_posts'))


@app.route('/')
def get_all_posts():
    """Display all blog posts."""
    result = db.session.execute(db.select(BlogPost))
    posts = result.scalars().all()
    return render_template("index.html", all_posts=posts,current_user=current_user)

def admin_only(f):
    """Decorator to restrict access to admin users."""
    @wraps(f)
    def decorated_function(*args,**kwargs):
        # if id is not 1 then return abort 403 error
        if  (current_user.is_authenticated and current_user.id != 1) or (not current_user.is_authenticated):
            return abort(403)
        # Otherwise continue with route function
        return f(*args,**kwargs)
    return decorated_function

# The decorator to allow user to delete it's own comment.
def only_commenter(function):
    """Decorator to restrict comment deletion to the commenter."""
    @wraps(function)
    def check(comment_id,*args,**kwargs):
        comment = db.session.execute(
            db.select(Comment).where(Comment.id == comment_id, Comment.author_id == current_user.id)).scalar()
        if not current_user.is_authenticated or not comment:
            return abort(403)
        return  function(comment_id,*args,**kwargs)
    return check


# TODO: Allow logged-in users to comment on posts
@app.route("/post/<int:post_id>",methods=["GET", "POST"])
@login_required
def show_post(post_id):
    """Display a specific post and allow commenting."""
    requested_post = db.get_or_404(BlogPost, post_id)
    comment_form = CommentForm()
    if request.method == "POST":
        new_comment = Comment(
            text = request.form.get("comment"),
            author_id = current_user.id,
            post_id = post_id
        )
        db.session.add(new_comment)
        db.session.commit()
        # Debug relationships
    for comment in requested_post.comments:
        print(
            f"Comment ID: {comment.id}, Author: {comment.comment_author.id}, Email: {getattr(comment.comment_author, 'email', None)}")
    return render_template("post.html", post=requested_post,form =comment_form,current_user= current_user)


#  Use a decorator so only an admin user can create a new post
@app.route("/new-post", methods=["GET", "POST"])
@admin_only
def add_new_post():
    """Create a new blog post."""
    form = CreatePostForm()
    if form.validate_on_submit():
        new_post = BlogPost(
            title=form.title.data,
            subtitle=form.subtitle.data,
            body=form.body.data,
            img_url=form.img_url.data,
            author=current_user.name,
            date=date.today().strftime("%B %d, %Y"),
            author_id = current_user.id

        )
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for("get_all_posts"))
    return render_template("make-post.html", form=form)



# Use a decorator so only an admin user can edit a post
@app.route("/edit-post/<int:post_id>", methods=["GET", "POST"])
@admin_only
def edit_post(post_id):
    """Edit an existing blog post."""
    post = db.get_or_404(BlogPost, post_id)
    edit_form = CreatePostForm(
        title=post.title,
        subtitle=post.subtitle,
        img_url=post.img_url,
        author=post.author,
        body=post.body
    )
    if edit_form.validate_on_submit():
        post.title = edit_form.title.data
        post.subtitle = edit_form.subtitle.data
        post.img_url = edit_form.img_url.data
        post.author = current_user
        post.body = edit_form.body.data
        db.session.commit()
        return redirect(url_for("show_post", post_id=post.id))
    return render_template("make-post.html", form=edit_form, is_edit=True,current_user =current_user)


#  decorator so only an admin user can delete a post
@app.route("/delete/<int:post_id>")
@admin_only
def delete_post(post_id):
    """Delete a specific blog post."""
    post_to_delete = db.get_or_404(BlogPost, post_id)
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect(url_for('get_all_posts'))

# Delete Comment
@app.route("/delete/comment/<int:comment_id>/<int:post_id>")
@only_commenter
def delete_comment(comment_id,post_id):
    """Delete a specific comment."""
    comment_to_delete = db.session.execute(
        db.select(Comment).where(Comment.id == comment_id)).scalar()
    print(comment_to_delete)
    db.session.delete(comment_to_delete)
    db.session.commit()
    return redirect(url_for('show_post',post_id =post_id))



@app.route("/about")
def about():
    """Render the About page."""
    return render_template("about.html",current_user = current_user)


@app.route("/contact")
def contact():
    """Render the Contact page."""
    return render_template("contact.html",current_user = current_user)


if __name__ == "__main__":
    app.run(debug=True, port=5002)
