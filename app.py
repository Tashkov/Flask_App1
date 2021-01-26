from flask import Flask, render_template
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

@app.route('/posts')
def posts():
    return render_template('posts.html', posts=all_posts)

@app.route('/home/users/<string:name>/posts/<int:id>')
def hello(name, id):
    return f'Hello {name} your id is: {id}'

@app.route('/onlyget', methods = ['GET', 'POST']) 
def get_req():
    return 'You can only get this webpage'

if __name__ == "__main__":
    app.run(debug=True)
