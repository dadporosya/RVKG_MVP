from flask import Flask, render_template, request
import logging

# from project import dbManager as _dbManager
# from project import config
# from project import userManager as _userManager

import dbManager as _dbManager
import config
import userManager as _userManager

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(message)s')

app = Flask(__name__)
dbManager = _dbManager.DbManager(config.DB_PATH)
userManager = _userManager.UserManager(dbManager)

DEBUG = True

@app.route("/", methods=["GET", "POST"])
def login():
    return render_template("loginPage.html")


@app.route("/processLogin", methods=["GET", "POST"])
def processLogin():
    if DEBUG:
        logging.info("Start process login")

    usernameIn = ''
    userPasswordIn = ''

    if request.method == "POST":
        usernameIn = request.form.get("username")
        userPasswordIn = request.form.get("password")
    
    exist = userManager.login(usernameIn, userPasswordIn)
        
    if exist:
        if DEBUG:
            logging.debug(f"Successful login by Username: {usernameIn}, Password: {userPasswordIn}")
        return render_template("successfulLogin.html")

    logMessage = "Account not found! Please, sign up first!"
    if DEBUG:
            logging.debug(f"Unsuccessful login by Username: {usernameIn}, Password: {userPasswordIn}")
    return render_template("registrationPage.html", logMessage=logMessage)


@app.route("/registration", methods=["GET", "POST"])
def registration():
    if DEBUG:
        logging.info("Registration")

    usernameIn = ''
    userPasswordIn = ''
    userFirstName = ''
    userLastName = ''

    if request.method == "POST":
        usernameIn = request.form.get("username")
        userPasswordIn = request.form.get("password")
        userFirstName = request.form.get("firstName")
        userLastName = request.form.get("lastName")
    
    data = {
        "Username": usernameIn,
        "Password": userPasswordIn,
        "First name": userFirstName,
        "Last name": userLastName
    }
    
    if DEBUG:
        logging.debug(f"Registration args: {', '.join(data.values())}")
    
    successfulRegistration = True
    logMessage = ""
    if userManager.checkIfUserExists(username = usernameIn):
        logMessage += "Username has been already taken! Choose a new one!"

    incorrectData = []
    for k, v in data.items():
        if not v:
            incorrectData.append(k)
            successfulRegistration = False
    
    logMessage += f"\nInvalid {", ".join(incorrectData)}"

    if successfulRegistration:
        userManager.addUser(usernameIn, userPasswordIn, userFirstName, userLastName)
        return render_template("successfulLogin.html")
    
    return render_template("registrationPage.html", logMessage=logMessage)


if __name__ == "__main__":
    app.run(debug=True)