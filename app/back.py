from flask import *
import psycopg2 as sql
import os

back = Flask(__name__)

def connection():
    return sql.connect(
        database=os.getenv("DB_NAME", "phonebook"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", "lego"),
        host=os.getenv("DB_HOST", "localhost"),
    )


@back.route('/')
def main():
    conn = connection()
    curs = conn.cursor()
    curs.execute("""
    CREATE TABLE IF NOT EXISTS contacts (
        id SERIAL PRIMARY KEY,
        name TEXT NOT NULL,
        surname TEXT NOT NULL,
        phone TEXT NOT NULL
        );
    """)
    conn.commit()
    curs.close()
    conn.close()
    return render_template("index.html")

@back.route('/add', methods = ["POST"])
def add():
    conn = connection()
    curs = conn.cursor()

    name = request.form["name"]
    surname = request.form["surname"]
    phone = request.form["phone"]

    curs.execute("INSERT INTO contacts (name, surname, phone) VALUES (%s, %s, %s);", (name, surname, phone))
    conn.commit()
    curs.close()
    conn.close()

    return redirect("/?success=true")

@back.route('/delete', methods = ["POST"])
def delete():
    conn = connection()
    curs = conn.cursor()

    phone = request.form["phone"]

    curs.execute("DELETE FROM contacts WHERE phone = %s", (phone,))
    conn.commit()
    curs.close()
    conn.close()

    return redirect("/?success=true")

@back.route('/data', methods = ["GET"])
def view_data():
    conn = connection()
    curs = conn.cursor()

    curs.execute("SELECT * FROM contacts")
    data = curs.fetchall()
    conn.commit()
    curs.close()
    conn.close()

    return render_template("data.html", data = data)


@back.route('/edit', methods = ["POST"])
def edit():
    conn = connection()
    curs = conn.cursor()

    old_phone = request.form["old_phone"]
    new_name = request.form["new_name"]
    new_surname = request.form["new_surname"]
    new_phone = request.form["new_phone"]

    curs.execute("""
        UPDATE contacts 
        SET name = %s, surname = %s, phone = %s 
        WHERE phone = %s;
    """, (new_name, new_surname, new_phone, old_phone))

    conn.commit()
    curs.close()
    conn.close()

    return redirect("/?success=true")

if __name__ == '__main__':
    back.run(host = '0.0.0.0', port = 5000, debug = True)