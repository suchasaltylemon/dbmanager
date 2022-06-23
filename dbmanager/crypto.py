from base64 import b64encode
from os import urandom
from hashlib import sha256
from uuid import uuid4

from .db import DB

SALT_SIZE_BYTES = 64
ENCODING = "utf-8"


class CryptoDB:
    def __init__(self, manager, db_name):
        self.db = CryptoDB.create_login_db(manager, db_name)

    def email_taken(self, email):
        return self.db.get_table("Accounts").has_row({"Email": email})

    def change_email(self, current_email, new_email):
        assert self.email_taken(current_email)

        self.db.get_table("Accounts").update_row("Email", current_email, {
            "Email": new_email
        })

    def change_password(self, email, new_password):
        salt = self.generate_salt()
        encrypted_password = self.encrypt_password(new_password, salt)
        account_id = self.db.get_table("Accounts").get_row({
            "Email": email
        })

        self.db.get_table("Salts").update_row({
            "AccountId": account_id
        }, {
            "Salt": salt
        })

        self.db.get_table("Accounts").update_row({
            "AccountId": account_id
        }, {
            "Password": encrypted_password
        })

    def add_account(self, email, password):
        assert not self.email_taken(email), "Email already taken"

        account_id = self.generate_uuid()
        salt = self.generate_salt()
        encrypted_password = self.encrypt_password(password, salt)

        accounts = self.db.get_table("Accounts")
        salts = self.db.get_table("Salts")

        accounts.add_row({
            "AccountId": account_id,
            "Email": email,
            "Password": encrypted_password
        })

        salts.add_row({
            "AccountId": account_id,
            "Salt": salt
        })

    def password_is_correct(self, email, password):
        account = self.db.get_table("Accounts").get_row({"Email": email})

        account_id = account.get("AccountId", None)
        assert account_id is not None, "Account not found"

        correct_password = account.get("Password", None)
        assert correct_password is not None, "Password not found"

        salt = self.db.get_table("Salts").get_row({
            "AccountId": account_id
        }).get("Salt", None)
        assert salt is not None, "Salt not found"

        encrypted_password = self.encrypt_password(password, salt)

        return encrypted_password == correct_password

    @staticmethod
    def generate_salt():
        return b64encode(urandom(SALT_SIZE_BYTES)).hex()

    @staticmethod
    def encrypt_password(password, salt):
        return sha256((password + salt).encode(ENCODING)).hexdigest()

    @staticmethod
    def generate_uuid():
        return uuid4().hex

    @staticmethod
    def create_login_db(manager, db_name) -> DB:
        logins_db = manager.get_database(db_name)

        if not logins_db.has_table("Accounts"):
            logins_db.create_table("Accounts", [
                ("AccountId", "string", ["UNIQUE", "NOT NULL", "PRIMARY KEY"]),
                ("Email", "string", ["UNIQUE", "NOT NULL"]),
                ("Password", "string", ["NOT NULL"])])

        if not logins_db.has_table("Salts"):
            logins_db.create_table("Salts", [
                ("AccountId", "string", ["UNIQUE", "NOT NULL", "PRIMARY KEY"]),
                ("Salt", "string", [])
            ])

        return logins_db
