import bcrypt
import sys
import os

# Ensuring the backend path is accessible
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from backend.database import Database

class LoginHandler: 
    def __init__(self, db_instance):
        #store the database connection here so the class can use it
        self.db = db_instance

    def hash_password(self, password: str) -> str:
        byte_password = password.encode('utf-8')
        pw_hash = bcrypt.hashpw(byte_password, bcrypt.gensalt())
        return pw_hash.decode('utf-8')

    def check_password(self, password: str, hashed: str) -> bool:
        if not hashed:
            return False
        # bcrypt.checkpw returns True or False on its own
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))


#Logic test
#only run when this file is specifically run
if __name__ == "__main__":
    db_conn = Database()
    handler = LoginHandler(db_conn) # Instantiate the class and pass in the db_conn object

    user_input = input('Enter username: ').strip()
    pass_input = input('Enter password: ')

    # Use the handler to get the hash
    stored_hash = handler.db.get_password_hash(user_input)

    # Call the method via the 'handler' instance
    if handler.check_password(pass_input, stored_hash):
        print("Login successful")
    else:
        print("Invalid username or password")

