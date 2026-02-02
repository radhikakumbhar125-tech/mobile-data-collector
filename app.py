from flask import Flask, render_template, request, redirect, url_for, flash, send_file
from flask_sqlalchemy import SQLAlchemy
import pandas as pd

app = Flask(__name__)
app.secret_key = "supersecretkey123"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(20), nullable=False)
    mobile = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    symptoms = db.Column(db.Text, nullable=True)

@app.route('/')
def index():
    return redirect(url_for('form'))

@app.route('/form', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        new_client = Client(
            name=request.form['name'],
            age=request.form['age'],
            gender=request.form['gender'],
            mobile=request.form['mobile'],
            email=request.form['email'],
            symptoms=request.form['symptoms']
        )
        db.session.add(new_client)
        db.session.commit()
        flash("Data submitted successfully!", "success")
        return redirect(url_for('form'))
    return render_template('form.html')

@app.route('/admin')
def admin_panel():
    clients = Client.query.all()
    return render_template('admin_panel.html', clients=clients)

@app.route('/export')
def export_data():
    clients = Client.query.all()
    df = pd.DataFrame([{
        "Name": c.name,
        "Age": c.age,
        "Gender": c.gender,
        "Mobile": c.mobile,
        "Email": c.email,
        "Symptoms": c.symptoms
    } for c in clients])
    df.to_excel("data.xlsx", index=False)
    return send_file("data.xlsx", as_attachment=True)

if __name__ == "__main__":
    db.create_all()
    app.run(host="0.0.0.0", port=5000)
