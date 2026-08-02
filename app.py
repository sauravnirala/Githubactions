from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import os
import pymysql

# Required for SQLAlchemy to use PyMySQL
pymysql.install_as_MySQLdb()

app = Flask(__name__)

# Database Configuration
DB_USER = os.getenv("MYSQL_USER", "root")
DB_PASSWORD = os.getenv("MYSQL_PASSWORD", "root")
DB_HOST = os.getenv("MYSQL_HOST", "mysql")
DB_NAME = os.getenv("MYSQL_DB", "employee_db")

app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


# Employee Table
class Employee(db.Model):
    __tablename__ = "employees"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    department = db.Column(db.String(100), nullable=False)
    salary = db.Column(db.Integer, nullable=False)


# Create table if it doesn't exist
with app.app_context():
    db.create_all()


@app.route("/")
def index():
    employees = Employee.query.all()
    return render_template("index.html", employees=employees)


@app.route("/add", methods=["GET", "POST"])
def add():

    if request.method == "POST":

        employee = Employee(
            name=request.form["name"],
            department=request.form["department"],
            salary=request.form["salary"]
        )

        db.session.add(employee)
        db.session.commit()

        return redirect("/")

    return render_template("add.html")


@app.route("/edit/<int:id>")
def edit(id):

    employee = Employee.query.get_or_404(id)

    return render_template("edit.html", employee=employee)


@app.route("/update/<int:id>", methods=["POST"])
def update(id):

    employee = Employee.query.get_or_404(id)

    employee.name = request.form["name"]
    employee.department = request.form["department"]
    employee.salary = request.form["salary"]

    db.session.commit()

    return redirect("/")


@app.route("/delete/<int:id>")
def delete(id):

    employee = Employee.query.get_or_404(id)

    db.session.delete(employee)
    db.session.commit()

    return redirect("/")


@app.route("/health")
def health():
    return {"status": "UP"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
