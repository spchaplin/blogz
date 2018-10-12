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

@app.route('/', methods=['POST', 'GET'])
def index():

    if request.method == 'POST':
        post_title = request.form['post_title']
        post_content = request.form['post_content']
       # new_task = Task(task_name)
        new_post = Blog(post_title, post_content)
        db.session.add(new_post)
        db.session.commit()

    #tasks = Task.query.filter_by(completed=False).all()
    posts = Blog.query.all()
    page_title = "Scott's Blog"
    #completed_tasks = Task.query.filter_by(completed=True).all()
    return render_template('posts.html', posts=posts, page_title=page_title)

# @app.route('/delete-task', methods=['POST'])
# def delete_task():

#     task_id = int(request.form['task-id'])
#     task = Task.query.get(task_id)
#     task.completed = True
#     db.session.add(task)
#     db.session.commit()

#     return redirect('/')

if __name__ == '__main__':
    app.run()