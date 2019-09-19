import os
import Generator
import mysql.connector
import getpass

action_prompt = "[C - Create a password, R - Retrieve a password, E - Exit the Program, S - Show All]\n"

def mkeysetup() -> str:
    mkeyprompt = "Please choose a non-empty masterkey:\n"
    mkey2prompt = "Please re-enter your masterkey:\n"
    mkey = getpass.getpass(prompt = mkeyprompt)
    while not mkey:
        print("Your masterkey was empty!")
        mkey = getpass.getpass(prompt = mkeyprompt)

    mkey2 = getpass.getpass(prompt = mkey2prompt)
    while mkey2 != mkey:
        print("Your masterkeys did not match!")
        mkey2 = getpass.getpass(prompt = mkey2prompt)
    print("Setup complete, enter you masterkey 1 more time to begin!")
    return mkey


def ascii():
    print("WELCOME TO ")
    print("  __   __   ______     __  __     __         ______ ");
    print(" /\ \ / /  /\  __ \   /\ \/\ \   /\ \       /\__  _\ ")
    print(" \ \ \ /   \ \  __ \  \ \ \_\ \  \ \ \____  \/_/\ \/ ")
    print("  \ \__|    \ \_\ \_\  \ \_____\  \ \_____\    \ \_\ ")
    print("   \/_/      \/_/\/_/   \/_____/   \/_____/     \/_/ ")
    print("\n")

def main():

    master = False

    ascii()

    db = mysql.connector.connect(
          host="localhost",
          user="root",
          passwd="password"
        )

    mycursor = db.cursor();
    mycursor.execute("DROP DATABASE main")
    mycursor.execute("SHOW DATABASES")

    for x in mycursor:
        if 'main' == x[0]:
            master = True;
            break;
    else:
        mycursor.execute("CREATE DATABASE main")
        mycursor.execute("USE main")
        mycursor.execute("CREATE TABLE passwords (website VARCHAR(255), \
        username_email VARCHAR(255), password VARCHAR(255), PRIMARY KEY(website, username_email))")

        mkey = mkeysetup()

        mycursor.execute("INSERT INTO passwords VALUES(%s, %s, %s)", ("SYSTEM", "MASTER", mkey))
        master = True;


    key = getpass.getpass(prompt = "Please enter your masterkey:\n")

    mycursor.execute("SELECT password FROM passwords WHERE website = %s AND \
                               username_email = %s", ("SYSTEM", "MASTER"))
    myresult = mycursor.fetchone()

    while key != myresult[0]:
        key = getpass.getpass(prompt = "Your masterkey was wrong! Please re-enter your master key:\n")

    action = ''

    if master:
        while action == '':
            action = input(action_prompt)
            if action.lower() == 'c':
                username = input('Please enter your username/email')
                usage = input('Please enter the website/usage')
                mycursor.execute("SELECT * FROM passwords WHERE username_email = %s AND website = %s", (username, usage))
                count = mycursor.rowcount
                print(count)
                print("working here")
                print(record)
                if record == "":
                    print("nothing found!")
                break
                if usage in pws or usage in usrs:
                    print('You already have a login for this website!')
                    break
                length = input('Please enter a length')
                password = Generator.gen(int(length))
                print('this is your password:')
                print(password)
                appendable = open(b_txt, 'a')
                append = '\n' + usage + '-' + username + ':' + password
                appendable.write(append)
                action = ''
            if action.lower() == 'r':
                usage = input('What is the usage/website?')
                username = 'username' + ':' + usrs[usage]
                password = 'password' + ':' + pws[usage]
                print(username)
                print(password)
                action = ''


if __name__ == "__main__":
    main()
