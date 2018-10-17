from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:@localhost:3306/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'd+(yL5}5t|^|J69!k2.Q'

### classes - db table and column setup

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    post_title = db.Column(db.String(300))
    post_content = db.Column(db.String(50000))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))  

    def __init__(self, post_title, post_content, owner):
        self.post_title = post_title
        self.post_content = post_content
        self.owner = owner

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    blogs = db.relationship('Blog', backref='owner')

    def __init__(self, username, password):
        self.username = username
        self.password = password

### routes

@app.before_request
def require_login():
    restricted_routes = ['newpost']
    if request.endpoint in restricted_routes and 'username' not in session:
        return redirect('/login')

# login page - get request - initial form render or rerender on error
@app.route("/login")
def login():
    page_title = "Login"
    username = request.args.get("username")
    username_format_error = request.args.get("username_format_error")
    pw1_format_error = request.args.get("pw1_format_error")
    username_exists_error = request.args.get("username_exists_error")
    wrong_pw_error = request.args.get("wrong_pw_error")

    if not username:
        # prevents "None" from displaying for null value
        username = ""

    if not username_exists_error:
        # prevents "None" from displaying for null value
        username_exists_error = ""

    if not username_format_error:
        username_format_error = ""
    else:
        # if error with username, reset the field
        username = ""

    if not wrong_pw_error:
        wrong_pw_error = ""

    if not pw1_format_error:
        pw1_format_error = ""
    
    return render_template('login.html', page_title=page_title, username=username, username_exists_error=username_exists_error, username_format_error=username_format_error, wrong_pw_error=wrong_pw_error, pw1_format_error=pw1_format_error)

# handle posted login form

@app.route("/login", methods=['POST'])
# logic for form validation below
def validate_login():
    is_valid_form = True
    # anything that invalidates form goes below...
    username = request.form['username']
    pw1 = request.form['password']
    user_stored = User.query.filter_by(username=username).first()

    # test that username in db
    if not user_stored:
        is_valid_form = False
        username_exists_error = "Username does not exist."
    else:
        username_exists_error = ""

    # test that password is correct
    if user_stored:
        correct_password = user_stored.password
        if pw1 != correct_password:
            is_valid_form = False
            wrong_pw_error = "The password for this user is incorrect."
        else:
            wrong_pw_error = ""
    else:
        #user is not in db
        wrong_pw_error = ""

    # test for valid username format
    if " " in username or len(username) < 3 or len(username) > 20:
        is_valid_form = False
        username_format_error = "Usernames must be 3 to 20 characters, and cannot include spaces."
    else:
        # must have some value to use as arg for str.format() later
        username_format_error = ""

    # test pw1 format
    if " " in pw1 or len(pw1) < 3 or len(pw1) > 20:
        is_valid_form = False
        pw1_format_error = "Passwords must be 3 to 20 characters, and cannot include spaces."
    else:
        pw1_format_error = ""

    # based on boolean value set above in conditionals...
    if is_valid_form:
        # get request
        session['username'] = username
        flash("Welcome, you successfully logged in.", "status")
        return redirect("/newpost?username={0}".format(username))
    else:
        # get request
        return redirect("/login?username={username}&username_exists_error={username_exists_error}&username_format_error={username_format_error}&wrong_pw_error={wrong_pw_error}&pw1_format_error={pw1_format_error}".format(username=username, username_exists_error=username_exists_error, username_format_error=username_format_error, wrong_pw_error=wrong_pw_error,pw1_format_error=pw1_format_error))

# signup page - get request - initial form render or rerender on error
@app.route("/signup")
def signup():
    page_title = "Signup"
    username = request.args.get("username")
    username_format_error = request.args.get("username_format_error")
    pw1_format_error = request.args.get("pw1_format_error")
    pw2_format_error = request.args.get("pw2_format_error")
    pw_match_error = request.args.get("pw_match_error")
    existing_user_error = request.args.get("existing_user_error")

    if not username:
        # prevents "None" from displaying for null value
        username = ""

    if not username_format_error:
        username_format_error = ""
    else:
        # if error with username, reset the field
        username = ""

    if not existing_user_error:
        existing_user_error = ""
    else:
        username = ""

    if not pw1_format_error:
        pw1_format_error = ""
    if not pw2_format_error:
        pw2_format_error = ""
    if not pw_match_error:
        pw_match_error = ""
    return render_template('signup.html', page_title=page_title, username=username, username_format_error=username_format_error, pw1_format_error=pw1_format_error, pw2_format_error=pw2_format_error, pw_match_error=pw_match_error, existing_user_error=existing_user_error)

# handle posted login form

