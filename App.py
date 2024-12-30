from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector

app = Flask(__name__)
app.secret_key = "your_secret_key"

def db_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="lms",
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error connecting to database: {err}")
        return None

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        connection = db_connection()
        if not connection:
            flash("Database connection failed. Please try again later.")
            return redirect(url_for("login"))

        try:
            cursor = connection.cursor(dictionary=True)
            query = """
                SELECT user_id, username, role, first_name, last_name 
                FROM users 
                WHERE username=%s AND password=%s
            """
            cursor.execute(query, (username, password))
            user = cursor.fetchone()
        except mysql.connector.Error as err:
            print(f"Error during login query: {err}")
            flash("An error occurred. Please try again.")
            user = None
        finally:
            cursor.close()
            connection.close()

        if user:
            session["user_id"] = user["user_id"]
            session["username"] = user["username"]
            session["role"] = user["role"]
            session["full_name"] = f"{user['first_name']} {user['last_name']}"
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid username or password!")

    return render_template("index.html")

@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.")
    return redirect(url_for("login"))

@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if "user_id" not in session:
        flash("You need to log in first!")
        return redirect(url_for("login"))

    connection = db_connection()
    if not connection:
        flash("Database connection failed. Please try again later.")
        return render_template("dashboard.html", users=[], full_name=session.get("full_name", "User"), role=session.get("role", "User"))

    users = []
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        email = request.form.get("email")
        role = request.form.get("role")
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")

        if username and password and email and role and first_name and last_name:
            try:
                cursor = connection.cursor()
                query = """
                    INSERT INTO users (username, password, email, role, first_name, last_name)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """
                cursor.execute(query, (username, password, email, role, first_name, last_name))
                connection.commit()
                flash("User added successfully!")
            except mysql.connector.Error as err:
                print(f"Error adding user: {err}")
                flash("An error occurred while adding the user. Please try again.")
            finally:
                cursor.close()
        else:
            flash("All fields are required to add a user.")

    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
    except mysql.connector.Error as err:
        print(f"Error fetching users: {err}")
        flash("An error occurred while fetching users. Please try again.")
    finally:
        cursor.close()
        connection.close()

    return render_template("dashboard.html", users=users, full_name=session.get("full_name", "User"), role=session.get("role", "User"))

@app.route("/delete_user", methods=["POST"])
def delete_user():
    if "user_id" not in session:
        flash("You need to log in first!")
        return redirect(url_for("login"))

    user_id = request.form["user_id"]

    connection = db_connection()
    if not connection:
        flash("Database connection failed. Please try again later.")
        return redirect(url_for("dashboard"))

    try:
        cursor = connection.cursor()
        query = "DELETE FROM users WHERE user_id = %s"
        cursor.execute(query, (user_id,))
        connection.commit()
        flash("User deleted successfully!")
    except mysql.connector.Error as err:
        print(f"Error deleting user: {err}")
        flash("An error occurred while deleting the user. Please try again.")
    finally:
        cursor.close()
        connection.close()

    return redirect(url_for("dashboard"))

if __name__ == "__main__":
    app.run(debug=True)
