from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///employee.db"
app.config["SQLALCHEMY_TRACK_MODIFICATION"] = False


db = SQLAlchemy(app)
app.app_context().push()

class Employee(db.Model):
    sno = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(200), nullable = False)
    email = db.Column(db.String(200), nullable = False)
    department = db.Column(db.String(200), nullable = False)
    contact = db.Column(db.String(15), nullable = False)
    joined_date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"{self.sno} - {self.name}"

@app.route("/", methods=['GET', 'POST'])
def hello_world():
    if request.method == 'POST':
        #print("post")
        #print(request.form['name'])
        name = request.form['name']
        email = request.form['email']
        department = request.form['department']
        contact = request.form['contact']
        employee = Employee(name = name, email = email, department = department, contact = contact)   
        db.session.add(employee)
        db.session.commit()
    allemployee = Employee.query.all()
    return render_template("index.html", allemployee=allemployee)

@app.route("/display")
def display():
    allemployee = Employee.query.all()
    print(allemployee)
    return "This is page 2"

@app.route("/delete/<int:sno>")
def delete(sno):
    employee = Employee.query.filter_by(sno=sno).first()
    db.session.delete(employee)
    db.session.commit()
    return redirect("/")

@app.route("/update/<int:sno>", methods=['GET', 'POST'])
def update(sno):
    if request.method=='POST':
        name = request.form['name']
        email = request.form['email']
        department = request.form['department']
        contact = request.form['contact']
        employee = Employee.query.filter_by(sno=sno).first()
        employee.name = name
        employee.email = email
        employee.department = department
        employee.contact = contact
        db.session.add(employee)
        db.session.commit()
        return redirect("/")
    employee = Employee.query.filter_by(sno=sno).first()
    return render_template("update.html", employee=employee)


@app.route("/about")
def about():
    allemployee = Employee.query.all()
    print(allemployee)
    return render_template("about.html")


if __name__ == "__main__":
    app.run(debug=True, port=8000)