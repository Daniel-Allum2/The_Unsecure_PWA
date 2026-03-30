import sqlite3 as sql
import time
import random
import bcrypt


def insertUser(username, password, DoB):
    con = sql.connect("database_files/database.db")
    cur = con.cursor()
    hashed_pw = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    cur.execute(
        "INSERT INTO users (username, password, dateOfBirth) VALUES (?, ?, ?)",
        (username, hashed_pw.decode("utf-8"), DoB),
    )
    con.commit()
    con.close()


def retrieveUsers(username, password):
    con = sql.connect("database_files/database.db")
    cur = con.cursor()
    cur.execute("SELECT password FROM users WHERE username = ?", (username,))
    row = cur.fetchone()
    if row is None:
        con.close()
        return False
    stored_hash = row[0]
    if isinstance(stored_hash, str):
        stored_hash = row[0].encode("utf-8")
    if bcrypt.checkpw(password.encode("utf-8"), stored_hash):
        with open("visitor_log.txt", "r") as file:
            number = int(file.read().strip())
            number += 1
        with open("visitor_log.txt", "w") as file:
            file.write(str(number))
        time.sleep(random.randint(80, 90) / 1000)

        con.close()
        return True

    else:
        con.close()
        return False


def insertFeedback(feedback):
    con = sql.connect("database_files/database.db")
    cur = con.cursor()
    cur.execute(f"INSERT INTO feedback (feedback) VALUES ('{feedback}')")
    con.commit()
    con.close()


def listFeedback():
    con = sql.connect("database_files/database.db")
    cur = con.cursor()
    data = cur.execute("SELECT * FROM feedback").fetchall()
    con.close()
    f = open("templates/partials/success_feedback.html", "w")
    for row in data:
        f.write("<p>\n")
        f.write(f"{row[1]}\n")
        f.write("</p>\n")
    f.close()
