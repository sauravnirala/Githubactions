from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL
import os

app = Flask(__name__)

app.config["MYSQL_HOST"] = os.getenv("MYSQL_HOST", "mysql")
app.config["MYSQL_USER"] = os.getenv("MYSQL_USER", "root")
app.config["MYSQL_PASSWORD"] = os.getenv("MYSQL_PASSWORD", "root")
app.config["MYSQL_DB"] = os.getenv("MYSQL_DB", "employee_db")

mysql = MySQL(app)


@app.route("/")
def index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM employees")
    employees = cur.fetchall()
    cur.close()
    return render_template("index.html", employees=employees)


@app.route("/add", methods=["GET", "POST"])
def add():

    if request.method == "POST":

        name = request.form["name"]
        department = request.form["department"]
        salary = request.form["salary"]

        cur = mysql.connection.cursor()

        cur.execute(
            "INSERT INTO employees(name,department,salary) VALUES(%s,%s,%s)",
            (name, department, salary),
        )

        mysql.connection.commit()
        cur.close()

        return redirect("/")

    return render_template("add.html")


@app.route("/edit/<int:id>")
def edit(id):

    cur = mysql.connection.cursor()

    cur.execute("SELECT * FROM employees WHERE id=%s", (id,))
    employee = cur.fetchone()

    cur.close()

    return render_template("edit.html", employee=employee)


@app.route("/update/<int:id>", methods=["POST"])
def update(id):

    name = request.form["name"]
    department = request.form["department"]
    salary = request.form["salary"]

    cur = mysql.connection.cursor()

    cur.execute(
        "UPDATE employees SET name=%s,department=%s,salary=%s WHERE id=%s",
        (name, department, salary, id),
    )

    mysql.connection.commit()
    cur.close()

    return redirect("/")


@app.route("/delete/<int:id>")
def delete(id):

    cur = mysql.connection.cursor()

    cur.execute("DELETE FROM employees WHERE id=%s", (id,))

    mysql.connection.commit()
    cur.close()

    return redirect("/")


@app.route("/health")
def health():
    return {"status": "UP"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
