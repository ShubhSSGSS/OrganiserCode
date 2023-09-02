import json
import random


def dataMerge(dataJson:str, dataID:int):
    '''Used to append either more plans to a particular user's plans
    or append more members to a particular plan.
    Returns : json string'''
    userPlans = json.loads(dataJson)
    userPlans[list(userPlans.keys())[0]].append(dataID)
    return json.dumps(userPlans)


def hashGen(genType):
    '''Returns a randomised hash based on whether genType equals 
    'UID' (for userID) or 'planID' (for planID) if the IDs aren't
    already present in the database.
    Returns : string'''
    fieldVals = [[chr(i) for i in range(97, 123)], [i for i in range(8)]]
    hashList = []

    for i in range(8):
        chosenFieldType = fieldVals[random.randint(0,1)]
        chosenFieldValue = chosenFieldType[random.randint(0, len(chosenFieldType)-1)]
        hashList.append(str(chosenFieldValue))

    return genType + ''.join(hashList)

def extractData(dataJson:str, extractType:str):
    '''Used to extract members of a particular plan or plans of
    a particular member. extractType can either be 'userPlans'
    (to extract plans) or 'planMembers' (to extract users).
    Returns : list'''
    return json.loads(dataJson)[extractType]