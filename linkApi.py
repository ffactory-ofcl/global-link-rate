import check, databaseConnection  #, log


def executeApiAction(functionName, arguments=None):
    # TODO rate limiting and user profiles
    if arguments == None:
        return (globals()[functionName]())
    else:
        return (globals()[functionName](arguments))


def addRating(arguments):  #funNum: 1
    # 1: ok | 2: error in calculate
    # 3: invalid arg type 4: invalid rating
    # 5: invalid link | 6: error in addrating
    # 7: error while updating
    errorCode = None

    username = arguments[0]
    link = arguments[1]
    rated = arguments[2]

    allLinkRating = 0
    allLinkRatingCount = 0
    rating = 0

    #convert rating
    try:
        rated = int(rated)
    except:
        errorCode = 3
        return {'errorCode': errorCode}

    if not check.RatingValidity(rated) == 1:
        errorCode = 4
        return {'errorCode': errorCode}

    if not check.UrlValidity(link) == 1:
        errorCode = 5
        return {'errorCode': errorCode}
    #userid = databaseConnection.executeSql(  #get user id
    #    "SELECT `id` FROM `users` WHERE `username`='{}'", username)[0]['id']

    #addRating
    if databaseConnection.executeMDb('inputs', 'insert', {
            'username': username,
            'link': link,
            'rated': rated
    })['errorCode'] != 1:
        errorCode = 6
        return {'errorCode': errorCode}
    #databaseConnection.executeSql(  #add new input to db
    #    "INSERT INTO `inputs` ( `username`,`link`,`rating`) VALUES ('{}', '{}', '{}')",
    #    (username, link, rated))

    #calculateRating
    isInDbCode = check.IfisInRatingsDb(link)
    #print('isindb: ' + str(isInDbCode))
    if isInDbCode == 1:  #updates link's entry
        #print('updating link\'s entry')
        #allLinkRatingAndCount = databaseConnection.executeSql(
        #    "SELECT `allLinkRating`,`allLinkRatingCount` FROM `ratings` WHERE `link`='{}'",
        #    link)

        allLinkRatingAndCount = databaseConnection.executeMDb(
            'ratings', 'find', {
                'link': link
            })['dbReturn']
        #print(allLinkRatingAndCount[0]['allLinkRating'])
        allLinkRating = allLinkRatingAndCount[0]['allLinkRating']
        allLinkRatingCount = allLinkRatingAndCount[0]['allLinkRatingCount']
        #print(allLinkRating)
        if allLinkRating == None or allLinkRatingCount == None:  #if link exists but has no alllinkrating/count
            allLinkRating = 0
            allLinkRatingCount = 0
            result = databaseConnection.executeMDb(
                'inputs', 'find', {'link': link}, 'all')['dbReturn']
            #result = databaseConnection.executeSql(
            #    "SELECT `link`, `rating` FROM `inputs` WHERE `link`='{}'",
            #    link)
            #CONTINUE HERE RERERERERREEREEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE (check if ratingcount is proper)
            #print(allLinkRatingCount)
            for row in result:
                allLinkRating = allLinkRating + float(row['rating'])
                allLinkRatingCount = allLinkRatingCount + 1
            rating = allLinkRating / allLinkRatingCount  #main rating for this link
            if databaseConnection.executeMDb(
                    'ratings', 'insert', {
                        'link': link,
                        'rating': rating,
                        'allLinkRating': allLinkRating,
                        'allLinkRatingCount': allLinkRatingCount
                    })['errorCode'] != 1:
                errorCode = 7
                return {'errorCode': errorCode}
            #databaseConnection.executeSql(
            #    "INSERT INTO ratings (link,rating,allLinkRating,allLinkRatingCount) VALUES ('{}', '{}', '{}', '{}')",
            #    (link, rating, allLinkRating, allLinkRatingCount))
        else:  #link exists and alllinkrating (+count) need to be updated
            #print('alllinkr ' + str(allLinkRating))
            newAllLinkRating = allLinkRating + rated
            newAllLinkRatingCount = allLinkRatingCount + 1
            #print('newalllinkr' + str(newAllLinkRating))
            #raise debugMe('debug')
            if allLinkRating == None or allLinkRating == 0 or allLinkRating == '' or allLinkRatingCount == None or allLinkRatingCount == 0 or allLinkRatingCount == '':
                #print('ree somtingwong')
                calculateLinkRating(link)
            else:
                #print('allgoodmyboy')
                rating = (newAllLinkRating) / (newAllLinkRatingCount)
                #print('rating: ' + str(rating))
                if databaseConnection.executeMDb(
                        'ratings', 'update', [{
                            'link': link
                        }, {
                            '$set': {
                                'rating': rating,
                                'allLinkRating': newAllLinkRating,
                                'allLinkRatingCount': newAllLinkRatingCount
                            }
                        }])['errorCode'] != 1:
                    errorCode = 7
                    #return {'errorCode': errorCode}
                #databaseConnection.executeSql(
                #    "UPDATE ratings SET `rating`='{}', `allLinkRating`='{}', `allLinkRatingCount`='{}' WHERE link='{}'",
                #   (rating, newAllLinkRating, newAllLinkRatingCount, link))
        #print('yay me is done :)')
        errorCode = 1
    elif isInDbCode == 2:  # recalculate from all input and insert new entry for new link
        #print('recalculating link from all input')
        result = databaseConnection.executeMDb(
            'inputs', 'find', {'link': link}, 'all')['dbReturn']
        #print(type(result))
        #result = databaseConnection.executeSql(
        #    "SELECT `link`, `rating` FROM `inputs` WHERE `link`='{}'", link)
        for row in result:
            allLinkRating = allLinkRating + float(row['rated'])
            allLinkRatingCount = allLinkRatingCount + 1
        rating = allLinkRating / allLinkRatingCount  #main rating for this link
        if databaseConnection.executeMDb(
                'ratings', 'insert', {
                    'link': link,
                    'rating': rating,
                    'allLinkRating': allLinkRating,
                    'allLinkRatingCount': allLinkRatingCount
                })['errorCode'] != 1:
            errorCode = 5
            #return {'errorCode': errorCode}
            #databaseConnection.executeMDb('ratings','insert',{})
            #databaseConnection.executeSql(
            #    "INSERT INTO ratings (link,rating,allLinkRating,allLinkRatingCount) VALUES ('{}', '{}', '{}', '{}')",
            #    (link, rating, allLinkRating, allLinkRatingCount))
        errorCode = 1
    else:
        #print('error while checking if is in ratingdb')
        errorCode = 0

    #print('now returning ' + str(errorCode))
    return {'errorCode': errorCode}


