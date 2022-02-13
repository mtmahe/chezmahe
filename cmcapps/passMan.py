import sqlite3
import sys

from werkzeug.security import generate_password_hash



""" Update password """
def main():

    if len(sys.argv) !=3:
        sys.exit("Usage: python poassMan.py username newPassword")

    username = sys.argv[1]
    password = sys.argv[2]
    hashword = generate_password_hash(password)

    # Add database
    db = sqlite3.connect('crypto.db', check_same_thread=False)

    # Make sure it loaded
    if not db:
        print("Could not load database")
        sys.exit(1)

    cur = db.cursor()

    # Change password in db
    cur.execute("UPDATE users SET hash = ? WHERE username = ?", (hashword, username))

    db.commit()


if __name__ == "__main__":
	main()
