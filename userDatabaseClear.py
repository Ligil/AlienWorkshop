import shelve

db = shelve.open('storage.db', 'c') #assign storage file to variable database, c stands for read and write
#del db['Users']
usersDict = db['Users']
usersObject = usersDict[1]
bought = usersObject.set_boughtItems([])
db['Users'] = usersDict
db.close()