def calculateLinkRating(arguments):
    link = arguments
    if isinstance(arguments, tuple):
        link = arguments[0]
    #print(link)
    errorCode = None  #1: ok; 2: url invalid; 3: error while updating
    allLinkRating = 0
    allLinkRatingCount = 0

    #result = databaseConnection.executeSql(
    #    "SELECT `link`, `rating` FROM `inputs` WHERE `link`='{}'", link)
    result = databaseConnection.executeMDb('inputs', 'find', {'link': link},
                                           'all')['dbReturn']
    #print(result[0])
    #print(result[1])
    #print(result[2])
    for row in result:
        #print(float(row['rated']))
        allLinkRating = allLinkRating + float(row['rated'])
        allLinkRatingCount = allLinkRatingCount + 1
    if allLinkRating == None or allLinkRating == 0 or allLinkRating == '' or allLinkRatingCount == None or allLinkRatingCount == 0 or allLinkRatingCount == '':
        rating = 0
    else:
        rating = allLinkRating / allLinkRatingCount  #main rating for this link

    isInDbCode = check.IfisInRatingsDb(link)
    #print('isindb: ' + str(isInDbCode))
    if isInDbCode == 1:  #updates link's entry
        #print(rating)
        #print(allLinkRating)
        #databaseConnection.executeSql(
        #    "UPDATE ratings SET rating='{}', allLinkRating='{}', allLinkRatingCount='{}' WHERE link='{}'",
        #    (rating, allLinkRating, allLinkRatingCount, link))
        if databaseConnection.executeMDb('ratings', 'update', [{
                'link': link
        }, {
                '$set': {
                    'rating': rating,
                    'allLinkRating': allLinkRating,
                    'allLinkRatingCount': allLinkRatingCount
                }
        }])['errorCode'] != 1:
            errorCode = 3
            return {'errorCode': errorCode}
    elif isInDbCode == 2:  #inserts new entry for new link
        databaseConnection.executeMDb(
            'ratings', 'insert', {
                'link': link,
                'rating': rating,
                'allLinkRating': allLinkRating,
                'allLinkRatingCount': allLinkRatingCount
            })
        #databaseConnection.executeSql(
        #    "INSERT INTO ratings (link,rating) VALUES ('{}', '{}')",
        #    (link, rating))
    errorCode = 1
    return {'errorCode': errorCode}


def getLinkRating(link):
    errorCode = None
    rating = -1
    if check.IfisInRatingsDb(link):
        rating = databaseConnection.executeMDb('ratings', 'find', {
            'link': link
        })['dbReturn'][0]['rating']

        errorCode = 1
    else:
        errorCode = 0
    return {'errorCode': errorCode, 'rating': rating}


def getTopLinkRatings():
    errorCode = None
    links = []
    if check.DbIsNotEmpty('ratings'):
        result = databaseConnection.executeMDb('ratings', 'find', {}, 'all',
                                               ['allLinkRating', -1])
        #print('res: ' + str(result))
        #result = databaseConnection.executeSql(
        #    "SELECT * FROM `ratings` ORDER BY allLinkRating DESC", '', 3)
        for row in result:
            links.append(row['dbReturn']['link'])
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


#getTopLinkRatings()
#print(getLinkRating('http://youtube.com'))
#print(calculateLinkRating('http://youtube.com'))
