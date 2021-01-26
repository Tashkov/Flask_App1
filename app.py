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

# welcome screen for the user with two choices
@app.route('/')
def index():
    return render_template('index.html')

# this is used to create posts in the DB
@app.route('/posts', methods = ['GET', 'POST'])
def posts():
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

# this is used for deleting the posts in the DB
@app.route('/posts/delete/<int:id>')
def delete(id):
    post = Blogpost.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    return redirect('/posts')

# this is used for editing the posts in the DB
@app.route('/posts/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):

    post = Blogpost.query.get_or_404(id)

    if request.method == "POST":
        post.title = request.form['title']
        post.author = request.form['author']
        post.content = request.form['content']
        db.session.commit()
        return redirect('/posts')
    else:
        return render_template('edit.html', post=post)

# This is used when user clicks -> NO
@app.route('/goodbye')
def exititing():
    return render_template('goodbye.html')

if __name__ == "__main__":
    app.run(debug=True)
