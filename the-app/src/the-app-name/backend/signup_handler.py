import bcrypt
import sys
import os
from backend.database import Database
from .logger import get_logger 

logger = get_logger("Signup Handler")
# Ensuring the backend path is accessible
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class SignupHandler: 
    def __init__(self, db_instance):
        self.db = db_instance

    def hash_password(self, password: str) -> str:
        """Hashes a plain-text password using bcrypt."""
        byte_password = password.encode('utf-8')
        # gensalt() generates the salt and mixes it into the hash automatically
        pw_hash = bcrypt.hashpw(byte_password, bcrypt.gensalt())
        return pw_hash.decode('utf-8')

    def register_user(self, username: str, password: str) -> bool:
        """
        Check if exists -> Hash -> Save.
        Returns True if successful, False if username taken or error.
        """
        # 1. Check if user already exists
        if self.db.get_password_hash(username):
            print(f"Error: User '{username}' already exists.")
            return False

        #Hash the password
        hashed_pw = self.hash_password(password)

        # 3. Store in the database
        success = self.db.create_user(username, hashed_pw)
        return success

# Logic test
# only run when this file is specifically run

if __name__ == "__main__":
    db_conn = Database()
    handler = SignupHandler(db_conn)

    new_user = input('Choose a username: ').strip()
    new_pass = input('Choose a password: ')

    if handler.register_user(new_user, new_pass):
        print(f"Registration successful for {new_user}!")
    else:
        print("Registration failed.")