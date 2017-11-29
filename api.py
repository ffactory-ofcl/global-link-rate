import linkApi, userApi


#start api -------------------------------------------------------------------
def executeApiAction(functionName, arguments):
    # TODO rate limiting and user profiles
    return (globals()[functionName](arguments))
    #    return {'errorCode': 0}


#end api ----------------------------------------------------------------------


class debugMe(Exception):
    pass


#print(getTopLinkRatings()['links'][0]['link'])
