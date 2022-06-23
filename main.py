from dbmanager import Manager, CryptoDB

PATH = r"C:/Users/Sam/PycharmProjects/dbmanager/db"


def main():
    with Manager(PATH) as manager:
        password_db = CryptoDB(manager, "Logins")

        email = input("Email: ")
        password = input("Password: ")

        if password_db.email_taken(email):
            print(password_db.password_is_correct(email, password))

        else:
            password_db.add_account(email, password)


if __name__ == "__main__":
    main()
