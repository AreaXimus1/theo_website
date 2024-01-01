from flask import Flask, render_template, redirect, url_for, request, flash, jsonify
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import SubmitField, IntegerField, DecimalField
from wtforms.validators import DataRequired, NumberRange
from werkzeug.utils import secure_filename
import os
import shutil
import pandas as pd

from initial_processing import initial_processing
from secondary_processing import secondary_processing, tertiary_processing


DATA_FOLDER = 'data'
UPLOAD_FOLDER = 'uploads'
iupred_number = None


app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)


# CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
db = SQLAlchemy()
db.init_app(app)


# CONFIGURE TABLE
class ParameterForm(FlaskForm):
    disorder_score = DecimalField("Disorder Score (0 - 1)", validators=[DataRequired(), NumberRange(min=0, max=1, message="Please give a number between 0 and 1.")])
    sequence_length = IntegerField("Sequence Length (1 - ∞)", validators=[DataRequired()])
    merge_closer_than = IntegerField("Merge Sequences if Closer than X (1 - ∞)", validators=[DataRequired()])
    submit = SubmitField('Submit')


with app.app_context():
    db.create_all()


@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template("index.html")


@app.route('/how-to-use/', methods=['GET','POST'])
def how_to_use():
    return render_template("use_instructions.html")


@app.route('/upload')
def upload_page():
    return render_template('upload.html')


@app.route('/process_upload', methods=['POST'])
def process_upload():
    global iupred_number
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
    iupred_number = initial_processing(DATA_FOLDER, UPLOAD_FOLDER)
    

    return redirect("/process-files")


@app.route("/process-files", methods=["GET", "POST"])
def process_files():
    form = ParameterForm()

    if form.validate_on_submit():
        disorder = float(form.disorder_score.data)
        sequence = int(form.sequence_length.data)
        merge = int(form.merge_closer_than.data)
        secondary_processing(DATA_FOLDER, iupred_number, disorder, sequence, merge)
        tertiary_processing(DATA_FOLDER)
        return redirect("/")

    return render_template("process_files.html", form=ParameterForm())


@app.route("/dataset", methods=["GET", "POST"])
def dataset():
    table = pd.read_csv(
        f"{DATA_FOLDER}/final_results/final_csv.csv",
        encoding="unicode-escape",
        usecols=[
            "Identifier",
            "Number of disordered regions",
            "Disordered region",
            "Disorder score in SIM region",
            "Number of SIMs",
            "Amino Acid Regions with SIMs",
            "SIM Sequences",
            "Type of SIM",
            "SIM Amino acid region",
            "D/E",
            "S/T",
            "P"
            ]
        )
    return render_template("dataset.html", data=table.to_html(classes="table table-hover", index=False))


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


if __name__ == "__main__":
    app.run(debug=True, port=5002)
