from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy(app)

# This is a model for our DB
# Each variable in the class is an attribute
# Each new class will be a new entity
class Blogpost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(30), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # this will print out whenever we create a new blogpost
    def __repr__(self):
        return f'Blog post {self.id}'

all_posts = [
    {
        'title': 'Post1',
        'content': 'This is the content of Post 1',
        'author': "Georgi"
    },
    {
        'title': 'Post2',
        'content': 'This is the content of post 2'
    }
]

@app.route('/')
def index():
    return render_template('index.html')

# this is the uri for our app
@app.route('/posts', methods = ['GET', 'POST'])
def posts():
# the logic behind it can`t yet Create or Read, prompots DB
    if request.method == "POST":
        post_title = request.form['title']
        post_content = request.form['content']
        post_author = request.form['author']
        new_post = Blogpost(title=post_title, content=post_content, author=post_author)
        db.session.add(new_post)
        db.session.commit()
        return redirect('/posts')
    else:
        all_posts = Blogpost.query.order_by(Blogpost.date_posted).all()
        return render_template('posts.html', posts=all_posts)

@app.route('/home/users/<string:name>/posts/<int:id>')
def hello(name, id):
    return f'Hello {name} your id is: {id}'

@app.route('/onlyget', methods = ['GET', 'POST']) 
def get_req():
    return 'You can only get this webpage'

if __name__ == "__main__":
    app.run(debug=True)
