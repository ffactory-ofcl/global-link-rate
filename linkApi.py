import check, databaseConnection  #, log


def executeApiAction(functionName, arguments=None):
    # TODO rate limiting and user profiles
    if arguments == None:
        return (globals()[functionName]())
    else:
        return (globals()[functionName](arguments))


def addRating(arguments):  #funNum: 1
    errorCode = None  # 1: ok | 2: error in calculate | 3: page doesn't exist | 4: invalid arg
    #return (arguments)
    username = arguments[0]
    link = arguments[1]
    rated = arguments[2]
    #return str(type(rated))
    allLinkRating = 0
    allLinkRatingCount = 0
    rating = 0

    #convert rating
    try:
        rated = int(rated)
    except:
        errorCode = 4
        return {'errorCode': errorCode}

    if not check.RatingValidity(rated) == 1:
        errorCode = 3
        return {'errorCode': errorCode}

    if not check.UrlValidity(link) == 1:
        errorCode = 3
        return {'errorCode': errorCode}
    userid = databaseConnection.executeSql(  #get user id
        "SELECT `id` FROM `users` WHERE `username`='{}'", username)[0]['id']

    #addRating
    databaseConnection.executeSql(  #add new input to db
        "INSERT INTO `inputs` ( `userid`,`link`,`rating`) VALUES ('{}', '{}', '{}')",
        (userid, link, rated))

    #calculateRating
    isInDbCode = check.IfisInRatingsDb(link)
    if isInDbCode == 1:  #updates link's entry
        allLinkRatingAndCount = databaseConnection.executeSql(
            "SELECT `allLinkRating`,`allLinkRatingCount` FROM `ratings` WHERE `link`='{}'",
            link)
        allLinkRating = allLinkRatingAndCount[0]['allLinkRating']
        allLinkRatingCount = allLinkRatingAndCount[0]['allLinkRatingCount']
        if allLinkRating == None or allLinkRatingCount == None:  #if link exists but has no alllinkrating/count
            allLinkRating = 0
            allLinkRatingCount = 0
            result = databaseConnection.executeSql(
                "SELECT `link`, `rating` FROM `inputs` WHERE `link`='{}'",
                link)
            for row in result:
                allLinkRating = allLinkRating + float(row["rating"])
                allLinkRatingCount = allLinkRatingCount + 1
            rating = allLinkRating / allLinkRatingCount  #main rating for this link
            databaseConnection.executeSql(
                "INSERT INTO ratings (link,rating,allLinkRating,allLinkRatingCount) VALUES ('{}', '{}', '{}', '{}')",
                (link, rating, allLinkRating, allLinkRatingCount))
        else:
            newAllLinkRating = allLinkRating + rated
            newAllLinkRatingCount = allLinkRatingCount + 1
            #raise debugMe('debug')
            if allLinkRating == None or allLinkRating == 0 or allLinkRating == '' or allLinkRatingCount == None or allLinkRatingCount == 0 or allLinkRatingCount == '':
                calculateLinkRating(link)
            else:
                rating = (newAllLinkRating) / (newAllLinkRatingCount)
                databaseConnection.executeSql(
                    "UPDATE ratings SET `rating`='{}', `allLinkRating`='{}', `allLinkRatingCount`='{}' WHERE link='{}'",
                    (rating, newAllLinkRating, newAllLinkRatingCount, link))
    elif isInDbCode == 2:  # recalculate from all input and insert new entry for new link
        result = databaseConnection.executeSql(
            "SELECT `link`, `rating` FROM `inputs` WHERE `link`='{}'", link)
        for row in result:
            allLinkRating = allLinkRating + float(row["rating"])
            allLinkRatingCount = allLinkRatingCount + 1
        rating = allLinkRating / allLinkRatingCount  #main rating for this link
        databaseConnection.executeSql(
            "INSERT INTO ratings (link,rating,allLinkRating,allLinkRatingCount) VALUES ('{}', '{}', '{}', '{}')",
            (link, rating, allLinkRating, allLinkRatingCount))
    else:
        errorCode = 0

    errorCode = 1
    return {'errorCode': errorCode}


def calculateLinkRating(arguments):
    link = arguments
    if isinstance(arguments, tuple):
        link = arguments[0]
    errorCode = None  #1: ok; 2: url invalid
    allLinkRating = 0
    allLinkRatingCount = 0

    result = databaseConnection.executeSql(
        "SELECT `link`, `rating` FROM `inputs` WHERE `link`='{}'", link)
    for row in result:
        allLinkRating = allLinkRating + float(row["rating"])
        allLinkRatingCount = allLinkRatingCount + 1
    if allLinkRating == None or allLinkRating == 0 or allLinkRating == '' or allLinkRatingCount == None or allLinkRatingCount == 0 or allLinkRatingCount == '':
        rating = 0
    else:
        rating = allLinkRating / allLinkRatingCount  #main rating for this link

    isInDbCode = check.IfisInRatingsDb(link)
    if isInDbCode == 1:  #updates link's entry
        databaseConnection.executeSql(
            "UPDATE ratings SET rating='{}', allLinkRating='{}', allLinkRatingCount='{}' WHERE link='{}'",
            (rating, allLinkRating, allLinkRatingCount, link))
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


def getTopLinkRatings():
    errorCode = None
    links = []
    if check.DbIsNotEmpty('ratings'):
        result = databaseConnection.executeSql(
            "SELECT * FROM `ratings` ORDER BY allLinkRating DESC", '', 3)
        for row in result:
            links.append(row)
    errorCode = 1
    return {'errorCode': errorCode, 'links': links}


def calculateAllLinks():
    errorCode = None
    #get all links
    if check.DbIsNotEmpty('ratings'):
        result = databaseConnection.executeSql("SELECT link FROM `ratings`",
                                               '', 'all')
        for row in result:
            calculateLinkRating(row)

    errorCode = 1
    return {'errorCode': errorCode}


class debugMe(Exception):
    pass


print(check.RatingValidity('3'))
