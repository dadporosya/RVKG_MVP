from flask import Flask, render_template, request, make_response
import logging

# from project import dbManager as _dbManager
# from project import config
# from project import userManager as _userManager

import dbManager as _dbManager
import config
import userManager as _userManager
import _helpers as h
import CookieManager as CookieMan

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(message)s')

app = Flask(__name__)
dbMan = _dbManager.DbManager(config.DB_PATH)
userManager = _userManager.UserManager(dbMan)

DEBUG = True

@app.route("/", methods=["GET", "POST"])
def login():
    print(CookieMan.getCookie())
    if dbMan.isUserLoggedIn(CookieMan.getCookie()):
        return successfulLogin()


    return render_template("loginPage.html")


@app.route("/processLogin", methods=["GET", "POST"])
def processLogin():
    if DEBUG:
        logging.info("Start process login")

    print("COOKIE MAN COOK", CookieMan.getCookie())
    if dbMan.isUserLoggedIn(CookieMan.getCookie()):
        return successfulLogin()

    usernameIn = ''
    userPasswordIn = ''

    if request.method == "POST":
        usernameIn = request.form.get("username")
        userPasswordIn = request.form.get("password")
    
    exist = userManager.login(usernameIn, userPasswordIn)
        
    if exist:
        return successfulLogin()

    logMessage = "Account not found! Please, sign up first!"
    return render_template("registrationPage.html", logMessage=logMessage)

def successfulLogin():
    if DEBUG:
        logging.debug(f"Successful login")
    return render_template("successfulLogin.html")

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
    
    successfulRegistrationFlag = True
    logMessage = ""
    if userManager.checkIfUserExists(username = usernameIn):
        logMessage += "Username has been already taken! Choose a new one!"

    incorrectData = []
    for k, v in data.items():
        if not v:
            incorrectData.append(k)
            successfulRegistrationFlag = False
    
    logMessage += f"\nInvalid {", ".join(incorrectData)}"

    if successfulRegistrationFlag:
        return successfulRegistration(usernameIn, userPasswordIn, userFirstName, userLastName)
    
    return render_template("registrationPage.html", logMessage=logMessage)

def successfulRegistration(usernameIn, userPasswordIn, userFirstName, userLastName):
    data = userManager.addUser(usernameIn, userPasswordIn, userFirstName, userLastName)

    response = make_response(render_template("successfulLogin.html"))

    cookie = CookieMan.generateCookie()
    dbMan.saveCookie(data[0], cookie)
    dbMan.setCookieLoggedIn(cookie, True)

    response = CookieMan.setCookie(response, cookie)

    return response


@app.route("/set-cookie")
def setCookie(userId:str|None=None):
    cookie = CookieMan.generateCookie()
    if userId:
        dbMan.saveCookie(userId, cookie)

    return CookieMan.setCookie(cookie=cookie)


if __name__ == "__main__":
    app.run(debug=True)