@app.route("/signup", methods=['POST'])
# logic for form validation below
def validate_signup():
    is_valid_form = True
    # anything that invalidates form goes below...
    username = request.form['username']
    pw1 = request.form['password']
    pw2 = request.form['re_enter_password']

    # test for valid username
    if " " in username or len(username) < 3 or len(username) > 20:
        is_valid_form = False
        username_format_error = "Usernames must be 3 to 20 characters, and cannot include spaces."
    else:
        # must have some value to use as arg for str.format() later
        username_format_error = ""

    # test pw1 format
    if " " in pw1 or len(pw1) < 3 or len(pw1) > 20:
        is_valid_form = False
        pw1_format_error = "Passwords must be 3 to 20 characters, and cannot include spaces."
    else:
        pw1_format_error = ""
    # test pw2 format
    if " " in pw2 or len(pw2) < 3 or len(pw2) > 20:
        is_valid_form = False
        pw2_format_error = "Passwords must be 3 to 20 characters, and cannot include spaces."
    else:
        pw2_format_error = ""
    # test pw match format
    if pw1 != pw2:
        is_valid_form = False
        pw_match_error = "Passwords must match."
    else:
        pw_match_error = ""

    # test for existing user
  
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        existing_user_error = "You entered an existing user. Please enter a unique username."
    else:
        existing_user_error = ""

    # based on values determined above...
   
    # add user to db and session 
    if is_valid_form and not existing_user:
        new_user = User(username, pw1)
        db.session.add(new_user)
        db.session.commit()
        session['username'] = username
        flash("Welcome, you successfully registered and are now logged in.", "status")

        # get request
        return redirect("/newpost?username={0}".format(username))
    else:
        # get request - rerender the form
        return redirect("/signup?username={username}&username_format_error={username_format_error}&pw1_format_error={pw1_format_error}&pw2_format_error={pw2_format_error}&pw_match_error={pw_match_error}&existing_user_error={existing_user_error}".format(username=username,username_format_error=username_format_error, pw1_format_error=pw1_format_error, pw2_format_error=pw2_format_error, pw_match_error=pw_match_error, existing_user_error=existing_user_error))

@app.route('/blog')
def index():

    id = request.args.get('id')
    if id:
        page_title = "Single Post"
        #if post id in parameters, render that post's page
        single_post = Blog.query.filter_by(id=id).first()
        single_post_title = single_post.post_title
        single_post_content = single_post.post_content
        return render_template('onepost.html', page_title=page_title, single_post_title=single_post_title, single_post_content=single_post_content)
    else:
        page_title = "Main - Posts List"
        #list all the blog posts
        posts = Blog.query.all()
        return render_template('posts.html', posts=posts, page_title=page_title)

@app.route('/newpost', methods=['GET', 'POST'])
def newpost():
    page_title = "Post Entry"
    if request.method == 'POST':
        ### form validation ###
        is_valid_form = True
        post_title = request.form['post_title']
        post_content = request.form['post_content']
        if post_title == '':
            post_title_error = 'Please enter a post title.'
            is_valid_form = False
        else:
            #varialble must have some value b/f refrenced
            post_title_error = ''
        if post_content == '':
            post_content_error = 'Please enter some post content.'
            is_valid_form = False
        else:
            post_content_error = ''
        if not is_valid_form:
            #get request
            return redirect('/newpost?post_title={post_title}&post_content={post_content}&post_title_error={post_title_error}&post_content_error={post_content_error}'.format(post_title=post_title, post_content=post_content,post_title_error=post_title_error, post_content_error=post_content_error))
        ### end form validation ###

        #if form is valid, write record to db and redirect to this new post's page...
        #setup owner variable later
        #single_post = Blog.query.filter_by(id=id).first()
        owner = User.query.filter_by(username=session['username']).first()
        new_post = Blog(post_title, post_content, owner)
        db.session.add(new_post)
        db.session.commit()
        new_post_id = new_post.id
        return redirect('/blog?id={new_post_id}'.format(new_post_id=new_post_id))
    
    #if form is not being posted, render form as get request...
    post_title = request.args.get('post_title')
    post_content = request.args.get('post_content')
    post_title_error = request.args.get('post_title_error')
    post_content_error = request.args.get('post_content_error')

    if not post_title:
        # prevents 'None' from displaying for null value
        post_title = ''
    if not post_content:
        post_content = ''
    if not post_title_error:
        post_title_error = ''
    if not post_content_error:
        post_content_error = ''

    return render_template('newpost.html', page_title=page_title, post_title=post_title, post_content=post_content, post_title_error=post_title_error, post_content_error=post_content_error)

@app.route('/logout')
def logout():
    if 'username' in session:
        del session['username']
        flash("Goodbye, you successfully logged out.", "status")
    return redirect('/blog')

if __name__ == '__main__':
    app.run()