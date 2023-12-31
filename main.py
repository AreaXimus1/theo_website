from flask import Flask, render_template, redirect, url_for, request, flash, jsonify
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditor, CKEditorField
from werkzeug.utils import secure_filename
from datetime import date
import os
import shutil

from initial_processing import raw_processing

DATA_FOLDER = 'data'
UPLOAD_FOLDER = 'uploads'



app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
ckeditor = CKEditor(app)
Bootstrap5(app)




# CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
db = SQLAlchemy()
db.init_app(app)


# CONFIGURE TABLE
class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    subtitle = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(250), nullable=False)
    body = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    img_url = db.Column(db.String(250), nullable=False)


with app.app_context():
    db.create_all()


@app.route('/', methods=['GET', 'POST'])
def home():
    result = db.session.execute(db.select(BlogPost))
    posts = result.scalars().all()
    return render_template("index.html", all_posts=posts)


@app.route('/how-to-use/', methods=['GET','POST'])
def how_to_use():
    return render_template("use_instructions.html")


@app.route('/upload')
def upload_page():
    return render_template('upload.html')

@app.route('/process_upload', methods=['POST'])
def process_upload():
    iupred_results = request.files['iupredResults']
    nuclear_scores = request.files['nuclearScores']

    if iupred_results.filename == '' or nuclear_scores.filename == '':
        return jsonify({'error': 'Please select both files'}), 400

    # Delete existing files with the same names
    try:
       shutil.rmtree(UPLOAD_FOLDER)
    except FileNotFoundError:
        pass
    os.mkdir(UPLOAD_FOLDER)

    # Save the new files
    iupred_results.save(os.path.join(app.config['UPLOAD_FOLDER'], 'iupred.txt'))
    nuclear_scores.save(os.path.join(app.config['UPLOAD_FOLDER'], 'nuclear.csv'))

    # Process iupred.txt and nuclear.csv
    raw_processing(DATA_FOLDER, UPLOAD_FOLDER)

    return render_template("index.html")



@app.route("/delete/<int:post_id>")
def delete_post(post_id):
    post_to_delete = db.get_or_404(BlogPost, post_id)
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect(url_for('get_all_posts'))


# Code from previous day
@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


if __name__ == "__main__":
    app.run(debug=True, port=5002)
