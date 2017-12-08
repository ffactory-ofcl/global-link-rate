from databaseConnection import executeSql
import log


def executeApiAction(functionName, arguments):
    # TODO rate limiting and user profiles
    return (globals()[functionName](arguments))


def gainXp(arguments):
    errorCode = None
    username = arguments[0]
    reason = arguments[1]
    amount = arguments[2]

    currentXP = executeSql("SELECT xp FROM `users` WHERE username = '{}'",
                           username)[0]['xp']
    newXP = currentXP + amount
    #print(currentXP[0]['xp'])
    if executeSql("UPDATE users SET xp='{}' WHERE username='{}'",
                  (newXP, username)) == ():
        log.writeLog(username, 'info', 'Gained {} xp. Reason: {}'.format(
            amount, reason))
        errorCode = 1
    else:
        errorCode = 0
    return errorCode
