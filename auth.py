from flask import session
from flask_bcrypt import Bcrypt
from db import execute_query

bcrypt = Bcrypt()

def register_user(username, password):
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    query = "INSERT INTO users (username, password) VALUES (%s, %s)"
    try:
        execute_query(query, (username, hashed_password))
        return True
    except Exception as e:
        print("error",e)
        return False

def verify_user(username, password):
    try:
        query = "SELECT password FROM users WHERE username = %s"
        result = execute_query(query, (username,), fetch_one=True) 

        if result is None:
            print("ERROR: User not found")
            return False

        if bcrypt.check_password_hash(result[0], password):
            session["user"] = username  
            return True

        print("ERROR: Incorrect password") 
        return False
    except Exception as e:
        print("ERROR:", e)
        return False
