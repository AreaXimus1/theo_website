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

from flask import Flask, flash, request, redirect, url_for


app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
ckeditor = CKEditor(app)
Bootstrap5(app)





# CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
UPLOAD_FOLDER = 'uploads'
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


##WTForm
class CreatePostForm(FlaskForm):
    title = StringField("Blog Post Title", validators=[DataRequired()])
    subtitle = StringField("Subtitle", validators=[DataRequired()])
    author = StringField("Your Name", validators=[DataRequired()])
    img_url = StringField("Blog Image URL", validators=[DataRequired(), URL()])
    body = CKEditorField("Blog Content", validators=[DataRequired()])
    submit = SubmitField("Submit Post")


class UploadForm(FlaskForm):
    pass


@app.route('/', methods=['GET', 'POST'])
def home():
    result = db.session.execute(db.select(BlogPost))
    posts = result.scalars().all()
    return render_template("index.html", all_posts=posts)



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
    existing_iupred_results_path = os.path.join(app.config['UPLOAD_FOLDER'], 'IUPred_Results.txt')
    existing_nuclear_scores_path = os.path.join(app.config['UPLOAD_FOLDER'], 'Nuclear_Scores.csv')

    if os.path.exists(existing_iupred_results_path):
        os.remove(existing_iupred_results_path)

    if os.path.exists(existing_nuclear_scores_path):
        os.remove(existing_nuclear_scores_path)

    # Save the new files
    iupred_results.save(os.path.join(app.config['UPLOAD_FOLDER'], 'IUPred_Results.txt'))
    nuclear_scores.save(os.path.join(app.config['UPLOAD_FOLDER'], 'Nuclear_Scores.csv'))

    return jsonify({'message': 'Files uploaded successfully'})












@app.route("/edit-post/<int:post_id>", methods=["GET", "POST"])
def edit_post(post_id):
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
        post.author = edit_form.author.data
        post.body = edit_form.body.data
        db.session.commit()
        return redirect(url_for("show_post", post_id=post.id))
    return render_template("make-post.html", form=edit_form, is_edit=True)


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
