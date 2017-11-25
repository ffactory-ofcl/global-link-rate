#from flask import render_template
from userClass import User
import databaseConnection


def showProfile(username):
    return getUserinformation(username)


def getUserinformation(username):
    userinformation = getRawUserdataFromDb(username)
    _userid = userinformation['id']
    _username = userinformation['username']
    _role = userinformation['role']
    _xp = userinformation['xp']
    return User(_userid, _username, _role, _xp)


def getRawUserdataFromDb(username):
    return databaseConnection.executeSql(
        "SELECT * FROM `users` WHERE `username`='{}'", username)[0]


def gainXP(username, xpAmount):
    currentXP = databaseConnection.executeSql(
        "SELECT xp FROM `users` WHERE username = '{}'", username)[0]['xp']
    newXP = currentXP + xpAmount
    #print(currentXP[0]['xp'])
    if databaseConnection.executeSql(
            "UPDATE users SET xp='{}' WHERE username='{}'",
        (newXP, username)) == ():
        return True
    else:
        return False
