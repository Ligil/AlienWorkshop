import shelve, User, Furniture
db = shelve.open('storage.db', 'c')

emptyDict = {}

userDict = db['Users']
for id in userDict:
    userObject = userDict[id]
    userObject.set_reviewsDict(emptyDict)

furnitureDict = db['Furniture']
for id in furnitureDict:
    furnitureObject = furnitureDict[id]
    furnitureObject.set_reviews({'lastId':0})
db['Users'] = userDict
db['Furniture'] = furnitureDict

db.close()
