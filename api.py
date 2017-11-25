import check, databaseConnection


#start api -------------------------------------------------------------------
def executeApiAction(functionName, arguments):
    # TODO rate limiting and user profiles
    return (globals()[functionName](arguments))
    #    return {'errorCode': 0}


def addRating(arguments):  #funNum: 1
    errorCode = None  # 1: ok | 2: error in calculate | 3: pago doesn't exist | 0: unknown
    link = arguments[0]
    username = arguments[1]
    rating = arguments[2]
    if not check.UrlValidity(link) == 1:
        errorCode = 3
        return {'errorCode': errorCode}
    userid = databaseConnection.executeSql(
        "SELECT `id` FROM `users` WHERE `username`='{}'", username)[0]['id']
    databaseConnection.executeSql(
        "INSERT INTO `inputs` ( `userid`,`link`,`rating`) VALUES ('{}', '{}', '{}')",
        (userid, link, rating))
    errorCode = 1
    if executeApiAction('calculateRatings', [link])['errorCode'] != 1:
        errorCode = 2
    return {'errorCode': errorCode}


def calculateRatings(arguments):
    link = arguments[0]
    errorCode = None  #1: ok; 2: url invalid
    allLinkRating = 0.0
    allLinkRatingCount = 0

    result = databaseConnection.executeSql(
        "SELECT `link`, `rating` FROM `inputs` WHERE `link`='{}'", link)
    for row in result:
        allLinkRating = allLinkRating + float(row["rating"])
        allLinkRatingCount = allLinkRatingCount + 1
    rating = allLinkRating / allLinkRatingCount  #main rating for this link

    isInDbCode = check.IfisInRatingsDb(link)
    if isInDbCode == 1:  #updates link's entry
        databaseConnection.executeSql(
            "UPDATE ratings SET rating='{}' WHERE link='{}'", (rating, link))
    elif isInDbCode == 2:  #inserts new entry for new link
        databaseConnection.executeSql(
            "INSERT INTO ratings (link,rating) VALUES ('{}', '{}')",
            (link, rating))
    errorCode = 1
    return {'errorCode': errorCode}


def getLinkRating(link):
    errorCode = None
    rating = -1
    if check.IfisInRatingsDb(link):
        result = databaseConnection.executeSql(
            "SELECT `rating` FROM `ratings` WHERE `link`='{}'", link)
        rating = result[0]['rating']
        errorCode = 1
    else:
        errorCode = 0
    return {'errorCode': errorCode, 'rating': rating}


#end api ----------------------------------------------------------------------

print()
