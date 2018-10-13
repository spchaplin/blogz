from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:@localhost:3306/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    post_title = db.Column(db.String(300))
    post_content = db.Column(db.String(50000))  

    def __init__(self, post_title, post_content):
        self.post_title = post_title
        self.post_content = post_content

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
        new_post = Blog(post_title, post_content)
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

if __name__ == '__main__':
    app.run()