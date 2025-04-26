
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.secret_key = 'your_secret_key'

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        subject = request.form['subject']
        if file and subject:
            upload_path = os.path.join(app.config['UPLOAD_FOLDER'], subject)
            os.makedirs(upload_path, exist_ok=True)
            file.save(os.path.join(upload_path, file.filename))
            return redirect(url_for('home'))
    return render_template('upload.html')

@app.route('/notes/<subject>')
def notes(subject):
    files = os.listdir(os.path.join(app.config['UPLOAD_FOLDER'], subject))
    return render_template('notes.html', files=files, subject=subject)

@app.route('/uploads/<subject>/<filename>')
def uploaded_file(subject, filename):
    return send_from_directory(os.path.join(app.config['UPLOAD_FOLDER'], subject), filename)

if __name__ == '__main__':
    app.run(debug=True)
